from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

rag_sbert_openai_router = APIRouter(
    prefix="/api",
    tags=["RAG", "SentenceTransformers", "OpenAI"]
)

@rag_sbert_openai_router.post("/rag-sbert-openai/invoke")
async def invoke():
    """Invoke chain with Retrieval-Augmented Generation, SentenceTransformers and OpenAI"""

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "TODO"
        }
    )
