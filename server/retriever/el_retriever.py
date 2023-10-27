import csv
import itertools
import os
import re
import spacy

from py2neo import Graph
from typing import Any, Dict, List, Tuple
from word2number import w2n

NUMBERS_TO_ADD = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "1st": 1,
    "2nd": 2,
    "3rd": 3,
    "4th": 4,
    "5th": 5,
    "6th": 6,
    "7th": 7,
    "8th": 8,
    "9th": 9,
    "10th": 10,
    "11th": 11,
    "12th": 12,
    "13th": 13,
    "14th": 14,
    "15th": 15,
    "16th": 16,
    "17th": 17,
    "18th": 18,
    "19th": 19,
    "20th": 20,
}
w2n.american_number_system.update(NUMBERS_TO_ADD)


class ELRetriever:
    """Retriever based on entity linking and query patterns."""

    def __init__(self) -> None:
        self.el = EntityLinker()
        self.qp = QueryPattern()
        self.graph = Graph(
            uri=os.environ.get("GRAPH_URI"),
            user=os.environ.get("GRAPH_USER"),
            password=os.environ.get("GRAPH_PASSWORD"),
        )

    def _execute_queries(self, queries: List[str]):
        """Execute queries on the graph."""
        facts = []
        for query in queries:
            facts += self.graph.run(query).data()
        return facts

    def run(self, question: str) -> str:
        """Retrieve context for a question based on a graph."""
        context = ""
        self.el.run(question)
        self.qp.run(self.el.question_entities)
        facts = self._execute_queries(self.qp.queries)
        if len(facts) == 0:
            new_queries = self.qp.add_intermediate_relations()
            facts = self._execute_queries(new_queries)
        for fact in facts:
            context += str(fact)
            context += "\n"
        if len(context) == 0:
            context = "[]"
        return context


class EntityLinker:
    """Entity linker used to identify graph entities in a question."""

    def __init__(self) -> None:
        self.spacy_model = spacy.load("en_core_web_sm")
        self.entities = self._load_entities()
        self.question_entities = {}

    def _load_entities(self) -> Dict[str, List[str]]:
        """Load the graph entites and synonyms."""
        entities_db = {}
        with open(
            "retriever/sdg_entities.csv", "r", encoding="utf-8-sig"
        ) as f:
            reader = csv.reader(f)
            for line in reader:
                concept = line[0]
                for label in line[1:]:
                    entities_db[label] = concept
        sorted_entities_db = sorted(
            list(entities_db.items()), key=lambda key: len(key[0]), reverse=True
        )
        entities_db = {}
        for key, val in sorted_entities_db:
            entities_db.setdefault(key, val)
        return entities_db

    def _extract_entities(self, sent: str) -> None:
        """Extract entities from a sentence."""
        sent_lower = sent.lower()
        for label, _ in self.entities.items():
            if label in sent_lower:
                if not (self.entities[label] in self.question_entities.keys()):
                    index = sent_lower.index(label)
                    self.question_entities[self.entities[label]] = {
                        "start": index,
                        "end": index + len(label),
                    }

    def _find_closest_concept(self, text: str, sent: str) -> str:
        """Find the closest concept of a word in a sententce."""
        start_index = sent.index(text)
        end_index = start_index + len(text)
        distance_min = len(sent)
        closest_concept = None
        for concept_name, concept_details in self.question_entities.items():
            if end_index <= concept_details["start"]:
                distance = concept_details["start"] - end_index
            elif concept_details["end"] <= start_index:
                distance = start_index - concept_details["end"]
            if distance < distance_min:
                distance_min = distance
                closest_concept = concept_name
        return closest_concept

    def _extract_number(self, spacy_sent: spacy.tokens.Doc) -> None:
        """Extract numerical information (numbers or text) in a sentence."""
        for token in spacy_sent:
            if token.like_num:
                if token.lower_.isdigit():
                    code = token.lower_
                else:
                    try:
                        code = str(w2n.word_to_num(token.lower_))
                    except:
                        break
                closest_concept = self._find_closest_concept(
                    token.lower_, spacy_sent.text
                )
                self.question_entities[closest_concept]["code"] = (
                    '{code:"' + code + '"}'
                )

    def _noun_in_entities(self, noun: str, sent: str) -> bool:
        """Check if a word is a graph entity."""
        found = False
        start_index = sent.lower().index(noun)
        end_index = start_index + len(noun)
        for concept_details in self.question_entities.values():
            if (concept_details["start"] <= start_index) and (
                concept_details["end"] >= end_index
            ):
                found = True
                break
        return found

    def _extract_complementary_info(self, spacy_sent: spacy.tokens.Doc):
        """Extract complementary nouns to entity in a sentence."""
        for token in spacy_sent:
            if token.pos_ == "NOUN":
                if not (self._noun_in_entities(token.lower_, spacy_sent.text)):
                    closest_concept = self._find_closest_concept(
                        token.lower_, spacy_sent.text
                    )
                    if (
                        "specifications"
                        in self.question_entities[closest_concept].keys()
                    ):
                        self.question_entities[closest_concept][
                            "specifications"
                        ].append(token.lower_)
                    else:
                        self.question_entities[closest_concept]["specifications"] = [
                            token.lower_
                        ]

    def run(self, question: str) -> None:
        """Extract graph entities and from a sentence."""
        spacy_sent = self.spacy_model(question)
        self._extract_entities(question)
        if len(self.question_entities) > 0:
            self._extract_number(spacy_sent)
            self._extract_complementary_info(spacy_sent)


class QueryPattern:
    """Query patterns construction for graph context extraction."""

    def __init__(self) -> None:
        self.queries = []

    def add_intermediate_relations(self) -> List[str]:
        """Modify requests to add intermediates relations."""
        new_queries = []
        for query in self.queries:
            rel_index = [rel.end() for rel in re.finditer("->", query)]
            for i, ind in enumerate(rel_index):
                new_query = f"{query[:ind]} (ne{i}) - [r] -> {query[ind:]}"
                new_queries.append(new_query)
        return new_queries

    def _create_query(self, entity_group: List[Tuple], entities: Dict[str, Any]) -> str:
        """Create cypher query from entity combinations."""
        query = "MATCH "
        for i, entity in enumerate(entity_group):
            if i == 0:
                query += f"""(e{i}:{entity}{entities[entity]['code'] if 'code' in entities[entity].keys() else ''}) -[r{i}]-> """
            elif i == len(entity_group) - 1:
                query += f"""(e{i}:{entity}{entities[entity]['code'] if 'code' in entities[entity].keys() else ''})"""
            else:
                query += f"""(e{i}:{entity}{entities[entity]['code'] if 'code' in entities[entity].keys() else ''}) -[r{i}]-> """

        spec_source = False
        for i, entity in enumerate(entity_group):
            if "specifications" in entities[entity].keys():
                if not (spec_source):
                    query += " WHERE "
                    spec_source = True
                else:
                    query += " AND "
                for j, specification in enumerate(entities[entity]["specifications"]):
                    if j > 0:
                        query += " AND "
                    query += f"""((e{i}.title CONTAINS \"{specification}\") OR (e{i}.description CONTAINS \"{specification}\") OR (e{i}.title CONTAINS \"{specification.capitalize()}\") OR (e{i}.description CONTAINS \"{specification.capitalize()}\"))"""

        query += " RETURN "
        for i, entity in enumerate(entity_group):
            if i == len(entity_group) - 1:
                query += f"""e{i} as entity_{i}"""
            else:
                query += f"""e{i} as entity_{i}, type(r{i}) as relation_{i}, """

        return query

    def run(self, entities: Dict[str, Any]) -> None:
        """Create cypher queries based on patters and entities found in the question."""
        if len(entities) == 1:
            entity = list(entities.keys())[0]
            query = f"""MATCH (e:{entity}{entities[entity]['code'] if 'code' in entities[entity].keys() else ''})"""
            if "specifications" in entities[entity].keys():
                query += " WHERE "
                for i, specification in enumerate(entities[entity]["specifications"]):
                    if i > 0:
                        query += " AND "
                    query += f"""((e.title CONTAINS \"{specification}\") OR (e.description CONTAINS \"{specification}\") OR (e.title CONTAINS \"{specification.capitalize()}\") OR (e.description CONTAINS \"{specification.capitalize()}\"))"""
            query += " RETURN e"
            self.queries.append(query)
        elif len(entities) > 1:
            entity_groups = itertools.permutations(entities.keys(), len(entities))
            for entity_group in entity_groups:
                self.queries.append(self._create_query(entity_group, entities))
