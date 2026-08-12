# AGENTS.md — sonarr-mcp

MCP server exposing Sonarr's v3 REST API (OpenAPI 3.0.0) as tools so an LLM can read and manage a Sonarr instance: series, episodes, episode files, queue, history, indexers, import lists, custom formats, tags, commands, system status, and more. Full surface — reads and writes. Uses FastMCP, `uv` for deps.

## Testing
- Offline suite: `make test` (or `uv run pytest`)
- Live integration (needs `SONARR_URL`/`SONARR_API_KEY`): `make test-integration`
  - GET endpoints run against the live instance.
  - POST/PUT/DELETE only run when `SONARR_WRITE_TESTS=1` (safe create→update→delete cycles against a scratch tag, then cleanup). Never point write tests at a production library.

## Tool registry and the spec
- `_TOOL_REGISTRY` in `sonarr_mcp.py` is generated from the vendored spec at `tests/data/sonarr_openapi.json` (pinned to Sonarr develop HEAD e7caf8fbaa8e7b9dff48ce26b476ebcad7fd7324). It lists every JSON-producing endpoint under `/api/v3` plus `GET /ping`.
- Excluded on purpose: `/login`, `/logout`, `/ping` (kept), static web routes, the `.ics` calendar feed, and binary/text endpoints (media covers, raw log files) — `_req` JSON-decodes every response.
- To add a tool or refresh coverage, regenerate the registry from a newer `openapi.json` (same algorithm as the authoring script) and re-run the tests. Do not hand-edit the registry.
- Tool naming: `sonarr_<verb>_<resource>` derived from path + method (e.g. `sonarr_list_series`, `sonarr_add_series`, `sonarr_delete_series`, `sonarr_run_command`). Overrides for flagship/action endpoints live in the authoring script.

## Annotations convention
- GET endpoints: `readOnlyHint=True` (`READONLY`).
- POST/PUT: `readOnlyHint=False`, `destructiveHint=False` (`WRITE`).
- DELETE: `readOnlyHint=False`, `destructiveHint=True` (`DESTRUCTIVE`).
- Keep the three `ToolAnnotations` constants; never mark a write read-only.

## Auth and base path
- Auth: `X-Api-Key` header (generate in Sonarr Settings > General > Security). Not bearer.
- `build_client` points at the origin with no path suffix; every registered tool carries its full path (`/api/v3/...` or `/ping`). `_req` raises `ToolError` with the API status and message on `>=400`.

## Release workflow
Always use the `make bump-*` targets to bump the version (`uv version --bump patch|minor|major`), which updates `pyproject.toml` and `uv.lock` together. Do NOT edit the version by hand.

- Bump: `make bump-patch` (or `bump-minor` / `bump-major`)
- Commit message is **just the version**, e.g. `0.1.2` — nothing else.
- Tag it `v<version>` (e.g. `v0.1.2`).
- Push main and the tag:
  ```
  git push origin main
  git push origin v<version>
  ```
- Deploy to the Proxmox host (root SSH key): pull the repo then reinstall the uv tool:
  ```
  ssh root@192.168.50.3 -- 'cd /root/sonarr-mcp && git fetch origin && git reset --hard origin/main'
  ssh root@192.168.50.3 -- 'cd /root/sonarr-mcp && uv tool install --force .'
  ```
  The host runs it via `uv tool install` → `/root/.local/bin/sonarr-mcp` (not from the repo). Locally it is registered in the christopfarr project opencode via `uv tool install` (no project copy dir).

## Initial state
Version starts at `0.0.0` in the initial commit. No tag on the scaffold commit; releases begin at the first `make bump-*`.
