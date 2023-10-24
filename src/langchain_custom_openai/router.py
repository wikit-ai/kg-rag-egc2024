from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

langchain_custom_openai_router = APIRouter(
    prefix="/api",
    tags=["LangChain", "OpenAI"]
)

@langchain_custom_openai_router.post("/langchain-custom-openai/invoke")
async def invoke():
    """Invoke chain with LangChain and OpenAI"""

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "TODO"
        }
    )
