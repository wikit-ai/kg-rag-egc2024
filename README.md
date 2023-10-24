# EGC 2024

[EGC 2024](https://iutdijon.u-bourgogne.fr/egc2024/) is the 24th French-speaking conference on Knowledge Extraction and Management. EGC stands for *"Extraction et la Gestion des Connaissances"* 🇫🇷

The conference will take place in Dijon, France from January 22nd to 26th, 2024.

This repo contains the code related to the [Call for Demonstrations](https://iutdijon.u-bourgogne.fr/egc2024/demonstrations/).

## Demonstration overview

<!-- TODO -->

## Demonstration setup

<!-- TODO -->

```sh
source .venv/bin/activate

cd src
pip install -r requirements.txt

uvicorn main:app --reload
```

## Graph Construction

To use the demonstrator, you should have a graph instance running. 

In this work, only specific parts of the SustainGraph are built.
The entire project is available here [https://gitlab.com/netmode/sustaingraph](https://gitlab.com/netmode/sustaingraph).

A running Neo4j instance is needed.

Environment variables must be set : 

```sh
export GRAPH_URI=<GRAPH_URI>
export GRAPH_USER=<GRAPH_USER>
export GRAPH_PASSWORD=<GRAPH_PASSWORD>
```

Then, the graph construction script can be run to construct specific parts of the SustainGraph : 

```sh
python3 graph_construction/graph_construction.py
```

## References

> Fotopoulou E, Mandilara I, Zafeiropoulos A, Laspidou C, Adamos G, Koundouri P and Papavassiliou S (2022) SustainGraph: A knowledge graph for tracking the progress and the interlinking among the sustainable development goals’ targets. Front. Environ. Sci. 10:1003599. doi: 10.3389/fenvs.2022.1003599