# Demo API server

The demonstration is based on a FastAPI server that exposes one invocation endpoint per scenario.

## Server setup

<!-- TODO -->

```sh
export GRAPH_URI=<GRAPH_URI>
export GRAPH_USER=<GRAPH_USER>
export GRAPH_PASSWORD=<GRAPH_PASSWORD>

export MISTRAL_API_KEY=<MISTRAL_API_KEY>

export OPENAI_API_KEY=<OPENAI_API_KEY>
export OPENAI_ORG=<OPENAI_ORG>
```

```sh
cd wikit-egc2024/server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```
