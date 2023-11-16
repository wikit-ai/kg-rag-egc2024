# Graph Construction

To use the demonstrator, you should have a graph instance running.

In this work, only specific parts of the SustainGraph are built.
The entire project is available [here](https://gitlab.com/netmode/sustaingraph).

A running Neo4j instance is needed.

Environment variables must be set :

```sh
export GRAPH_URI=<GRAPH_URI>
export GRAPH_USER=<GRAPH_USER>
export GRAPH_PASSWORD=<GRAPH_PASSWORD>
```

Then, the graph construction script can be run to construct specific parts of the SustainGraph :

```sh
cd kg-rag-egc2024/graph_construction
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 graph_construction.py
```
