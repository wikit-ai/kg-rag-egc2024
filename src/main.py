import os
import uvicorn
from fastapi import FastAPI

from containers import ApplicationContainer
from entity_linking_mistralai.router import entity_linking_mistralai_router
from entity_linking_openai.router import entity_linking_openai_router
from langchain_custom_openai.router import langchain_custom_openai_router
from langchain_graph_qa_openai.router import langchain_graph_qa_openai_router
from rag_sbert_openai.router import rag_sbert_openai_router

app = FastAPI(
    title="Wikit Demo for EGC 2024",
    version="1.0",
    description=(
        "This API server exposes REST endpoints for the EGC 2024 demo by Wikit R&D."
    ),
)

app.containers = ApplicationContainer()

app.include_router(entity_linking_mistralai_router)
app.include_router(entity_linking_openai_router)
app.include_router(langchain_custom_openai_router)
app.include_router(langchain_graph_qa_openai_router)
app.include_router(rag_sbert_openai_router)


@app.get("/health")
async def health():
    return {"status": "OK"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3008))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
