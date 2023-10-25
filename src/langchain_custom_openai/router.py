from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from langchain_custom_openai.service import LangChainCustom
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

langchain_custom_openai_router = APIRouter(
    prefix="/api", tags=["LangChain", "OpenAI"]
)


@langchain_custom_openai_router.post("/langchain-custom-openai/invoke")
@inject
async def invoke(
    utterance: str,
    langchain_custom_service: LangChainCustom = Depends(
        Provide[ApplicationContainer.langchain_custom_service]
    ),
):
    """Invoke chain with LangChain graph cypher QA and OpenAI model with custom prompt."""
    model_output = langchain_custom_service.run(utterance)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(model_output)
    )
