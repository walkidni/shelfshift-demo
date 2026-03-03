from fastapi import FastAPI


def test_vercel_root_entrypoint_exports_fastapi_app() -> None:
    from app import app

    assert isinstance(app, FastAPI)
