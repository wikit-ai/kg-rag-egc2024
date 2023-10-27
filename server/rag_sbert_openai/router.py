from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from fastapi import APIRouter, Body, Depends, Header, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from rag_sbert_openai.service import RagSBertOpenAI
from wikit.schema import WikitBotApiResponse, WikitBotMessage

rag_sbert_openai_router = APIRouter(
    prefix="/api",
    tags=["RAG", "SentenceTransformers", "OpenAI"]
)

@rag_sbert_openai_router.post("/rag-sbert-openai/invoke")
@inject
async def invoke(
    utterance: str = Body(title="User utterance", embed=True),
    rag_sbert_openai_service: RagSBertOpenAI = Depends(
        Provide[ApplicationContainer.rag_sbert_openai_service]
    ),
    x_wikit_response_format: str = Header(
        title="Response format",
        description="The response format can be Wikit Bot JSON (`wikit`) or default JSON (`json`)",
        default="json",
        regex="(json|wikit)"
    )
):
    """Invoke chain with Retrieval-Augmented Generation, SentenceTransformers and OpenAI"""

    model_output = rag_sbert_openai_service.run(utterance)

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