from shelfshift_demo.helpers.docs_runtime import (
    execute_docs_cell,
    extract_markdown_code_cells,
)


def test_extract_markdown_code_cells_preserves_order_and_content() -> None:
    markdown = """
# Demo

```python
value = 2 + 2
value
```

```bash
echo "hello"
```
"""
    cells = extract_markdown_code_cells(markdown)
    assert [cell["language"] for cell in cells] == ["python", "bash"]
    assert cells[0]["code"] == 'value = 2 + 2\nvalue'
    assert cells[1]["code"] == 'echo "hello"'


def test_execute_docs_cell_python_keeps_session_state() -> None:
    first = execute_docs_cell("x = 5", language="python", session_id=None)
    assert first["ok"] is True
    assert first["session_id"]

    second = execute_docs_cell("x + 7", language="python", session_id=first["session_id"])
    assert second["ok"] is True
    assert second["result"] == "12"


def test_execute_docs_cell_console_runs_prompt_lines() -> None:
    result = execute_docs_cell("$ echo shell-ok", language="console", session_id=None)
    assert result["ok"] is True
    assert "shell-ok" in result["stdout"]


def test_execute_docs_cell_json_formats_payload() -> None:
    result = execute_docs_cell('{"b":2,"a":1}', language="json", session_id=None)
    assert result["ok"] is True
    assert result["stdout"] == '{\n  "a": 1,\n  "b": 2\n}\n'

