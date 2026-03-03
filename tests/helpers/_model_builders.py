from __future__ import annotations

from typing import Any

from shelfshift.core.canonical import Product as CanonicalProduct
from shelfshift.core.canonical import Variant as CanonicalVariant


def _legacy_price_to_canonical(price: Any) -> dict[str, Any] | None:
    if price is None:
        return None
    if not isinstance(price, dict):
        return None
    if "current" in price:
        return price
    amount = price.get("amount")
    currency = price.get("currency")
    if amount is None and currency is None:
        return None
    return {"current": {"amount": amount, "currency": currency}}


def Variant(  # noqa: N802 - keep legacy test helper API.
    *,
    id: str | None = None,
    sku: str | None = None,
    title: str | None = None,
    options: dict[str, str] | None = None,
    option_values: list[dict[str, str]] | None = None,
    price: dict[str, Any] | None = None,
    price_amount: float | int | str | None = None,
    currency: str | None = None,
    inventory: dict[str, Any] | None = None,
    inventory_quantity: int | None = None,
    weight: float | int | str | dict[str, Any] | None = None,
    weight_unit: str = "g",
    image: str | None = None,
    raw: dict[str, Any] | None = None,
) -> CanonicalVariant:
    normalized_option_values: list[dict[str, str]] = []
    if options:
        normalized_option_values.extend(
            [{"name": name, "value": value} for name, value in options.items()]
        )
    if option_values:
        normalized_option_values.extend(option_values)

    normalized_price = _legacy_price_to_canonical(price)
    if normalized_price is None and price_amount is not None:
        normalized_price = {"current": {"amount": price_amount, "currency": currency or "USD"}}

    normalized_inventory = dict(inventory or {})
    if inventory_quantity is not None and "quantity" not in normalized_inventory:
        normalized_inventory["quantity"] = inventory_quantity
    if "track_quantity" not in normalized_inventory and inventory_quantity is not None:
        normalized_inventory["track_quantity"] = True

    normalized_weight = weight
    if isinstance(weight, (int, float, str)):
        normalized_weight = {"value": weight, "unit": weight_unit}

    media: list[dict[str, Any]] = []
    if image:
        media.append({"url": image, "type": "image", "is_primary": True})

    variant = CanonicalVariant(
        id=id,
        sku=sku,
        title=title,
        option_values=normalized_option_values,
        price=normalized_price,
        inventory=normalized_inventory,
        weight=normalized_weight,
        media=media,
    )
    if raw is not None:
        variant.identifiers.values["raw"] = str(raw)
    return variant


def Product(  # noqa: N802 - keep legacy test helper API.
    *,
    source: dict[str, Any] | None = None,
    platform: str | None = None,
    id: str | None = None,
    slug: str | None = None,
    url: str | None = None,
    title: str | None = None,
    description: str | None = None,
    price: dict[str, Any] | None = None,
    images: list[str] | None = None,
    options: dict[str, list[str]] | list[dict[str, Any]] | None = None,
    variants: list[CanonicalVariant] | None = None,
    brand: str | None = None,
    category: str | None = None,
    meta_title: str | None = None,
    meta_description: str | None = None,
    tags: list[str] | None = None,
    vendor: str | None = None,
    weight: float | int | str | dict[str, Any] | None = None,
    requires_shipping: bool = True,
    track_quantity: bool = True,
    is_digital: bool = False,
    raw: dict[str, Any] | None = None,
) -> CanonicalProduct:
    normalized_source = dict(source or {})
    if not normalized_source:
        normalized_source = {
            "platform": platform or "unknown",
            "id": id,
            "slug": slug,
            "url": url,
        }

    normalized_price = _legacy_price_to_canonical(price)
    normalized_weight = weight
    if isinstance(weight, (int, float, str)):
        normalized_weight = {"value": weight, "unit": "g"}

    normalized_options = options
    if isinstance(options, dict):
        normalized_options = [{"name": name, "values": values} for name, values in options.items()]

    taxonomy = {"paths": [], "primary": None}
    if category:
        taxonomy = {"paths": [[category]], "primary": [category]}

    media = [{"url": image_url, "type": "image"} for image_url in (images or [])]
    provenance = {"raw": raw} if raw is not None else {}

    return CanonicalProduct(
        source=normalized_source,
        title=title,
        description=description,
        seo={"title": meta_title, "description": meta_description},
        brand=brand,
        vendor=vendor,
        taxonomy=taxonomy,
        tags=tags or [],
        options=normalized_options or [],
        variants=variants or [],
        price=normalized_price,
        weight=normalized_weight,
        requires_shipping=requires_shipping,
        track_quantity=track_quantity,
        is_digital=is_digital,
        media=media,
        provenance=provenance,
    )

