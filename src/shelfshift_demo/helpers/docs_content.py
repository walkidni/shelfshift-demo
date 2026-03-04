"""Documentation content loading and navigation helpers."""

from dataclasses import dataclass
from pathlib import Path
import re

import bleach
from markdown import Markdown
from markupsafe import Markup
from .docs_runtime import extract_markdown_code_cells


@dataclass(frozen=True)
class DocsPage:
    slug: str
    title: str
    filename: str


@dataclass(frozen=True)
class DocsSection:
    key: str
    title: str
    base_path: str
    source_index: str
    pages: tuple[DocsPage, ...]


_CONTENT_ROOT = Path(__file__).resolve().parents[1] / "content"

_ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS).union(
    {
        "p",
        "pre",
        "code",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "div",
        "span",
    }
)
_ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title", "rel"],
    "pre": ["class"],
    "code": ["class"],
    "th": ["align"],
    "td": ["align"],
    "div": ["class", "id"],
    "span": ["class", "id"],
    "h1": ["id"],
    "h2": ["id"],
    "h3": ["id"],
    "h4": ["id"],
    "h5": ["id"],
    "h6": ["id"],
}
_ALLOWED_PROTOCOLS = list(bleach.sanitizer.ALLOWED_PROTOCOLS) + ["mailto"]
_BASH_FENCE_PATTERN = re.compile(r"```bash[^\n]*\n(.*?)\n```", re.DOTALL)
_HEREDOC_START_PATTERN = re.compile(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?")
_NAV_LINE_PATTERN = re.compile(
    r"(?m)^\s*(?:"
    r"Previous:\s*\[[^\]]+\]\([^)]+\)(?:\s*\|\s*Next:\s*\[[^\]]+\]\([^)]+\))?"
    r"|Next:\s*\[[^\]]+\]\([^)]+\)"
    r")\s*$"
)

_SECTIONS: dict[str, DocsSection] = {
    "library": DocsSection(
        key="library",
        title="Shelfshift Library Documentation",
        base_path="/library",
        source_index="shelfshift/guides/library/INDEX.md",
        pages=(
            DocsPage(slug="index", title="Overview", filename="INDEX.md"),
            DocsPage(slug="getting-started", title="Getting Started", filename="GETTING_STARTED.md"),
            DocsPage(slug="core-concepts", title="Core Concepts", filename="CORE_CONCEPTS.md"),
            DocsPage(slug="api-reference", title="API Reference", filename="API_REFERENCE.md"),
            DocsPage(slug="canonical-model", title="Canonical Model", filename="CANONICAL_MODEL.md"),
            DocsPage(slug="advanced-usage", title="Advanced Usage", filename="ADVANCED_USAGE.md"),
        ),
    ),
    "cli": DocsSection(
        key="cli",
        title="Shelfshift CLI Documentation",
        base_path="/cli",
        source_index="shelfshift/guides/cli/INDEX.md",
        pages=(
            DocsPage(slug="index", title="Overview", filename="INDEX.md"),
            DocsPage(slug="getting-started", title="CLI Getting Started", filename="GETTING_STARTED.md"),
            DocsPage(slug="core-concepts", title="CLI Core Concepts", filename="CORE_CONCEPTS.md"),
            DocsPage(slug="command-reference", title="CLI Command Reference", filename="COMMAND_REFERENCE.md"),
            DocsPage(slug="advanced-usage", title="CLI Advanced Usage", filename="ADVANCED_USAGE.md"),
        ),
    ),
}


def get_docs_section(section_key: str) -> DocsSection:
    try:
        return _SECTIONS[section_key]
    except KeyError as exc:  # pragma: no cover - guarded by route definitions.
        raise ValueError(f"Unknown docs section: {section_key}") from exc


def get_docs_page(section: DocsSection, slug: str | None) -> DocsPage:
    target_slug = (slug or "index").strip().lower()
    for page in section.pages:
        if page.slug == target_slug:
            return page
    raise FileNotFoundError(f"Unknown docs slug: {target_slug}")


def get_docs_neighbors(section: DocsSection, current_page: DocsPage) -> tuple[DocsPage | None, DocsPage | None]:
    index = section.pages.index(current_page)
    prev_page = section.pages[index - 1] if index > 0 else None
    next_page = section.pages[index + 1] if index + 1 < len(section.pages) else None
    return prev_page, next_page


def load_docs_markdown(section: DocsSection, page: DocsPage) -> str:
    file_path = _CONTENT_ROOT / section.key / page.filename
    return file_path.read_text(encoding="utf-8")


def render_docs_html(section: DocsSection, markdown_text: str) -> tuple[Markup, Markup, list[dict[str, str]]]:
    normalized = _rewrite_local_links(section, markdown_text)
    normalized = _strip_embedded_navigation(normalized)
    normalized = _rewrite_bash_fences_as_console_sessions(normalized)
    docs_code_cells = extract_markdown_code_cells(normalized)
    parser = Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "sane_lists",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "use_pygments": True,
                "css_class": "codehilite",
            }
        },
    )
    html = parser.convert(normalized)
    toc = getattr(parser, "toc", "")
    safe_html = bleach.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True,
    )
    safe_toc = bleach.clean(
        toc,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True,
    )
    return Markup(safe_html), Markup(safe_toc), docs_code_cells


def _rewrite_local_links(section: DocsSection, text: str) -> str:
    rewritten = text
    rewritten = rewritten.replace("(./INDEX.md)", f"({section.base_path})")
    for page in section.pages:
        target = section.base_path if page.slug == "index" else f"{section.base_path}/{page.slug}"
        rewritten = rewritten.replace(f"(./{page.filename})", f"({target})")

    # Drop horizontal separators used as markdown file boundaries in source docs.
    rewritten = re.sub(r"\n---\n", "\n\n", rewritten)
    return rewritten


def _strip_embedded_navigation(text: str) -> str:
    stripped = _NAV_LINE_PATTERN.sub("", text)
    # Collapse excessive blank lines introduced after removing nav lines.
    return re.sub(r"\n{3,}", "\n\n", stripped).strip()


def _rewrite_bash_fences_as_console_sessions(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        block = match.group(1)
        session = _bash_script_to_console_session(block)
        return f"```console\n{session}\n```"

    return _BASH_FENCE_PATTERN.sub(_replace, text)


def _bash_script_to_console_session(block: str) -> str:
    lines = block.splitlines()
    rewritten_lines: list[str] = []
    heredoc_marker: str | None = None

    for line in lines:
        if not line.strip():
            rewritten_lines.append("")
            continue

        if heredoc_marker is not None:
            rewritten_lines.append(f"> {line}")
            if line.strip() == heredoc_marker:
                heredoc_marker = None
            continue

        rewritten_lines.append(f"$ {line}")
        heredoc_match = _HEREDOC_START_PATTERN.search(line)
        if heredoc_match is not None:
            heredoc_marker = heredoc_match.group(1)

    return "\n".join(rewritten_lines)
