"""Server-only canonical payload serializers."""

from typing import Any

from shelfshift.core.canonical.entities import Product


def serialize_product_for_api(product: Product, *, include_raw: bool) -> dict[str, Any]:
    payload = product.to_dict()
    if include_raw:
        raw_payload = product.provenance.get("raw")
        if raw_payload is not None:
            payload["raw"] = raw_payload
    return payload


__all__ = ["serialize_product_for_api"]
