# AI-Document-QA-API

Minimal backend foundation for document ingestion:

- PDF input upload endpoint built with FastAPI
- Text extraction from uploaded PDFs
- PostgreSQL storage of extracted text

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The default local configuration uses SQLite and creates `document_qa.db` in the
project directory, so PostgreSQL is not required for development. To use
PostgreSQL instead, set `DATABASE_URL` to a URL containing the password for the
local `postgres` role before starting the API:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:<password>@localhost:5432/document_qa"
uvicorn app.main:app --reload
```

## API

- `POST /documents/upload` (multipart form with `file` as a PDF)
