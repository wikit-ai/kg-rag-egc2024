from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

langchain_graph_qa_openai_router = APIRouter(
    prefix="/api",
    tags=["LangChain", "OpenAI"]
)

@langchain_graph_qa_openai_router.post("/langchain-graph-qa-openai/invoke")
async def invoke():
    """Invoke chain with LangChain graph cypher QA and OpenAI"""

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "TODO"
        }
    )
