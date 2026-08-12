# sonarr_openapi.json

Sonarr v3 OpenAPI spec, vendored from the Sonarr repo so the tool registry and
tests stay reproducible and work offline.

- Source: `src/Sonarr.Api.V3/openapi.json`
- Branch: `develop`, pinned to commit
  `e7caf8fbaa8e7b9dff48ce26b476ebcad7fd7324`
- The `_TOOL_REGISTRY` in `sonarr_mcp.py` is generated from this file. To
  refresh: download a newer `openapi.json`, regenerate the registry with the
  authoring script, update the SHA here and in `sonarr_mcp.py`/`AGENTS.md`, and
  re-run the tests.
