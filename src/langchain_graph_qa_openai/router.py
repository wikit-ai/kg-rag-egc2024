from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from langchain_graph_qa_openai.service import LangChainGraphQA
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

langchain_graph_qa_openai_router = APIRouter(
    prefix="/api", tags=["LangChain", "OpenAI"]
)


@langchain_graph_qa_openai_router.post("/langchain-graph-qa-openai/invoke")
@inject
async def invoke(
    langchain_graphqa_service: LangChainGraphQA = Depends(
        Provide[ApplicationContainer.langchain_graphqa_service]
    ),
):
    """Invoke chain with LangChain graph cypher QA and OpenAI"""
    res = langchain_graphqa_service.run("What is the SDG 1 ?")

    return JSONResponse(status_code=status.HTTP_200_OK, content=res)
