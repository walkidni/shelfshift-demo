"""Product import helpers (URL and CSV)."""


import json
import logging

from fastapi import HTTPException
import requests

from shelfshift.core.canonical.entities import Product
from shelfshift.core.detect import detect_product_url
from shelfshift.core.importers.csv import import_product_from_csv, import_products_from_csv
from shelfshift.core.importers.url import import_product_from_url

from ..config import Settings
from ..logging import product_result_to_loggable

logger = logging.getLogger("uvicorn.error")


def normalize_url(product_url: str) -> str:
    normalized = (product_url or "").strip()
    if not normalized:
        raise HTTPException(status_code=400, detail="product_url is required")
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized}"

    info = detect_product_url(normalized)
    if not info.get("platform"):
        raise HTTPException(
            status_code=422,
            detail="Unsupported URL. Supported URL detection sources: Shopify, WooCommerce, Squarespace, Amazon, AliExpress.",
        )
    return normalized


def run_import_product(product_url: str, *, settings: Settings) -> Product:
    normalized_url = normalize_url(product_url)

    try:
        product = import_product_from_url(normalized_url)
        logger.debug(
            "Imported product summary:\n%s",
            json.dumps(
                product_result_to_loggable(
                    product,
                    verbosity=settings.log_verbosity,
                    debug_enabled=settings.debug,
                ),
                ensure_ascii=False,
                indent=2,
            ),
        )
        return product
    except requests.HTTPError as exc:
        status = getattr(exc.response, "status_code", 502) or 502
        text = getattr(exc.response, "text", str(exc))
        raise HTTPException(status_code=status, detail=f"Upstream provider error: {text}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal import error: {exc}") from exc


def run_import_products(
    urls: list[str],
    *,
    settings: Settings,
) -> tuple[list[Product], list[dict[str, str]]]:
    """Import multiple URLs with partial-success semantics.

    Returns (products, errors) where *errors* is a list of
    ``{"url": ..., "detail": ...}`` dicts for URLs that failed.
    """
    products: list[Product] = []
    errors: list[dict[str, str]] = []
    for url in urls:
        try:
            products.append(run_import_product(url, settings=settings))
        except HTTPException as exc:
            errors.append({"url": url, "detail": exc.detail})
    return products, errors


def run_import_csv_product(
    *,
    source_platform: str,
    csv_bytes: bytes,
    source_weight_unit: str | None,
) -> Product:
    try:
        product = import_product_from_csv(
            source_platform=source_platform,
            csv_bytes=csv_bytes,
            source_weight_unit=source_weight_unit,
        )
        logger.debug(
            "Imported CSV product summary:\n%s",
            json.dumps(product_result_to_loggable(product), ensure_ascii=False, indent=2),
        )
        return product
    except ValueError as exc:
        detail = str(exc)
        if "exceeds 5 MB" in detail:
            raise HTTPException(status_code=413, detail=detail) from exc
        raise HTTPException(status_code=422, detail=detail) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal CSV import error: {exc}") from exc


def run_import_csv_products(
    *,
    source_platform: str,
    csv_bytes: bytes,
    source_weight_unit: str | None,
) -> list[Product]:
    try:
        products = import_products_from_csv(
            source_platform=source_platform,
            csv_bytes=csv_bytes,
            source_weight_unit=source_weight_unit,
        )
        logger.debug(
            "Imported %d CSV product(s) (batch).",
            len(products),
        )
        return products
    except ValueError as exc:
        detail = str(exc)
        if "exceeds 5 MB" in detail:
            raise HTTPException(status_code=413, detail=detail) from exc
        raise HTTPException(status_code=422, detail=detail) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal CSV import error: {exc}") from exc
