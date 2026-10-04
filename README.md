# AI-Document-QA-API

Minimal backend foundation for document ingestion:

- PDF input upload endpoint built with FastAPI
- Text extraction from uploaded PDFs
- PostgreSQL storage of extracted text

## Run locally

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://postgres@localhost:5432/document_qa"
uvicorn app.main:app --reload
```

## API

- `POST /documents/upload` (multipart form with `file` as a PDF)
