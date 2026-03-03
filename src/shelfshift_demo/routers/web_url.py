"""Web routes for URL-based import and direct export."""


from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from shelfshift.core import export_csv
from shelfshift.core.exporters.shared.weight_units import DEFAULT_WEIGHT_UNIT_BY_TARGET
from ..helpers.docs_content import (
	get_docs_neighbors,
	get_docs_page,
	get_docs_section,
	load_docs_markdown,
	render_docs_html,
)
from ..config import get_app_settings
from ..helpers import importing as _importing_helpers
from ..helpers.payload import product_to_json_b64, products_to_json_b64
from ..helpers.rendering import render_docs_page, render_landing_page, render_web_page
from ..helpers.serialization import serialize_product_for_api

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
	return render_landing_page(request, templates)


@router.get("/url", response_class=HTMLResponse)
def url_import_page(request: Request) -> HTMLResponse:
	return render_web_page(
		request,
		templates,
		template_name="url.html",
		active_page="url",
		error=None,
		product_urls=[],
		target_platform="shopify",
		weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
		bigcommerce_csv_format="modern",
		squarespace_product_page="",
		squarespace_product_url="",
	)


@router.get("/library", response_class=HTMLResponse)
def library_docs_page(request: Request) -> HTMLResponse:
	return _render_docs_section_page(request, section_key="library", slug=None)


@router.get("/cli", response_class=HTMLResponse)
def cli_docs_page(request: Request) -> HTMLResponse:
	return _render_docs_section_page(request, section_key="cli", slug=None)


@router.get("/library/{slug}", response_class=HTMLResponse)
def library_docs_subpage(request: Request, slug: str) -> HTMLResponse:
	return _render_docs_section_page(request, section_key="library", slug=slug)


@router.get("/cli/{slug}", response_class=HTMLResponse)
def cli_docs_subpage(request: Request, slug: str) -> HTMLResponse:
	return _render_docs_section_page(request, section_key="cli", slug=slug)


def _render_docs_section_page(
	request: Request,
	*,
	section_key: str,
	slug: str | None,
) -> HTMLResponse:
	section = get_docs_section(section_key)
	try:
		page = get_docs_page(section, slug)
		markdown_text = load_docs_markdown(section, page)
	except FileNotFoundError as exc:
		raise HTTPException(status_code=404, detail="Documentation page not found.") from exc

	docs_html, docs_toc_html = render_docs_html(section, markdown_text)
	prev_page, next_page = get_docs_neighbors(section, page)

	def _page_item(item):
		path = section.base_path if item.slug == "index" else f"{section.base_path}/{item.slug}"
		return {"slug": item.slug, "title": item.title, "path": path}

	return render_docs_page(
		request,
		templates,
		active_page="library_docs" if section.key == "library" else "cli_docs",
		docs_section_title=section.title,
		docs_source_index=section.source_index,
		docs_pages=[_page_item(item) for item in section.pages],
		docs_current_slug=page.slug,
		docs_current_title=page.title,
		docs_html=docs_html,
		docs_toc_html=docs_toc_html,
		docs_prev_page=_page_item(prev_page) if prev_page else None,
		docs_next_page=_page_item(next_page) if next_page else None,
	)


@router.post("/import.url")
def import_url_from_web(
	request: Request,
	product_urls: list[str] = Form(...),
) -> HTMLResponse:
	settings = get_app_settings(request)
	urls = [url.strip() for url in product_urls if url.strip()]
	if not urls:
		return render_web_page(
			request,
			templates,
			template_name="url.html",
			active_page="url",
			error="At least one product URL is required.",
			error_title="Import Error",
			product_urls=[],
			target_platform="shopify",
			weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
			bigcommerce_csv_format="modern",
			squarespace_product_page="",
			squarespace_product_url="",
			status_code=400,
		)

	try:
		if len(urls) == 1:
			products = [_importing_helpers.run_import_product(urls[0], settings=settings)]
			errors: list[dict[str, str]] = []
		else:
			products, errors = _importing_helpers.run_import_products(urls, settings=settings)
	except HTTPException as exc:
		return render_web_page(
			request,
			templates,
			template_name="url.html",
			active_page="url",
			error=str(exc.detail),
			error_title="Import Error",
			product_urls=urls,
			target_platform="shopify",
			weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
			bigcommerce_csv_format="modern",
			squarespace_product_page="",
			squarespace_product_url="",
			status_code=exc.status_code,
		)

	if len(products) == 1:
		product = products[0]
		editor_payload = serialize_product_for_api(product, include_raw=False)
		return render_web_page(
			request,
			templates,
			template_name="url.html",
			active_page="url",
			error=None,
			error_title="Import Error",
			product_urls=urls,
			target_platform="shopify",
			weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
			bigcommerce_csv_format="modern",
			squarespace_product_page="",
			squarespace_product_url="",
			preview_product_json_b64=product_to_json_b64(product),
			editor_product_payload=editor_payload,
			url_import_errors=errors,
		)

	if not products:
		return render_web_page(
			request,
			templates,
			template_name="url.html",
			active_page="url",
			error="All URL imports failed.",
			error_title="Import Error",
			product_urls=urls,
			target_platform="shopify",
			weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
			bigcommerce_csv_format="modern",
			squarespace_product_page="",
			squarespace_product_url="",
			url_import_errors=errors,
			status_code=422,
		)

	editor_payloads = [serialize_product_for_api(product, include_raw=False) for product in products]
	return render_web_page(
		request,
		templates,
		template_name="url.html",
		active_page="url",
		error=None,
		error_title="Import Error",
		product_urls=urls,
		target_platform="shopify",
		weight_unit=DEFAULT_WEIGHT_UNIT_BY_TARGET["shopify"],
		bigcommerce_csv_format="modern",
		squarespace_product_page="",
		squarespace_product_url="",
		preview_product_json_b64=products_to_json_b64(products),
		editor_product_payload=None,
		editor_products_payload=editor_payloads,
		url_import_errors=errors,
	)


def _export_csv_response(
	*,
	request: Request,
	product_urls: list[str],
	target_platform: str,
	publish: bool,
	weight_unit: str,
	bigcommerce_csv_format: str = "modern",
	squarespace_product_page: str = "",
	squarespace_product_url: str = "",
) -> Response:
	settings = get_app_settings(request)
	if len(product_urls) == 1:
		products = _importing_helpers.run_import_product(product_urls[0], settings=settings)
	else:
		products_list, errors = _importing_helpers.run_import_products(product_urls, settings=settings)
		if errors and not products_list:
			raise HTTPException(status_code=422, detail=errors[0]["detail"])
		products = products_list if len(products_list) > 1 else products_list[0]
	exported = export_csv(
		products,
		target=target_platform,
		options={
			"publish": publish,
			"weight_unit": weight_unit,
			"bigcommerce_csv_format": bigcommerce_csv_format,
			"squarespace_product_page": squarespace_product_page,
			"squarespace_product_url": squarespace_product_url,
		},
	)
	return Response(
		content=exported.csv_bytes,
		media_type="text/csv; charset=utf-8",
		headers={"Content-Disposition": f'attachment; filename="{exported.filename}"'},
	)


@router.post("/export/shopify.csv")
def export_shopify_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	publish: bool = Form(False),
	weight_unit: str = Form("g"),
) -> Response:
	return _export_csv_response(
		request=request,
		product_urls=[product_url],
		target_platform="shopify",
		publish=publish,
		weight_unit=weight_unit,
	)


@router.post("/export/bigcommerce.csv")
def export_bigcommerce_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	publish: bool = Form(False),
	csv_format: str = Form("modern"),
	weight_unit: str = Form("kg"),
) -> Response:
	return _export_csv_response(
		request=request,
		product_urls=[product_url],
		target_platform="bigcommerce",
		publish=publish,
		weight_unit=weight_unit,
		bigcommerce_csv_format=csv_format,
	)


@router.post("/export/wix.csv")
def export_wix_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	publish: bool = Form(False),
	weight_unit: str = Form("kg"),
) -> Response:
	return _export_csv_response(
		request=request,
		product_urls=[product_url],
		target_platform="wix",
		publish=publish,
		weight_unit=weight_unit,
	)


@router.post("/export/squarespace.csv")
def export_squarespace_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	publish: bool = Form(False),
	squarespace_product_page: str = Form(default=""),
	squarespace_product_url: str = Form(default=""),
	weight_unit: str = Form("kg"),
) -> Response:
	return _export_csv_response(
		request=request,
		product_urls=[product_url],
		target_platform="squarespace",
		publish=publish,
		weight_unit=weight_unit,
		squarespace_product_page=squarespace_product_page,
		squarespace_product_url=squarespace_product_url,
	)


@router.post("/export/woocommerce.csv")
def export_woocommerce_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	publish: bool = Form(False),
	weight_unit: str = Form("kg"),
) -> Response:
	return _export_csv_response(
		request=request,
		product_urls=[product_url],
		target_platform="woocommerce",
		publish=publish,
		weight_unit=weight_unit,
	)


@router.post("/export.csv")
def export_csv_from_web(
	request: Request,
	product_url: str = Form(...),
	target_platform: str = Form(...),
	publish: bool = Form(False),
	weight_unit: str = Form(default=""),
	bigcommerce_csv_format: str = Form("modern"),
	squarespace_product_page: str = Form(default=""),
	squarespace_product_url: str = Form(default=""),
) -> Response:
	try:
		return _export_csv_response(
			request=request,
			product_urls=[product_url],
			target_platform=target_platform,
			publish=publish,
			weight_unit=weight_unit,
			bigcommerce_csv_format=bigcommerce_csv_format,
			squarespace_product_page=squarespace_product_page,
			squarespace_product_url=squarespace_product_url,
		)
	except (HTTPException, ValueError) as exc:
		detail = exc.detail if isinstance(exc, HTTPException) else str(exc)
		status_code = exc.status_code if isinstance(exc, HTTPException) else 422
		return render_web_page(
			request,
			templates,
			template_name="url.html",
			active_page="url",
			error=detail,
			error_title="Export Error",
			product_urls=[product_url],
			target_platform=target_platform,
			weight_unit=weight_unit,
			bigcommerce_csv_format=bigcommerce_csv_format,
			squarespace_product_page=squarespace_product_page,
			squarespace_product_url=squarespace_product_url,
			status_code=status_code,
		)
