# sonarr-mcp

Part of the [arr-mcps](https://github.com/SavageCore/arr-mcps) collection.
MCP server exposing [Sonarr](https://sonarr.tv)'s v3 REST API
([OpenAPI 3.0.0](https://sonarr.tv/docs/api/)) as tools, so an LLM can read
and manage a Sonarr instance: series, episodes, episode files, the download
queue, history, indexers, import lists, custom formats, tags, commands, system
status, and more. Full surface — reads **and** writes, with destructive tools
flagged.

Built with [FastMCP](https://gofastmcp.com).

## Getting an API key

Generate one in Sonarr **Settings > General > Security**. Auth is the
`X-Api-Key` header.

## Install

Download a wheel from the [latest release](https://github.com/SavageCore/sonarr-mcp/releases/latest)
and install it as a `uv` tool (no repo checkout needed):

```bash
uv tool install sonarr_mcp-*.whl
```

This puts a `sonarr-mcp` command on your PATH. Register it with Claude Code:

```bash
claude mcp add sonarr \
  --env SONARR_URL=http://your-sonarr-host:8989 \
  --env SONARR_API_KEY=<key> \
  -- sonarr-mcp
```

### From source

```bash
uv sync
cp .env.example .env   # fill in SONARR_URL and SONARR_API_KEY
```

```bash
claude mcp add sonarr \
  --env SONARR_URL=http://your-sonarr-host:8989 \
  --env SONARR_API_KEY=<key> \
  -- uv run --directory /path/to/sonarr-mcp sonarr-mcp
```

## Config

| Env var | Required | Default |
|---|---|---|
| `SONARR_URL` | yes | - |
| `SONARR_API_KEY` | yes* | none (no `X-Api-Key` header sent if unset) |

\* Every API endpoint requires auth; practically you must set it, but the
server still starts without one so errors surface from the API rather than at
startup.

## Tools

**15 resource-scoped tools**, each covering multiple Sonarr v3 endpoints (223
total) via an `operation` parameter. Call a tool with `operation` set to one
of its listed operations and an `arguments` dict matching that operation's
parameters — the tool's own description (visible to your MCP client) lists
every operation, its signature, and a one-line doc. This keeps the full REST
surface available while costing a fraction of the context budget of
registering all 223 endpoints as separate tools.

| Tool | Operations | Kind |
|---|---|---|
| `sonarr_profiles_formats` | 49 | reads + writes |
| `sonarr_config` | 26 | reads + writes |
| `sonarr_media_library` | 26 | reads + writes |
| `sonarr_system_commands` | 20 | reads + writes |
| `sonarr_import_lists` | 18 | reads + writes |
| `sonarr_notifications_metadata` | 18 | reads + writes |
| `sonarr_download_clients` | 16 | reads + writes |
| `sonarr_indexers` | 11 | reads + writes |
| `sonarr_storage` | 8 | reads + writes |
| `sonarr_history_blocklist` | 7 | reads + writes |
| `sonarr_queue` | 7 | reads + writes |
| `sonarr_tags` | 7 | reads + writes |
| `sonarr_release_search` | 4 | reads + writes |
| `sonarr_wanted` | 4 | read-only |
| `sonarr_calendar` | 2 | read-only |

Example: `sonarr_queue(operation="sonarr_delete_queue", arguments={"id": 42})`.
Endpoint-level naming (`sonarr_<verb>_<resource>`) is preserved as the
`operation` value, so the full endpoint list is still discoverable from each
group tool's description at runtime.

## Development

```bash
make help  # list all commands
```

| Command | Does |
|---|---|
| `make sync` | `uv sync` |
| `make test` | Offline tests - one per endpoint, mocked HTTP |
| `make test-integration` | Tests against the live instance (needs `SONARR_URL`/`SONARR_API_KEY`) |
| `make build` | Build wheel + sdist into `dist/` |
| `make bump-patch` / `bump-minor` / `bump-major` | Bump the version in `pyproject.toml` + `uv.lock` |
| `make clean` | Remove build artifacts |

The release workflow (`.github/workflows/release.yml`) builds and publishes to
[Releases](https://github.com/SavageCore/sonarr-mcp/releases) whenever a `v*`
tag is pushed - so the usual flow is `make bump-patch`, commit, then tag and
push.

The offline suite covers every endpoint (mocked HTTP). The integration suite
exercises GET endpoints against your live instance; POST/PUT/DELETE only run
when `SONARR_WRITE_TESTS=1`, as a safe create→update→delete cycle against a
scratch tag that is cleaned up afterwards.
