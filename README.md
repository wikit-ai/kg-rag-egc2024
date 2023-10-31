# EGC 2024

[EGC 2024](https://iutdijon.u-bourgogne.fr/egc2024/) is the 24th French-speaking conference on Knowledge Extraction and Management. EGC stands for _"Extraction et la Gestion des Connaissances"_ 🇫🇷

The conference will take place in Dijon, France from January 22nd to 26th, 2024.

This repo contains the code related to the [Call for Demonstrations](https://iutdijon.u-bourgogne.fr/egc2024/demonstrations/).

## Demonstration overview

Given a question in natural language, we want to extract the knowledge from the graph that can be used to answer it, and then generate an answer based on this knowledge.

5 different techniques to do knowledge graph-based retrieval augmented generation are available :

- _langchain_graph_qa_openai_ uses the _LangChain_ tool to generate a Cypher query based on the user's utterance and then uses the knowledge extracted from the graph with the query to generate an answer to the question with OpenAI model.
- _langchain_custom_openai_ is the same as _langchain_graph_qa_openai_ but with custom prompts and a custom graph schema definition.
- _rag_bert_openai_ uses semantic similarity between the content of the graph and the user's utterance to extract the relevant knowledge used to generate an answer with OpenAI model.
- _entity_linking_openai_ uses entity linking and query patterns to extract knowledge from the graph and then generate an answer to the question based on this knowledge with OpenAI model.
- _entity_linking_mistral_ is the same as _entity_linking_openai_ but with Mistral model.

## Graph construction

Information for building the graph used in the demonstrators is available in the _graph_construction_ folder.

## Dataset

The questions used to evaluate the different methods are listed in the file _sdg_questions.csv_ in the _dataset_ folder.

## References

> Fotopoulou E, Mandilara I, Zafeiropoulos A, Laspidou C, Adamos G, Koundouri P and Papavassiliou S (2022) SustainGraph: A knowledge graph for tracking the progress and the interlinking among the sustainable development goals’ targets. Front. Environ. Sci. 10:1003599. doi: 10.3389/fenvs.2022.1003599
