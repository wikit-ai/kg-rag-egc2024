from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

entity_linking_openai_router = APIRouter(
    prefix="/api",
    tags=["Entity linking", "OpenAI"]
)

@entity_linking_openai_router.post("/entity-linking-openai/invoke")
async def invoke():
    """Invoke chain with entity linking and OpenAI"""

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "TODO"
        }
    )
