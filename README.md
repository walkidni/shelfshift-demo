# ShelfShift Demo

FastAPI demo application for the [`shelfshift`](https://pypi.org/project/shelfshift/) library.

It provides:

- a web UI for URL/CSV import and CSV export flows
- JSON API endpoints for detection, import, and export
- canonical payload round-trips using `shelfshift.core`

## Requirements

- Python `>=3.11`
- [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
uv sync --all-groups
uv run shelfshift-demo
```

App runs on `http://localhost:8000`.

## Configuration

Copy and edit environment values:

```bash
cp .env.example .env
```

Supported env vars:

- `APP_NAME`
- `APP_TAGLINE`
- `BRAND_PRIMARY`
- `BRAND_SECONDARY`
- `BRAND_INK`
- `DEBUG`
- `LOG_VERBOSITY` (`low|medium|high|extrahigh`)
- `RAPIDAPI_KEY`
- `CORS_ALLOW_ORIGINS` (comma-separated)

## Main Routes

### Web

- `GET /` landing page
- `GET /url` URL import page
- `GET /csv` CSV import page

### API

- `GET /health`
- `GET /api/v1/detect`
- `POST /api/v1/detect/csv`
- `POST /api/v1/import`
- `POST /api/v1/import/csv`
- `POST /api/v1/export/from-product.csv`
- `POST /api/v1/export/{shopify|bigcommerce|wix|squarespace|woocommerce}.csv`

## Development

Run tests:

```bash
uv run pytest -q
```

Run lint:

```bash
uv run ruff check .
```

Run type checks:

```bash
uv run ty check src/
```

## Deploy To Vercel

This repository is prepared for Vercel's Python runtime with a root entrypoint:

- `app.py` exports `app` (FastAPI instance)

Deploy with Vercel CLI:

```bash
vercel deploy -y
```

## Project Layout

```text
app.py
src/shelfshift_demo/
  config.py
  main.py
  helpers/
  logging/
  routers/
  web/
tests/
fixtures/exporter/
```
