import io
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import DocumentText

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Document QA API", lifespan=lifespan)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    extracted_chunks: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            extracted_chunks.append(page_text)
    return "\n".join(extracted_chunks).strip()


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename and file.filename.lower().endswith(".pdf")):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    try:
        extracted_text = extract_text_from_pdf(pdf_bytes)
    except Exception as exc:  # pragma: no cover - defensive parse protection
        raise HTTPException(status_code=400, detail="Invalid or unreadable PDF.") from exc

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No extractable text found in PDF.")

    document = DocumentText(filename=file.filename, extracted_text=extracted_text)
    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename,
        "extracted_text": document.extracted_text,
    }
