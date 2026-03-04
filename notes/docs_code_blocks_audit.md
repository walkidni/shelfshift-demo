# Documentation Code Blocks Audit

- Generated on: 2026-03-03
- Total documentation code blocks: 65
- Source roots: `src/shelfshift_demo/content/library`, `src/shelfshift_demo/content/cli`

## Test-Derived Output Notes

- The inferred outputs below are derived from `tests/test_app.py`, `tests/test_csv_import_feature.py`, `tests/test_batch_csv_feature.py`, and `tests/test_batch_url_feature.py`.
- They are example outcomes, not guaranteed outputs for every placeholder input in docs snippets.

## Block Inventory (Full Content)

### Block 01 — `cli/ADVANCED_USAGE.md`

- Language: `json`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```json
{
  "source": {"platform": "shopify", "id": "123", "slug": "demo-item", "url": "https://example.com/products/demo-item"},
  "title": "Demo Item",
  "description": "Demo description",
  "tags": ["tag-a", "tag-b"],
  "options": [{"name": "Size", "values": ["S", "M"]}],
  "variants": [
    {
      "sku": "DEMO-S",
      "option_values": [{"name": "Size", "value": "S"}],
      "price": {"current": {"amount": "19.99", "currency": "USD"}},
      "inventory": {"track_quantity": true, "quantity": 10, "available": true, "allow_backorder": false},
      "weight": {"value": "250", "unit": "g"}
    }
  ],
  "price": {"current": {"amount": "19.99", "currency": "USD"}},
  "weight": {"value": "250", "unit": "g"},
  "media": [{"url": "https://cdn.example.com/image.jpg", "type": "image"}],
  "identifiers": {"values": {"barcode": "0123456789"}}
}
```

### Block 02 — `cli/ADVANCED_USAGE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```bash
shelfshift import-url "https://example.myshopify.com/products/demo-item" > import_result.json
python - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("import_result.json").read_text(encoding="utf-8"))
products = data["products"]

products[0]["title"] = "Edited via CLI workflow"
products[0]["tags"] = ["featured", "spring"]

Path("products_edited.json").write_text(
    json.dumps(products, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
PY
shelfshift export-csv ./products_edited.json --to shopify --out ./shopify.csv
```

### Block 03 — `cli/ADVANCED_USAGE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```bash
shelfshift import-url "https://example.myshopify.com/products/demo-item" > import_result.json
python - <<'PY'
import json
from pathlib import Path

payload = json.loads(Path("import_result.json").read_text(encoding="utf-8"))
Path("products_only.json").write_text(
    json.dumps(payload["products"], ensure_ascii=False, indent=2),
    encoding="utf-8",
)
PY
shelfshift export-csv ./products_only.json --to shopify --out ./shopify.csv
```

### Block 04 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: unknown URL can return `platform=None`; known product URLs return structured detection data, e.g. `platform="woocommerce"`, `is_product=True`, `slug="adjustable-wrench-set"`, and `platform="squarespace"`, `slug="custom-patchwork-shirt-snzgy"`.

```bash
shelfshift detect "https://example.myshopify.com/products/demo-item"
shelfshift detect ./source.csv
```

### Block 05 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```bash
shelfshift import-url "https://example.myshopify.com/products/demo-item"
```

### Block 06 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```bash
shelfshift import-url \
  "https://store-a.com/products/a" \
  "https://store-b.com/products/b"
```

### Block 07 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```bash
shelfshift import-url "https://store-a.com/products/a" --strict
```

### Block 08 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```bash
shelfshift import-csv ./source.csv
shelfshift import-csv ./source.csv --source-platform shopify
shelfshift import-csv ./source.csv --source-platform squarespace --source-weight-unit kg
```

### Block 09 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```bash
shelfshift convert ./source.csv \
  --to shopify \
  --out ./shopify.csv \
  --report ./convert_report.json
```

### Block 10 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```bash
shelfshift convert ./source.csv \
  --source squarespace \
  --source-weight-unit kg \
  --to woocommerce \
  --weight-unit g \
  --out ./woocommerce.csv \
  --report ./convert_report.json
```

### Block 11 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: Tests do not currently assert concrete `validate` report payload examples for these exact snippets.

```bash
shelfshift validate ./source.csv --platform shopify --report ./validate_report.json
shelfshift validate ./source.csv --platform wix --source-weight-unit lb --report ./validate_report.json
```

### Block 12 — `cli/COMMAND_REFERENCE.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```bash
shelfshift export-csv ./canonical_products.json \
  --to bigcommerce \
  --weight-unit g \
  --out ./bigcommerce.csv \
  --report ./export_report.json
```

### Block 13 — `cli/CORE_CONCEPTS.md`

- Language: `json`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```json
{
  "products": [/* canonical product objects */],
  "errors": [/* batch errors, if any */]
}
```

### Block 14 — `cli/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
python -m venv .venv
source .venv/bin/activate
pip install shelfshift
```

### Block 15 — `cli/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
uvx shelfshift --help
```

### Block 16 — `cli/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
uv tool install shelfshift
shelfshift --help
```

### Block 17 — `cli/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```bash
shelfshift convert ./source.csv \
  --to shopify \
  --out ./shopify.csv \
  --report ./convert_report.json
```

### Block 18 — `cli/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
shelfshift --help
```

### Block 19 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from pathlib import Path
from shelfshift.core import import_url, export_csv

imported = import_url("https://demo.myshopify.com/products/red-rain-coat")
product = imported.products[0]
product.title = "Edited Title"

exported = export_csv(product, target="bigcommerce", options={"bigcommerce_csv_format": "modern"})
Path("bigcommerce.csv").write_bytes(exported.csv_bytes)
```

### Block 20 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```python
from pathlib import Path
from shelfshift.core import import_csv, validate, export_csv

imported = import_csv("./source_wix.csv", platform="wix", source_weight_unit="kg")
reports = validate(imported.products)

if all(r.valid for r in reports):
    exported = export_csv(imported.products, target="shopify", options={"weight_unit": "g"})
    Path("shopify.csv").write_bytes(exported.csv_bytes)
```

### Block 21 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```python
from pathlib import Path
from shelfshift.core import import_json, export_csv

imported = import_json("./canonical_products.json", from_file=True)
exported = export_csv(imported.products, target="woocommerce", options={"weight_unit": "kg"})
Path("woocommerce.csv").write_bytes(exported.csv_bytes)
```

### Block 22 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from shelfshift.core import import_url

try:
    result = import_url([
        "https://demo.myshopify.com/products/red-rain-coat",
        "https://www.amazon.com/dp/B0C1234567",
    ], strict=True)
except ValueError as exc:
    print("Import failed:", exc)
```

### Block 23 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
register_importer(key: str, handler: ImporterFn) -> None
register_exporter(key: str, handler: ExporterFn) -> None
get_importer(key: str) -> ImporterFn
get_exporter(key: str) -> ExporterFn
list_importers() -> list[str]
list_exporters() -> list[str]
```

### Block 24 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
detect_csv_platform(csv_bytes: bytes) -> str
```

### Block 25 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
detect_product_url(url: str) -> dict
```

### Block 26 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
validate_product(product: Product) -> ValidationReport
```

### Block 27 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
normalize_product_url(product_url: str) -> str
import_products_from_urls(urls: list[str]) -> tuple[list[Product], list[dict[str, str]]]
```

### Block 28 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
parse_decimal_money(value: Any) -> Decimal | None
normalize_currency(value: Any) -> str | None
format_decimal(value: Decimal | None) -> str
resolve_option_defs(product: Product) -> list[OptionDef]
resolve_variant_option_values(product: Product, variant: Variant) -> list[OptionValue]
resolve_taxonomy_paths(product: Product) -> list[list[str]]
resolve_current_money(product: Product, variant: Variant | None = None) -> Money | None
resolve_primary_image_url(product: Product, variant: Variant | None = None) -> str | None
resolve_all_image_urls(product: Product) -> list[str]
```

### Block 29 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
product_to_shopify_rows(
    product: Product,
    *,
    publish: bool,
    weight_unit: str = "g",
) -> list[dict[str, str]]
```

### Block 30 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
product_to_bigcommerce_rows(
    product: Product,
    *,
    publish: bool,
    csv_format: Literal["modern", "legacy"] = "modern",
    weight_unit: str = "kg",
) -> list[dict[str, str]]
```

### Block 31 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
product_to_wix_rows(
    product: Product,
    *,
    publish: bool,
    weight_unit: str = "kg",
) -> list[dict[str, str]]
```

### Block 32 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
product_to_squarespace_rows(
    product: Product,
    *,
    publish: bool,
    product_page: str = "",
    product_url: str = "",
    weight_unit: str = "kg",
) -> list[dict[str, str]]
```

### Block 33 — `library/ADVANCED_USAGE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
product_to_woocommerce_rows(
    product: Product,
    *,
    publish: bool,
    weight_unit: str = "kg",
) -> list[dict[str, str]]
```

### Block 34 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
@dataclass(frozen=True)
class DetectResult:
    kind: str
    platform: str | None
    is_product: bool
    product_id: str | None = None
    slug: str | None = None


@dataclass
class ImportResult:
    products: list[Product]
    errors: list[dict[str, str]]


@dataclass(frozen=True)
class ExportResult:
    csv_bytes: bytes
    filename: str
```

### Block 35 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
def detect_url(url: str) -> DetectResult
```

### Block 36 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: unknown URL can return `platform=None`; known product URLs return structured detection data, e.g. `platform="woocommerce"`, `is_product=True`, `slug="adjustable-wrench-set"`, and `platform="squarespace"`, `slug="custom-patchwork-shirt-snzgy"`.

```python
from shelfshift.core import detect_url

result = detect_url("https://demo.myshopify.com/products/red-rain-coat")
print(result.platform)    # shopify
print(result.is_product)  # True
print(result.slug)        # red-rain-coat
```

### Block 37 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
def detect_csv(csv_input: bytes | str | pathlib.Path) -> DetectResult
```

### Block 38 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from shelfshift.core import detect_csv

result = detect_csv("./source.csv")
print(result.platform)  # e.g. shopify
```

### Block 39 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
def import_url(
    urls: str | list[str],
    *,
    strict: bool = False,
) -> ImportResult
```

### Block 40 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from shelfshift.core import import_url

single = import_url("https://demo.myshopify.com/products/red-rain-coat")
product = single.products[0]

batch = import_url([
    "https://demo.myshopify.com/products/red-rain-coat",
    "https://www.amazon.com/dp/B0C1234567",  # detectable but unsupported for import
])
print(len(batch.products))
print(batch.errors)
```

### Block 41 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from shelfshift.core import import_url

try:
    import_url(
        [
            "https://demo.myshopify.com/products/red-rain-coat",
            "https://www.amazon.com/dp/B0C1234567",
        ],
        strict=True,
    )
except ValueError as exc:
    print(str(exc))
    # Strict mode failed with 1 URL import error(s).
```

### Block 42 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```python
def import_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    platform: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
) -> ImportResult
```

### Block 43 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```python
from shelfshift.core import import_csv

result = import_csv("./source.csv")
print(len(result.products))

result2 = import_csv(
    "./source_bigcommerce.csv",
    platform="bigcommerce",
    source_weight_unit="kg",
)
```

### Block 44 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```python
from shelfshift.core import import_csv

try:
    import_csv("./empty.csv", strict=True)
except ValueError as exc:
    print(exc)
```

### Block 45 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
def import_json(
    payload: dict | list[dict] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> ImportResult
```

### Block 46 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from pathlib import Path
from shelfshift.core import import_json

single = import_json({"source": {"platform": "shopify"}, "title": "Demo"})

many = import_json([
    {"source": {"platform": "shopify"}, "title": "One"},
    {"source": {"platform": "shopify"}, "title": "Two"},
])

from_file = import_json("./canonical_products.json", from_file=True)
from_path_obj = import_json(Path("./canonical_products.json"))
```

### Block 47 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: export endpoints return CSV attachments (`text/csv`) with platform-specific columns. Example assertions include Shopify `Handle="demo-mug"` + `Variant SKU`, BigCommerce row types (`Product/Variant/Image`), Squarespace `Product Type [Non Editable]="PHYSICAL"`, and Wix rows with `fieldType` values `PRODUCT`/`VARIANT`.

```python
def export_csv(
    products: Product | list[Product],
    *,
    target: str,
    options: dict[str, Any] | None = None,
) -> ExportResult
```

### Block 48 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from pathlib import Path
from shelfshift.core import import_url, export_csv

imported = import_url("https://demo.myshopify.com/products/red-rain-coat")
exported = export_csv(
    imported.products,
    target="woocommerce",
    options={"publish": False, "weight_unit": "kg"},
)
Path("woocommerce.csv").write_bytes(exported.csv_bytes)
print(exported.filename)
```

### Block 49 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
def convert_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    target: str,
    source: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
    export_options: dict[str, Any] | None = None,
) -> tuple[bytes, dict[str, Any]]
```

### Block 50 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from pathlib import Path
from shelfshift.core import convert_csv

csv_bytes, report = convert_csv(
    "./source.csv",
    source="squarespace",
    source_weight_unit="kg",
    target="shopify",
    export_options={"weight_unit": "g"},
)
Path("shopify.csv").write_bytes(csv_bytes)
print(report)
```

### Block 51 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
def validate(products: Product | list[Product]) -> list[ValidationReport]
```

### Block 52 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: Shopify CSV import returns canonical product data such as `source.platform="shopify"`, `source.slug="v-neck-tee"`, `title="V-Neck T-Shirt"`, and variant SKUs `SQ-TEE-S` / `SQ-TEE-M`. Missing `source_weight_unit` for Squarespace yields HTTP 422 with `source_weight_unit is required`.

```python
from shelfshift.core import import_csv, validate

products = import_csv("./source.csv").products
reports = validate(products)
for i, report in enumerate(reports, start=1):
    print(i, report.valid)
    for issue in report.issues:
        print(issue.code, issue.field, issue.message)
```

### Block 53 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
def json_to_product(
    payload: dict[str, Any] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> Product


def json_to_products(
    payload: list[dict[str, Any]] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> list[Product]
```

### Block 54 — `library/API_REFERENCE.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from shelfshift.core import json_to_product, json_to_products

single = json_to_product({"source": {"platform": "shopify"}, "title": "Demo"})
many = json_to_products([
    {"source": {"platform": "shopify"}, "title": "One"},
    {"source": {"platform": "shopify"}, "title": "Two"},
])
```

### Block 55 — `library/CANONICAL_MODEL.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
@dataclass
class Product:
    source: SourceRef
    title: str | None
    description: str | None
    seo: Seo
    brand: str | None
    vendor: str | None
    taxonomy: CategorySet
    tags: list[str]
    options: list[OptionDef]
    variants: list[Variant]
    price: Price | None
    weight: Weight | None
    requires_shipping: bool
    track_quantity: bool
    is_digital: bool
    media: list[Media]
    identifiers: Identifiers
    provenance: dict[str, Any]
```

### Block 56 — `library/CANONICAL_MODEL.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
@dataclass
class SourceRef:
    platform: str
    id: str | None
    slug: str | None
    url: str | None

@dataclass
class Variant:
    id: str | None
    sku: str | None
    title: str | None
    option_values: list[OptionValue]
    price: Price | None
    inventory: Inventory
    weight: Weight | None
    media: list[Media]
    identifiers: Identifiers

@dataclass
class Price:
    current: Money
    compare_at: Money | None
    cost: Money | None
    min_price: Money | None
    max_price: Money | None

@dataclass
class Money:
    amount: Decimal | None
    currency: str | None

@dataclass
class Weight:
    value: Decimal | None
    unit: Literal["g", "kg", "lb", "oz"]

@dataclass
class Media:
    url: str
    type: Literal["image", "video"]
    alt: str | None
    position: int | None
    is_primary: bool | None
    variant_skus: list[str]

@dataclass
class OptionDef:
    name: str
    values: list[str]

@dataclass
class OptionValue:
    name: str
    value: str

@dataclass
class Inventory:
    track_quantity: bool | None
    quantity: int | None
    available: bool | None
    allow_backorder: bool | None

@dataclass
class Seo:
    title: str | None
    description: str | None

@dataclass
class CategorySet:
    paths: list[list[str]]
    primary: list[str] | None

@dataclass
class Identifiers:
    values: dict[str, str]
```

### Block 57 — `library/CANONICAL_MODEL.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from decimal import Decimal
from shelfshift.core import import_url, export_csv
from shelfshift.core.canonical import Money, Price

result = import_url("https://demo.myshopify.com/products/red-rain-coat")
product = result.products[0]

product.title = "Red Rain Coat v2"
product.tags = [*product.tags, "spring-2026"]

if product.price is None:
    product.price = Price(current=Money())
product.price.current.amount = Decimal("49.99")
product.price.current.currency = "USD"

csv_result = export_csv(product, target="shopify", options={"weight_unit": "g"})
```

### Block 58 — `library/CORE_CONCEPTS.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: unknown URL can return `platform=None`; known product URLs return structured detection data, e.g. `platform="woocommerce"`, `is_product=True`, `slug="adjustable-wrench-set"`, and `platform="squarespace"`, `slug="custom-patchwork-shirt-snzgy"`.

```python
from shelfshift.core import (
    detect_url,
    detect_csv,
    import_url,
    import_csv,
    import_json,
    export_csv,
    convert_csv,
    validate,
    json_to_product,
    json_to_products,
)
```

### Block 59 — `library/CORE_CONCEPTS.md`

- Language: `python`
- Output inference status: `n/a`
- Output note: Declaration/schema/reference block; no runtime output expected.

```python
def detect_url(url: str) -> DetectResult
def detect_csv(csv_input: bytes | str | pathlib.Path) -> DetectResult

def import_url(
    urls: str | list[str],
    *,
    strict: bool = False,
) -> ImportResult

def import_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    platform: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
) -> ImportResult

def import_json(
    payload: dict[str, Any] | list[dict[str, Any]] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> ImportResult

def export_csv(
    products: Product | list[Product],
    *,
    target: str,
    options: dict[str, Any] | None = None,
) -> ExportResult

def convert_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    target: str,
    source: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
    export_options: dict[str, Any] | None = None,
) -> tuple[bytes, dict[str, Any]]

def validate(products: Product | list[Product]) -> list[ValidationReport]

def json_to_product(
    payload: dict[str, Any] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> Product

def json_to_products(
    payload: list[dict[str, Any]] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> list[Product]
```

### Block 60 — `library/CORE_CONCEPTS.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from shelfshift.core.canonical import Product, Variant, Price, Money, Weight
```

### Block 61 — `library/CORE_CONCEPTS.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: URL import returns canonical product payloads. Batch import shape is `{products: [...], errors: [...]}` with partial-failure support (successful products preserved; failed URLs reported in `errors`).

```python
from shelfshift import import_url, export_csv
```

### Block 62 — `library/CORE_CONCEPTS.md`

- Language: `python`
- Output inference status: `inferred`
- Output note: From tests: unknown URL can return `platform=None`; known product URLs return structured detection data, e.g. `platform="woocommerce"`, `is_product=True`, `slug="adjustable-wrench-set"`, and `platform="squarespace"`, `slug="custom-patchwork-shirt-snzgy"`.

```python
__version__: str

def detect_url(url: str) -> DetectResult
def detect_csv(csv_input: bytes | str | pathlib.Path) -> DetectResult

def import_url(
    urls: str | list[str],
    *,
    strict: bool = False,
) -> ImportResult

def import_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    platform: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
) -> ImportResult

def import_json(
    payload: dict[str, Any] | list[dict[str, Any]] | str | bytes | pathlib.Path,
    *,
    from_file: bool = False,
) -> ImportResult

def export_csv(
    products: Product | list[Product],
    *,
    target: str,
    options: dict[str, Any] | None = None,
) -> ExportResult

def convert_csv(
    csv_input: bytes | str | pathlib.Path,
    *,
    target: str,
    source: str | None = None,
    strict: bool = False,
    source_weight_unit: str | None = None,
    export_options: dict[str, Any] | None = None,
) -> tuple[bytes, dict[str, Any]]

def validate(products: Product | list[Product]) -> list[ValidationReport]
```

### Block 63 — `library/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
uv add shelfshift
uv sync
```

### Block 64 — `library/GETTING_STARTED.md`

- Language: `bash`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```bash
pip install shelfshift
```

### Block 65 — `library/GETTING_STARTED.md`

- Language: `python`
- Output inference status: `hard`
- Output note: No direct, high-confidence output mapping found in tests for this exact snippet.

```python
from shelfshift import convert_csv

csv_bytes, report = convert_csv(
    "./source.csv",
    target="shopify",
)
```

## Hard-To-Infer Blocks

The following block IDs did not have enough direct test evidence for a confident concrete output example:

- 11, 14, 15, 16, 18, 29, 30, 31, 32, 33, 38, 45, 46, 49, 50, 53, 54, 60, 63, 64
- 65