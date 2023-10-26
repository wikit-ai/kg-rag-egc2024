from fastapi import APIRouter, Body, Header, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from wikit.schema import WikitBotApiResponse, WikitBotMessage

rag_sbert_openai_router = APIRouter(
    prefix="/api",
    tags=["RAG", "SentenceTransformers", "OpenAI"]
)

@rag_sbert_openai_router.post("/rag-sbert-openai/invoke")
async def invoke(
    utterance: str = Body(title="User utterance", embed=True),
    x_wikit_response_format: str = Header(
        title="Response format",
        description="The response format can be Wikit Bot JSON (`wikit`) or default JSON (`json`)",
        default="json",
        regex="(json|wikit)"
    )
):
    """Invoke chain with Retrieval-Augmented Generation, SentenceTransformers and OpenAI"""

    # TODO Call service to get the output

    if x_wikit_response_format == "wikit":
        wikit_response = WikitBotApiResponse(
            messages=[
                WikitBotMessage(replies=["TODO"]), # TODO Construct bot message with answer from the output
            ]
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(wikit_response)
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "status": "TODO"  # TODO Send the output
        })
    )