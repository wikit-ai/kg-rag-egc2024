from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from entity_linking_openai.service import ELOpenAI
from fastapi import APIRouter, Body, Depends, Header, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from wikit.schema import WikitBotApiResponse, WikitBotMessage

entity_linking_openai_router = APIRouter(
    prefix="/api",
    tags=["Entity linking", "OpenAI"]
)

@entity_linking_openai_router.post("/entity-linking-openai/invoke")
@inject
async def invoke(
    utterance: str = Body(title="User utterance", embed=True),
    el_openai_service: ELOpenAI = Depends(
        Provide[ApplicationContainer.el_openai_service]
    ),
    x_wikit_response_format: str = Header(
        title="Response format",
        description="The response format can be Wikit Bot JSON (`wikit`) or default JSON (`json`)",
        default="json",
        regex="(json|wikit)"
    )
):
    """Invoke chain with entity linking and OpenAI"""

    model_output = el_openai_service.run(utterance)

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
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(model_output)
    )

