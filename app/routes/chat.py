from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag_service import retrieve_chunks
from app.services.llm_service import get_llm
from app.prompts.system_prompt import SYSTEM_PROMPT

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

llm = get_llm()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    chunks = retrieve_chunks(request.question)

    context = "\n\n".join(chunks)

    prompt = f"""
    {SYSTEM_PROMPT}

    Context:
        {context}

        Question:
            {request.question}
            """

    response = llm.invoke(prompt)

    return ChatResponse(
answer=response.content
)