import os

from py2neo import Graph
from sentence_transformers import SentenceTransformer, util
from typing import Any, List, Dict, Tuple


class SimilarityRetriever:
    """Retriever based on semantic similarity."""

    def __init__(self) -> None:
        self.similarity_model = SentenceTransformer("all-mpnet-base-v2")
        self.graph = Graph(
            uri=os.environ.get("GRAPH_URI"),
            user=os.environ.get("GRAPH_USER"),
            password=os.environ.get("GRAPH_PASSWORD"),
        )

        self.facts = self._extract_graph_facts()
        self.embed_facts = self.similarity_model.encode(self.facts)

    def _extract_graph_facts(self) -> List[Any]:
        """Extract graph nodes and relations."""
        facts: List[Dict[Any, Any]] = self.graph.run(
            """MATCH (x)-[r]->(y) 
            RETURN head(labels(x)) as source, properties(x) as source_properties, type(r) as relation, head(labels(y)) as destination, properties(y) as destination_properties 
            """
        ).data()

        str_facts = []
        for fact in facts:
            relation = fact["source"]
            if "code" in fact["source_properties"].keys():
                relation += f" {fact['source_properties']['code']}"
            if "title" in fact["source_properties"].keys():
                relation += f" with title \"{fact['source_properties']['title']}\" "
            elif "description" in fact["source_properties"].keys():
                relation += f" {fact['source_properties']['description']}"
            relation += f"{fact['relation']} {fact['destination']}"
            if "code" in fact["destination_properties"].keys():
                relation += f" {fact['destination_properties']['code']}"
            if "title" in fact["destination_properties"].keys():
                relation += (
                    f" with title \"{fact['destination_properties']['title']}\" "
                )
            elif "description" in fact["destination_properties"].keys():
                relation += f" {fact['destination_properties']['description']}"
            str_facts.append(relation)

            if ("description" in fact["source_properties"].keys()) and (
                "title" in fact["source_properties"].keys()
            ):
                description = fact["source"]
                if "code" in fact["source_properties"].keys():
                    description += f" {fact['source_properties']['code']}"
                if "title" in fact["source_properties"].keys():
                    description += (
                        f" with title \"{fact['source_properties']['title']}\". "
                    )
                description += fact["source_properties"]["description"]
                if not description in str_facts:
                    str_facts.append(description)

            if ("description" in fact["destination_properties"].keys()) and (
                "title" in fact["destination_properties"].keys()
            ):
                description = fact["destination"]
                if "code" in fact["destination_properties"].keys():
                    description += f" {fact['destination_properties']['code']} "
                if "title" in fact["destination_properties"].keys():
                    description += (
                        f"with title \"{fact['destination_properties']['title']}\". "
                    )
                description += fact["destination_properties"]["description"]
                if not description in str_facts:
                    str_facts.append(description)

        return str_facts

    def _extract_relevant_facts(self, fact_score_pairs: List[Tuple]):
        """Extract relevant facts with a similarity score above a threshold without exceeding the maximum size for the prompt."""
        context = []
        for score, fact in fact_score_pairs:
            if score > 0.3:
                new_context = context + [fact]
                if len(str(new_context).split()) < 2300:
                    context = new_context
                else:
                    break
            else:
                break

        formatted_context = "\n".join(context)
        return formatted_context

    def run(self, question: str) -> str:
        """Retrieve context for a question based on a graph facts."""
        embed_question = self.similarity_model.encode(question)
        scores = util.cos_sim(embed_question, self.embed_facts)[0].cpu().tolist()
        fact_score_pairs = list(zip(scores, self.facts))
        fact_score_pairs = sorted(fact_score_pairs, key=lambda x: x[0], reverse=True)
        context = self._extract_relevant_facts(fact_score_pairs)
        return context
