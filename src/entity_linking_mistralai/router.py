from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

entity_linking_mistralai_router = APIRouter(
    prefix="/api",
    tags=["Entity linking", "Mistral AI"]
)

@entity_linking_mistralai_router.post("/entity-linking-mistralai/invoke")
async def invoke():
    """Invoke chain with entity linking and Mistral AI"""

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "TODO"
        }
    )
