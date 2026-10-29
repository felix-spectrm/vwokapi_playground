# CLAUDE.md

CLI client for the VWOK API, built with Typer + httpx.

## Commands

- Install/sync: `uv sync`
- Run the CLI: `uv run vwok <command>`
- Type-check: `devenv tasks run python:typecheck` (basedpyright)

Config via env vars (or root flags placed before the subcommand, e.g. `vwok --client-id … catalog models DE VW`): `CLIENT_ID`, `CLIENT_SECRET` (OAuth client credentials; the client fetches and refreshes the 1-hour token), `BASE_URL` (optional). `.env` is auto-loaded by devenv.

Commands: `vwok catalog models|base-configuration|types|options` and `vwok operation configure|check|marketing-code|images|recover|resolve|solve|solutions`. Path params are positional arguments; the request body is a JSON `PAYLOAD` argument (inline, `@file.json`, or `-` for stdin) validated into `Configuration`.

## Architecture

uv workspace (Python >=3.14) with a strict two-layer split:

- `packages/vwok-client/` — typed HTTP client library (httpx + attrs + cattrs, ships `py.typed`). `http.py` is the authenticated transport (one reused `httpx.Client`, token handling, `ApiError` incl. `retry_after` on 429); `client.py` has `VwokClient` (wraps an `HttpClient`, built with `VwokClient.from_credentials`) with one method per endpoint; `models/` has the payload classes (`_payload.py`, parsed from JSON with cattrs) and response classes (`_responses.py`).
- `cmd/vwok-cli/` — thin Typer CLI on top of `vwok-client`; entry point `vwok`, one module per group in `apps/`, wired in `main.py`. No HTTP or model logic of its own.

When adding an endpoint: model(s) in `models/` and a method on `VwokClient` (plus `__init__.py` re-exports) → CLI command in `vwok-cli`.

OKAPI limits: 60 requests/minute per credential (shared); `marketing_code` writes to VW's production system; `check` returns `buildable: false` as a normal 200.
