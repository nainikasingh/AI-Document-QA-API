import importlib

from fastapi.testclient import TestClient


def sample_pdf_bytes() -> bytes:
    return b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 44 >>
stream
BT
/F1 24 Tf
72 100 Td
(Hello PDF) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000010 00000 n
0000000060 00000 n
0000000117 00000 n
0000000243 00000 n
0000000313 00000 n
trailer
<< /Root 1 0 R /Size 6 >>
startxref
407
%%EOF
"""


def test_upload_document_extracts_and_stores_text(monkeypatch, tmp_path):
    database_url = f"sqlite:///{tmp_path}/test.db"
    monkeypatch.setenv("DATABASE_URL", database_url)

    import app.database as database
    import app.main as main
    import app.models as models

    importlib.reload(database)
    importlib.reload(models)
    importlib.reload(main)
    main.Base.metadata.create_all(bind=database.engine)

    client = TestClient(main.app)

    response = client.post(
        "/documents/upload",
        files={"file": ("sample.pdf", sample_pdf_bytes(), "application/pdf")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "sample.pdf"
    assert "Hello PDF" in payload["extracted_text"]

    with database.SessionLocal() as db:
        persisted = db.get(models.DocumentText, payload["id"])
        assert persisted is not None
        assert "Hello PDF" in persisted.extracted_text
