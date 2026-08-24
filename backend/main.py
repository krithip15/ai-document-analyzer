from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pdf_processor import extract_text
from chunker import create_chunks
from vector_store import add_chunks, search_chunks
from rag import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


@app.get("/")
def root():
    return {"message": "DocuMind API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # 1. Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # 2. Read the uploaded file
    file_data = await file.read()

    # 3. Check file size
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File size must be less than 20 MB."
        )

    # 4. Make sure the file isn't empty
    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    # 5. Reset file position so PyPDF can read it
    from io import BytesIO

    pdf_file = BytesIO(file_data)

    try:
        # 6. Extract text from PDF
        pages = extract_text(pdf_file)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the PDF. It may be corrupted or encrypted.",
        )

    # 7. Check whether text was extracted
    if not pages or not any(page["text"].strip() for page in pages):
        raise HTTPException(
            status_code=400, detail="No readable text was found in this PDF."
        )

    # 8. Create chunks
    chunks = create_chunks(pages)

    if not chunks:
        raise HTTPException(
            status_code=400, detail="Could not create text chunks from this document."
        )

    # 9. Store embeddings in ChromaDB
    stored_chunks = add_chunks(chunks, file.filename)

    return {"filename": file.filename, "pages": len(pages), "chunks": stored_chunks}


class SearchRequest(BaseModel):
    query: str
    filename: str


@app.post("/search")
def search_document(request: SearchRequest):

    results = search_chunks(request.query, request.filename)

    return results


class QuestionRequest(BaseModel):
    question: str
    filename: str


@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if not request.filename.strip():
        raise HTTPException(status_code=400, detail="Filename is required.")

    return generate_answer(request.question, request.filename)
