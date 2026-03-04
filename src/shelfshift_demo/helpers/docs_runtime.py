"""Notebook-style execution helpers for documentation code blocks."""

from __future__ import annotations

import ast
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
import io
import json
from pathlib import Path
import re
import secrets
import subprocess
import threading
import time
import traceback
from typing import Any

_CODE_FENCE_PATTERN = re.compile(r"```([A-Za-z0-9_-]*)[^\n]*\n(.*?)\n```", re.DOTALL)
_SESSION_LOCK = threading.Lock()
_MAX_SESSIONS = 64
_SESSION_TTL_SECONDS = 30 * 60
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_BLOCKED_SHELL_TOKENS = (
    " rm -",
    "sudo ",
    "apt ",
    "apt-get ",
    "dnf ",
    "yum ",
    "pip install",
    "uv pip",
    "npm install",
)


def extract_markdown_code_cells(markdown_text: str) -> list[dict[str, str]]:
    """Extract fenced code blocks from markdown in source order."""
    cells: list[dict[str, str]] = []
    for match in _CODE_FENCE_PATTERN.finditer(markdown_text):
        language = (match.group(1) or "").strip().lower() or "text"
        code = match.group(2)
        cells.append({"language": language, "code": code})
    return cells


@dataclass
class _PythonSession:
    namespace: dict[str, Any] = field(default_factory=lambda: {"__name__": "__docs_cell__"})
    last_used: float = field(default_factory=time.time)
    execution_count: int = 0


_PYTHON_SESSIONS: dict[str, _PythonSession] = {}


def execute_docs_cell(code: str, *, language: str, session_id: str | None) -> dict[str, Any]:
    """Execute a docs code cell and return structured output."""
    normalized_language = _normalize_language(language)
    source = str(code or "")

    if normalized_language == "python":
        resolved_session_id, session = _get_or_create_python_session(session_id)
        result = _run_python_cell(source, session)
        result["session_id"] = resolved_session_id
        result["language"] = normalized_language
        return result

    if normalized_language in {"bash", "shell", "console"}:
        script = _console_script_to_shell(source) if normalized_language == "console" else source
        return {
            "language": normalized_language,
            "session_id": session_id,
            **_run_shell_cell(script),
        }

    if normalized_language == "json":
        return {
            "language": normalized_language,
            "session_id": session_id,
            **_run_json_cell(source),
        }

    return {
        "ok": False,
        "stdout": "",
        "stderr": f"Execution is not supported for language '{normalized_language}'.",
        "result": None,
        "exit_code": None,
        "language": normalized_language,
        "session_id": session_id,
    }


def _normalize_language(language: str | None) -> str:
    value = str(language or "").strip().lower()
    if value in {"python", "py"}:
        return "python"
    if value in {"bash", "sh", "zsh"}:
        return "bash"
    if value in {"console", "shell", "terminal"}:
        return "console" if value == "console" else "shell"
    if value in {"json", "javascript", "js", "text"}:
        return value
    return value or "text"


def _get_or_create_python_session(session_id: str | None) -> tuple[str, _PythonSession]:
    now = time.time()
    with _SESSION_LOCK:
        _evict_stale_sessions(now)
        if session_id and session_id in _PYTHON_SESSIONS:
            session = _PYTHON_SESSIONS[session_id]
            session.last_used = now
            return session_id, session

        created_id = secrets.token_hex(8)
        session = _PythonSession()
        _PYTHON_SESSIONS[created_id] = session
        _evict_overflow()
        return created_id, session


def _evict_stale_sessions(now: float) -> None:
    stale_ids = [
        sid for sid, session in _PYTHON_SESSIONS.items()
        if (now - session.last_used) > _SESSION_TTL_SECONDS
    ]
    for sid in stale_ids:
        _PYTHON_SESSIONS.pop(sid, None)


def _evict_overflow() -> None:
    if len(_PYTHON_SESSIONS) <= _MAX_SESSIONS:
        return
    sorted_sessions = sorted(_PYTHON_SESSIONS.items(), key=lambda item: item[1].last_used)
    to_remove = len(_PYTHON_SESSIONS) - _MAX_SESSIONS
    for sid, _ in sorted_sessions[:to_remove]:
        _PYTHON_SESSIONS.pop(sid, None)


def _run_python_cell(code: str, session: _PythonSession) -> dict[str, Any]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    result_repr: str | None = None
    ok = True

    try:
        parsed = ast.parse(code, mode="exec")
        body = list(parsed.body)
        final_expr = body[-1] if body and isinstance(body[-1], ast.Expr) else None
        body_for_exec = body[:-1] if final_expr is not None else body
        module_node = ast.Module(body=body_for_exec, type_ignores=[])
        compiled_exec = compile(module_node, "<docs-cell>", "exec")

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compiled_exec, session.namespace)
            if final_expr is not None:
                compiled_expr = compile(ast.Expression(final_expr.value), "<docs-cell>", "eval")
                final_value = eval(compiled_expr, session.namespace)
                if final_value is not None:
                    result_repr = repr(final_value)
    except Exception:
        ok = False
        traceback.print_exc(file=stderr)

    session.execution_count += 1
    session.last_used = time.time()

    return {
        "ok": ok,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "result": result_repr,
        "exit_code": 0 if ok else 1,
    }


def _console_script_to_shell(code: str) -> str:
    lines = code.splitlines()
    script_lines: list[str] = []
    for line in lines:
        if line.startswith("$ "):
            script_lines.append(line[2:])
            continue
        if line.startswith("> "):
            script_lines.append(line[2:])
    if script_lines:
        return "\n".join(script_lines)
    return code


def _run_shell_cell(code: str) -> dict[str, Any]:
    safe_code = f" {code.lower()} "
    for token in _BLOCKED_SHELL_TOKENS:
        if token in safe_code:
            return {
                "ok": False,
                "stdout": "",
                "stderr": "This command type is blocked in docs runner for safety.",
                "result": None,
                "exit_code": 126,
            }

    try:
        completed = subprocess.run(
            ["bash", "-lc", code],
            cwd=str(_PROJECT_ROOT),
            text=True,
            capture_output=True,
            timeout=8,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + "\nExecution timed out after 8s.",
            "result": None,
            "exit_code": 124,
        }

    return {
        "ok": completed.returncode == 0,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "result": None,
        "exit_code": completed.returncode,
    }


def _run_json_cell(code: str) -> dict[str, Any]:
    try:
        payload = json.loads(code)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "stdout": "",
            "stderr": f"Invalid JSON: {exc}",
            "result": None,
            "exit_code": 1,
        }
    return {
        "ok": True,
        "stdout": json.dumps(payload, indent=2, sort_keys=True) + "\n",
        "stderr": "",
        "result": None,
        "exit_code": 0,
    }


__all__ = ["execute_docs_cell", "extract_markdown_code_cells"]
