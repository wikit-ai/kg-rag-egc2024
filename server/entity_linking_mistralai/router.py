from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from entity_linking_mistralai.service import ELMistral
from fastapi import APIRouter, Body, Depends, Header, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from wikit.schema import WikitBotApiResponse, WikitBotMessage


entity_linking_mistralai_router = APIRouter(
    prefix="/api", tags=["Entity linking", "Mistral AI"]
)


@entity_linking_mistralai_router.post("/entity-linking-mistralai/invoke")
@inject
async def invoke(
    utterance: str = Body(title="User utterance", embed=True),
    el_mistralai_service: ELMistral = Depends(
        Provide[ApplicationContainer.el_mistralai_service]
    ),
    x_wikit_response_format: str = Header(
        title="Response format",
        description="The response format can be Wikit Bot JSON (`wikit`) or default JSON (`json`)",
        default="json",
        regex="(json|wikit)"
    )
):
    """Invoke chain with entity linking and Mistral AI"""
    model_output = el_mistralai_service.run(utterance)

    if x_wikit_response_format == "wikit":
        wikit_response = WikitBotApiResponse(
            messages=[
                WikitBotMessage(replies=[model_output.answer]),
            ]
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(wikit_response)
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(model_output)
    )
