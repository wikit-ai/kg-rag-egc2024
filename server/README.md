# Demo API server

The demonstration is based on a FastAPI server that exposes one invocation endpoint per scenario.

## Server setup

<!-- TODO -->

```sh
export GRAPH_URI=<GRAPH_URI>
export GRAPH_USER=<GRAPH_USER>
export GRAPH_PASSWORD=<GRAPH_PASSWORD>

export MISTRAL_API_URL=https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1
export HF_TOKEN=<HF_TOKEN>

export OPENAI_API_KEY=<OPENAI_API_KEY>
```

```sh
cd wikit-egc2024/server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```
