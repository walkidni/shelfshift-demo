from fastapi.testclient import TestClient

from shelfshift_demo.main import app


client = TestClient(app)


def test_docs_run_cell_endpoint_executes_python() -> None:
    response = client.post(
        "/api/v1/docs/run-cell",
        json={"code": "n = 3\nn * 2", "language": "python"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert payload["result"] == "6"
    assert payload["session_id"]


def test_library_docs_page_includes_code_cells_payload() -> None:
    response = client.get("/library/advanced-usage")
    assert response.status_code == 200
    assert 'id="docs-code-cells"' in response.text

