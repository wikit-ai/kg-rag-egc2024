from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from langchain_graph_qa_openai.service import LangChainGraphQA
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

langchain_graph_qa_openai_router = APIRouter(
    prefix="/api", tags=["LangChain", "OpenAI"]
)


@langchain_graph_qa_openai_router.post("/langchain-graph-qa-openai/invoke")
@inject
async def invoke(
    utterance: str,
    langchain_graphqa_service: LangChainGraphQA = Depends(
        Provide[ApplicationContainer.langchain_graphqa_service]
    ),
):
    """Invoke chain with LangChain graph cypher QA and OpenAI model."""
    model_output = langchain_graphqa_service.run(utterance)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(model_output)
    )
