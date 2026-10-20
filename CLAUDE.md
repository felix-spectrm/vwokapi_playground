# CLAUDE.md

CLI client for the VWOK API, built with Typer + httpx.

## Commands

- Install/sync: `uv sync`
- Run the CLI: `uv run vwok <command>`
- Type-check: `devenv tasks run python:typecheck` (basedpyright)

Config via env vars (or flags): `TOKEN`, `BASE_URL`. `.env` is auto-loaded by devenv.

## Architecture

uv workspace (Python >=3.14) with a strict two-layer split:

- `packages/vwok-client/` — typed HTTP client library (httpx + pydantic, ships `py.typed`). `http.py` has `VwokClient.request()` and `ApiError`; all models and API logic live here.
- `cmd/vwok-cli/` — thin Typer CLI on top of `vwok-client`; entry point `vwok`, all commands in `main.py`. No HTTP or model logic of its own.

When adding an endpoint: model(s) and client method in `vwok-client` (plus `__init__.py` re-export) → CLI command in `vwok-cli`.
