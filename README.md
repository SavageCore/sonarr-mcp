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

One tool per Sonarr v3 JSON endpoint (plus `GET /ping`). Naming is
`sonarr_<verb>_<resource>`. GET endpoints are read-only; POST/PUT are writes;
DELETE endpoints are flagged destructive.

| Tool | Method | Endpoint |
|---|---|
| **AutoTagging** | | |
| `sonarr_list_autotagging` | GET | `/api/v3/autotagging` |
| `sonarr_create_autotagging` | POST | `/api/v3/autotagging` |
| `sonarr_list_autotagging_schema` | GET | `/api/v3/autotagging/schema` |
| `sonarr_delete_autotagging` | DELETE | `/api/v3/autotagging/{id}` |
| `sonarr_get_autotagging` | GET | `/api/v3/autotagging/{id}` |
| `sonarr_update_autotagging` | PUT | `/api/v3/autotagging/{id}` |
| **Backup** | | |
| `sonarr_list_system_backup` | GET | `/api/v3/system/backup` |
| `sonarr_restore_backup_upload` | POST | `/api/v3/system/backup/restore/upload` |
| `sonarr_restore_backup` | POST | `/api/v3/system/backup/restore/{id}` |
| `sonarr_delete_system_backup` | DELETE | `/api/v3/system/backup/{id}` |
| **Blocklist** | | |
| `sonarr_list_blocklist` | GET | `/api/v3/blocklist` |
| `sonarr_bulk_delete_blocklist` | DELETE | `/api/v3/blocklist/bulk` |
| `sonarr_delete_blocklist` | DELETE | `/api/v3/blocklist/{id}` |
| **Calendar** | | |
| `sonarr_list_calendar` | GET | `/api/v3/calendar` |
| `sonarr_get_calendar` | GET | `/api/v3/calendar/{id}` |
| **Command** | | |
| `sonarr_list_command` | GET | `/api/v3/command` |
| `sonarr_run_command` | POST | `/api/v3/command` |
| `sonarr_delete_command` | DELETE | `/api/v3/command/{id}` |
| `sonarr_get_command` | GET | `/api/v3/command/{id}` |
| **CustomFilter** | | |
| `sonarr_list_customfilter` | GET | `/api/v3/customfilter` |
| `sonarr_create_customfilter` | POST | `/api/v3/customfilter` |
| `sonarr_delete_customfilter` | DELETE | `/api/v3/customfilter/{id}` |
| `sonarr_get_customfilter` | GET | `/api/v3/customfilter/{id}` |
| `sonarr_update_customfilter` | PUT | `/api/v3/customfilter/{id}` |
| **CustomFormat** | | |
| `sonarr_list_customformat` | GET | `/api/v3/customformat` |
| `sonarr_create_customformat` | POST | `/api/v3/customformat` |
| `sonarr_bulk_delete_customformat` | DELETE | `/api/v3/customformat/bulk` |
| `sonarr_bulk_update_customformat` | PUT | `/api/v3/customformat/bulk` |
| `sonarr_list_customformat_schema` | GET | `/api/v3/customformat/schema` |
| `sonarr_delete_customformat` | DELETE | `/api/v3/customformat/{id}` |
| `sonarr_get_customformat` | GET | `/api/v3/customformat/{id}` |
| `sonarr_update_customformat` | PUT | `/api/v3/customformat/{id}` |
| **Cutoff** | | |
| `sonarr_list_wanted_cutoff` | GET | `/api/v3/wanted/cutoff` |
| `sonarr_get_wanted_cutoff` | GET | `/api/v3/wanted/cutoff/{id}` |
| **DelayProfile** | | |
| `sonarr_list_delayprofile` | GET | `/api/v3/delayprofile` |
| `sonarr_create_delayprofile` | POST | `/api/v3/delayprofile` |
| `sonarr_reorder_delayprofile` | PUT | `/api/v3/delayprofile/reorder/{id}` |
| `sonarr_delete_delayprofile` | DELETE | `/api/v3/delayprofile/{id}` |
| `sonarr_get_delayprofile` | GET | `/api/v3/delayprofile/{id}` |
| `sonarr_update_delayprofile` | PUT | `/api/v3/delayprofile/{id}` |
| **DiskSpace** | | |
| `sonarr_get_diskspace` | GET | `/api/v3/diskspace` |
| **DownloadClient** | | |
| `sonarr_list_downloadclient` | GET | `/api/v3/downloadclient` |
| `sonarr_create_downloadclient` | POST | `/api/v3/downloadclient` |
| `sonarr_create_downloadclient_action` | POST | `/api/v3/downloadclient/action/{name}` |
| `sonarr_delete_downloadclient_bulk` | DELETE | `/api/v3/downloadclient/bulk` |
| `sonarr_update_downloadclient_bulk` | PUT | `/api/v3/downloadclient/bulk` |
| `sonarr_list_downloadclient_schema` | GET | `/api/v3/downloadclient/schema` |
| `sonarr_create_downloadclient_test` | POST | `/api/v3/downloadclient/test` |
| `sonarr_create_downloadclient_testall` | POST | `/api/v3/downloadclient/testall` |
| `sonarr_delete_downloadclient` | DELETE | `/api/v3/downloadclient/{id}` |
| `sonarr_get_downloadclient` | GET | `/api/v3/downloadclient/{id}` |
| `sonarr_update_downloadclient` | PUT | `/api/v3/downloadclient/{id}` |
| **DownloadClientConfig** | | |
| `sonarr_get_config_downloadclient` | GET | `/api/v3/config/downloadclient` |
| `sonarr_get_config_downloadclient_by_id` | GET | `/api/v3/config/downloadclient/{id}` |
| `sonarr_update_config_downloadclient` | PUT | `/api/v3/config/downloadclient/{id}` |
| **Episode** | | |
| `sonarr_list_episode` | GET | `/api/v3/episode` |
| `sonarr_monitor_episode` | PUT | `/api/v3/episode/monitor` |
| `sonarr_get_episode` | GET | `/api/v3/episode/{id}` |
| `sonarr_update_episode` | PUT | `/api/v3/episode/{id}` |
| **EpisodeFile** | | |
| `sonarr_list_episodefile` | GET | `/api/v3/episodefile` |
| `sonarr_bulk_delete_episodefile` | DELETE | `/api/v3/episodefile/bulk` |
| `sonarr_bulk_update_episodefile` | PUT | `/api/v3/episodefile/bulk` |
| `sonarr_bulk_edit_episodefiles` | PUT | `/api/v3/episodefile/editor` |
| `sonarr_delete_episodefile` | DELETE | `/api/v3/episodefile/{id}` |
| `sonarr_get_episodefile` | GET | `/api/v3/episodefile/{id}` |
| `sonarr_update_episodefile` | PUT | `/api/v3/episodefile/{id}` |
| **FileSystem** | | |
| `sonarr_list_filesystem` | GET | `/api/v3/filesystem` |
| `sonarr_list_filesystem_mediafiles` | GET | `/api/v3/filesystem/mediafiles` |
| `sonarr_list_filesystem_type` | GET | `/api/v3/filesystem/type` |
| **Health** | | |
| `sonarr_get_health` | GET | `/api/v3/health` |
| **History** | | |
| `sonarr_list_history` | GET | `/api/v3/history` |
| `sonarr_mark_history_item_failed` | POST | `/api/v3/history/failed/{id}` |
| `sonarr_list_history_series` | GET | `/api/v3/history/series` |
| `sonarr_list_history_since` | GET | `/api/v3/history/since` |
| **HostConfig** | | |
| `sonarr_get_config_host` | GET | `/api/v3/config/host` |
| `sonarr_get_config_host_by_id` | GET | `/api/v3/config/host/{id}` |
| `sonarr_update_config_host` | PUT | `/api/v3/config/host/{id}` |
| **ImportList** | | |
| `sonarr_list_importlist` | GET | `/api/v3/importlist` |
| `sonarr_create_importlist` | POST | `/api/v3/importlist` |
| `sonarr_create_importlist_action` | POST | `/api/v3/importlist/action/{name}` |
| `sonarr_delete_importlist_bulk` | DELETE | `/api/v3/importlist/bulk` |
| `sonarr_update_importlist_bulk` | PUT | `/api/v3/importlist/bulk` |
| `sonarr_list_importlist_schema` | GET | `/api/v3/importlist/schema` |
| `sonarr_create_importlist_test` | POST | `/api/v3/importlist/test` |
| `sonarr_create_importlist_testall` | POST | `/api/v3/importlist/testall` |
| `sonarr_delete_importlist` | DELETE | `/api/v3/importlist/{id}` |
| `sonarr_get_importlist` | GET | `/api/v3/importlist/{id}` |
| `sonarr_update_importlist` | PUT | `/api/v3/importlist/{id}` |
| **ImportListConfig** | | |
| `sonarr_get_config_importlist` | GET | `/api/v3/config/importlist` |
| `sonarr_get_config_importlist_by_id` | GET | `/api/v3/config/importlist/{id}` |
| `sonarr_update_config_importlist` | PUT | `/api/v3/config/importlist/{id}` |
| **ImportListExclusion** | | |
| `sonarr_list_importlistexclusion` | GET | `/api/v3/importlistexclusion` |
| `sonarr_create_importlistexclusion` | POST | `/api/v3/importlistexclusion` |
| `sonarr_delete_importlistexclusion_bulk` | DELETE | `/api/v3/importlistexclusion/bulk` |
| `sonarr_list_importlistexclusion_paged` | GET | `/api/v3/importlistexclusion/paged` |
| `sonarr_delete_importlistexclusion` | DELETE | `/api/v3/importlistexclusion/{id}` |
| `sonarr_get_importlistexclusion` | GET | `/api/v3/importlistexclusion/{id}` |
| `sonarr_update_importlistexclusion` | PUT | `/api/v3/importlistexclusion/{id}` |
| **Indexer** | | |
| `sonarr_list_indexer` | GET | `/api/v3/indexer` |
| `sonarr_create_indexer` | POST | `/api/v3/indexer` |
| `sonarr_create_indexer_action` | POST | `/api/v3/indexer/action/{name}` |
| `sonarr_delete_indexer_bulk` | DELETE | `/api/v3/indexer/bulk` |
| `sonarr_update_indexer_bulk` | PUT | `/api/v3/indexer/bulk` |
| `sonarr_list_indexer_schema` | GET | `/api/v3/indexer/schema` |
| `sonarr_create_indexer_test` | POST | `/api/v3/indexer/test` |
| `sonarr_create_indexer_testall` | POST | `/api/v3/indexer/testall` |
| `sonarr_delete_indexer` | DELETE | `/api/v3/indexer/{id}` |
| `sonarr_get_indexer` | GET | `/api/v3/indexer/{id}` |
| `sonarr_update_indexer` | PUT | `/api/v3/indexer/{id}` |
| **IndexerConfig** | | |
| `sonarr_get_config_indexer` | GET | `/api/v3/config/indexer` |
| `sonarr_get_config_indexer_by_id` | GET | `/api/v3/config/indexer/{id}` |
| `sonarr_update_config_indexer` | PUT | `/api/v3/config/indexer/{id}` |
| **IndexerFlag** | | |
| `sonarr_get_indexerflag` | GET | `/api/v3/indexerflag` |
| **Language** | | |
| `sonarr_list_language` | GET | `/api/v3/language` |
| `sonarr_get_language` | GET | `/api/v3/language/{id}` |
| **LanguageProfile** | | |
| `sonarr_list_languageprofile` | GET | `/api/v3/languageprofile` |
| `sonarr_create_languageprofile` | POST | `/api/v3/languageprofile` |
| `sonarr_delete_languageprofile` | DELETE | `/api/v3/languageprofile/{id}` |
| `sonarr_get_languageprofile` | GET | `/api/v3/languageprofile/{id}` |
| `sonarr_update_languageprofile` | PUT | `/api/v3/languageprofile/{id}` |
| **LanguageProfileSchema** | | |
| `sonarr_list_languageprofile_schema` | GET | `/api/v3/languageprofile/schema` |
| **Localization** | | |
| `sonarr_list_localization` | GET | `/api/v3/localization` |
| `sonarr_get_localization_language` | GET | `/api/v3/localization/language` |
| `sonarr_get_localization` | GET | `/api/v3/localization/{id}` |
| **Log** | | |
| `sonarr_list_log` | GET | `/api/v3/log` |
| **LogFile** | | |
| `sonarr_list_log_file` | GET | `/api/v3/log/file` |
| **ManualImport** | | |
| `sonarr_list_manualimport` | GET | `/api/v3/manualimport` |
| `sonarr_commit_manual_import` | POST | `/api/v3/manualimport` |
| **MediaManagementConfig** | | |
| `sonarr_get_config_mediamanagement` | GET | `/api/v3/config/mediamanagement` |
| `sonarr_get_config_mediamanagement_by_id` | GET | `/api/v3/config/mediamanagement/{id}` |
| `sonarr_update_config_mediamanagement` | PUT | `/api/v3/config/mediamanagement/{id}` |
| **Metadata** | | |
| `sonarr_list_metadata` | GET | `/api/v3/metadata` |
| `sonarr_create_metadata` | POST | `/api/v3/metadata` |
| `sonarr_create_metadata_action` | POST | `/api/v3/metadata/action/{name}` |
| `sonarr_list_metadata_schema` | GET | `/api/v3/metadata/schema` |
| `sonarr_create_metadata_test` | POST | `/api/v3/metadata/test` |
| `sonarr_create_metadata_testall` | POST | `/api/v3/metadata/testall` |
| `sonarr_delete_metadata` | DELETE | `/api/v3/metadata/{id}` |
| `sonarr_get_metadata` | GET | `/api/v3/metadata/{id}` |
| `sonarr_update_metadata` | PUT | `/api/v3/metadata/{id}` |
| **Missing** | | |
| `sonarr_list_wanted_missing` | GET | `/api/v3/wanted/missing` |
| `sonarr_get_wanted_missing` | GET | `/api/v3/wanted/missing/{id}` |
| **NamingConfig** | | |
| `sonarr_get_config_naming` | GET | `/api/v3/config/naming` |
| `sonarr_list_config_naming_examples` | GET | `/api/v3/config/naming/examples` |
| `sonarr_get_config_naming_by_id` | GET | `/api/v3/config/naming/{id}` |
| `sonarr_update_config_naming` | PUT | `/api/v3/config/naming/{id}` |
| **Notification** | | |
| `sonarr_list_notification` | GET | `/api/v3/notification` |
| `sonarr_create_notification` | POST | `/api/v3/notification` |
| `sonarr_create_notification_action` | POST | `/api/v3/notification/action/{name}` |
| `sonarr_list_notification_schema` | GET | `/api/v3/notification/schema` |
| `sonarr_create_notification_test` | POST | `/api/v3/notification/test` |
| `sonarr_create_notification_testall` | POST | `/api/v3/notification/testall` |
| `sonarr_delete_notification` | DELETE | `/api/v3/notification/{id}` |
| `sonarr_get_notification` | GET | `/api/v3/notification/{id}` |
| `sonarr_update_notification` | PUT | `/api/v3/notification/{id}` |
| **Parse** | | |
| `sonarr_get_parse` | GET | `/api/v3/parse` |
| **Ping** | | |
| `sonarr_ping` | GET | `/ping` |
| **QualityDefinition** | | |
| `sonarr_list_qualitydefinition` | GET | `/api/v3/qualitydefinition` |
| `sonarr_get_qualitydefinition_limits` | GET | `/api/v3/qualitydefinition/limits` |
| `sonarr_update_quality_definitions` | PUT | `/api/v3/qualitydefinition/update` |
| `sonarr_get_qualitydefinition` | GET | `/api/v3/qualitydefinition/{id}` |
| `sonarr_update_qualitydefinition` | PUT | `/api/v3/qualitydefinition/{id}` |
| **QualityProfile** | | |
| `sonarr_list_qualityprofile` | GET | `/api/v3/qualityprofile` |
| `sonarr_create_qualityprofile` | POST | `/api/v3/qualityprofile` |
| `sonarr_delete_qualityprofile` | DELETE | `/api/v3/qualityprofile/{id}` |
| `sonarr_get_qualityprofile` | GET | `/api/v3/qualityprofile/{id}` |
| `sonarr_update_qualityprofile` | PUT | `/api/v3/qualityprofile/{id}` |
| **QualityProfileSchema** | | |
| `sonarr_list_qualityprofile_schema` | GET | `/api/v3/qualityprofile/schema` |
| **Queue** | | |
| `sonarr_list_queue` | GET | `/api/v3/queue` |
| `sonarr_bulk_delete_queue` | DELETE | `/api/v3/queue/bulk` |
| `sonarr_delete_queue` | DELETE | `/api/v3/queue/{id}` |
| **QueueAction** | | |
| `sonarr_grab_queue_bulk` | POST | `/api/v3/queue/grab/bulk` |
| `sonarr_grab_queue_item` | POST | `/api/v3/queue/grab/{id}` |
| **QueueDetails** | | |
| `sonarr_get_queue_details` | GET | `/api/v3/queue/details` |
| **QueueStatus** | | |
| `sonarr_get_queue_status` | GET | `/api/v3/queue/status` |
| **Release** | | |
| `sonarr_list_release` | GET | `/api/v3/release` |
| `sonarr_search_releases` | POST | `/api/v3/release` |
| **ReleaseProfile** | | |
| `sonarr_list_releaseprofile` | GET | `/api/v3/releaseprofile` |
| `sonarr_create_releaseprofile` | POST | `/api/v3/releaseprofile` |
| `sonarr_delete_releaseprofile` | DELETE | `/api/v3/releaseprofile/{id}` |
| `sonarr_get_releaseprofile` | GET | `/api/v3/releaseprofile/{id}` |
| `sonarr_update_releaseprofile` | PUT | `/api/v3/releaseprofile/{id}` |
| **ReleasePush** | | |
| `sonarr_push_release` | POST | `/api/v3/release/push` |
| **RemotePathMapping** | | |
| `sonarr_list_remotepathmapping` | GET | `/api/v3/remotepathmapping` |
| `sonarr_create_remotepathmapping` | POST | `/api/v3/remotepathmapping` |
| `sonarr_delete_remotepathmapping` | DELETE | `/api/v3/remotepathmapping/{id}` |
| `sonarr_get_remotepathmapping` | GET | `/api/v3/remotepathmapping/{id}` |
| `sonarr_update_remotepathmapping` | PUT | `/api/v3/remotepathmapping/{id}` |
| **RenameEpisode** | | |
| `sonarr_get_rename` | GET | `/api/v3/rename` |
| **RootFolder** | | |
| `sonarr_list_rootfolder` | GET | `/api/v3/rootfolder` |
| `sonarr_create_rootfolder` | POST | `/api/v3/rootfolder` |
| `sonarr_delete_rootfolder` | DELETE | `/api/v3/rootfolder/{id}` |
| `sonarr_get_rootfolder` | GET | `/api/v3/rootfolder/{id}` |
| **SeasonPass** | | |
| `sonarr_update_season_pass` | POST | `/api/v3/seasonpass` |
| **Series** | | |
| `sonarr_list_series` | GET | `/api/v3/series` |
| `sonarr_add_series` | POST | `/api/v3/series` |
| `sonarr_delete_series` | DELETE | `/api/v3/series/{id}` |
| `sonarr_get_series` | GET | `/api/v3/series/{id}` |
| `sonarr_update_series` | PUT | `/api/v3/series/{id}` |
| **SeriesEditor** | | |
| `sonarr_bulk_delete_series` | DELETE | `/api/v3/series/editor` |
| `sonarr_bulk_update_series` | PUT | `/api/v3/series/editor` |
| **SeriesFolder** | | |
| `sonarr_get_series_folder` | GET | `/api/v3/series/{id}/folder` |
| **SeriesImport** | | |
| `sonarr_import_series` | POST | `/api/v3/series/import` |
| **SeriesLookup** | | |
| `sonarr_lookup_series` | GET | `/api/v3/series/lookup` |
| **System** | | |
| `sonarr_restart_sonarr` | POST | `/api/v3/system/restart` |
| `sonarr_get_system_routes` | GET | `/api/v3/system/routes` |
| `sonarr_get_system_routes_duplicate` | GET | `/api/v3/system/routes/duplicate` |
| `sonarr_shutdown_sonarr` | POST | `/api/v3/system/shutdown` |
| `sonarr_get_system_status` | GET | `/api/v3/system/status` |
| **Tag** | | |
| `sonarr_list_tag` | GET | `/api/v3/tag` |
| `sonarr_create_tag` | POST | `/api/v3/tag` |
| `sonarr_delete_tag` | DELETE | `/api/v3/tag/{id}` |
| `sonarr_get_tag` | GET | `/api/v3/tag/{id}` |
| `sonarr_update_tag` | PUT | `/api/v3/tag/{id}` |
| **TagDetails** | | |
| `sonarr_list_tag_detail` | GET | `/api/v3/tag/detail` |
| `sonarr_get_tag_detail` | GET | `/api/v3/tag/detail/{id}` |
| **Task** | | |
| `sonarr_get_system_task` | GET | `/api/v3/system/task` |
| `sonarr_get_system_task_by_id` | GET | `/api/v3/system/task/{id}` |
| **UiConfig** | | |
| `sonarr_get_config_ui` | GET | `/api/v3/config/ui` |
| `sonarr_get_config_ui_by_id` | GET | `/api/v3/config/ui/{id}` |
| `sonarr_update_config_ui` | PUT | `/api/v3/config/ui/{id}` |
| **Update** | | |
| `sonarr_list_update` | GET | `/api/v3/update` |
| **UpdateLogFile** | | |
| `sonarr_list_log_file_update` | GET | `/api/v3/log/file/update` |

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
