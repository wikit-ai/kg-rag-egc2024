from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from entity_linking_mistralai.service import ELMistral
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

entity_linking_mistralai_router = APIRouter(
    prefix="/api", tags=["Entity linking", "Mistral AI"]
)


@entity_linking_mistralai_router.post("/entity-linking-mistralai/invoke")
@inject
async def invoke(
    utterance: str,
    el_mistralai_service: ELMistral = Depends(
        Provide[ApplicationContainer.el_mistralai_service]
    ),
):
    """Invoke chain with entity linking and Mistral AI"""
    model_output = el_mistralai_service.run(utterance)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(model_output)
    )
