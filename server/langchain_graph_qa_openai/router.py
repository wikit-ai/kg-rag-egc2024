from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from langchain_graph_qa_openai.service import LangChainGraphQA
from fastapi import APIRouter, Body, Header, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from wikit.schema import WikitBotApiResponse, WikitBotMessage

langchain_graph_qa_openai_router = APIRouter(
    prefix="/api", tags=["LangChain", "OpenAI"]
)


@langchain_graph_qa_openai_router.post("/langchain-graph-qa-openai/invoke")
@inject
async def invoke(
    utterance: str = Body(title="User utterance", embed=True),
    x_wikit_response_format: str = Header(
        title="Response format",
        description="The response format can be Wikit Bot JSON (`wikit`) or default JSON (`json`)",
        default="json",
        regex="(json|wikit)"
    ),
    langchain_graphqa_service: LangChainGraphQA = Depends(
        Provide[ApplicationContainer.langchain_graphqa_service]
    ),
):
    """Invoke chain with LangChain graph cypher QA and OpenAI model."""
    model_output = langchain_graphqa_service.run(utterance)

    if x_wikit_response_format == "wikit":
        wikit_response = WikitBotApiResponse(
            messages=[
                WikitBotMessage(replies=[model_output.answer])
            ]
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(wikit_response)
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(model_output)
    )
