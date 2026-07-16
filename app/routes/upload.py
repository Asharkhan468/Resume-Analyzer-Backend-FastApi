from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.pdf_loader import load_pdf
from app.utils.chunking import split_documents
from app.services.rag_service import store_chunks

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    # Only PDF files allowed
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save PDF
    file_path = DOCUMENTS_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Load PDF
    documents = load_pdf(str(file_path))

    # Split into chunks
    chunks = split_documents(documents)

    # Store in ChromaDB
    store_chunks(chunks)

    return {
        "success": True,
        "message": "PDF uploaded successfully.",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }