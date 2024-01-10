FROM python:3.10.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

ENV GRAPH_URI "bolt://xxxxxxxxxxxxxxxxxxx"

ENV GRAPH_USER "neo4j"

ENV GRAPH_PASSWORD "password"

ENV OPENAI_API_KEY "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

ENV OPENAI_ORG = "org-xxxxxxxxxxxx"

ENV MISTRAL_API_KEY "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]