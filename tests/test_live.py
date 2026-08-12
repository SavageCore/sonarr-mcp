"""Integration tests against a real Sonarr instance.

Skipped unless SONARR_URL and SONARR_API_KEY are set. Run with:
    uv run pytest -m integration

GET endpoints are exercised against the live instance. POST/PUT/DELETE tools
only run when SONARR_WRITE_TESTS=1, and only as a safe create->update->delete
cycle against a scratch tag which is cleaned up afterwards. Never point write
tests at a production library.
"""

import os

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

import sonarr_mcp

from tests.test_tools import EXCLUDE_PATHS, EXCLUDE_CONTENT_ENDPOINTS, SPEC_PATH, registry_for

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not (os.environ.get("SONARR_URL") and os.environ.get("SONARR_API_KEY")),
        reason="requires SONARR_URL and SONARR_API_KEY",
    ),
]

WRITES_ENABLED = os.environ.get("SONARR_WRITE_TESTS") == "1"


def spec_ops():
    import json

    d = json.load(open(SPEC_PATH))
    ops = []
    for p, methods in d["paths"].items():
        for m, op in methods.items():
            if m in ("head", "parameters"):
                continue
            if p in EXCLUDE_PATHS or p in EXCLUDE_CONTENT_ENDPOINTS:
                continue
            if not (p.startswith("/api/v3") or p == "/ping"):
                continue
            ops.append((m.upper(), p, op))
    return ops


def pathless_get_ops():
    return [(m, p) for m, p, op in spec_ops() if m == "GET" and "{" not in p]


def op_to_args(spec):
    args = {}
    for p in spec["pp"]:
        args[p["name"]] = "abc" if p["type"] == "str" else 1
    return args


@pytest.fixture(autouse=True)
def configure_client():
    sonarr_mcp._client = sonarr_mcp.build_client(os.environ["SONARR_URL"], os.environ["SONARR_API_KEY"])
    yield
    sonarr_mcp._client = None


async def call(name, **kwargs):
    async with Client(sonarr_mcp.mcp) as c:
        return await c.call_tool(name, kwargs)


# --- always-on GET smoke tests ------------------------------------------------

async def test_ping():
    result = await call("sonarr_ping")
    assert result.data.get("status") == "OK"


async def test_system_status():
    result = await call("sonarr_get_system_status")
    assert "appName" in result.data
    assert "version" in result.data


# --- every GET collection endpoint is reachable --------------------------------

@pytest.mark.parametrize(
    "method,path",
    pathless_get_ops(),
    ids=[f"{m.lower()}_{p}" for m, p in pathless_get_ops()],
)
async def test_get_collection_endpoints_reachable(method, path):
    spec = registry_for(method, path)
    try:
        await call(spec["name"], **op_to_args(spec))
    except ToolError as e:
        status = int(str(e).split(":")[0].split()[-1])
        assert 400 <= status < 500, f"{spec['name']}: unexpected {e}"


# --- GET-by-id endpoints when data exists ----------------------------------------

async def test_get_series_by_id_when_series_exist():
    series = await call("sonarr_list_series")
    records = series.data
    if not isinstance(records, list) or not records:
        pytest.skip("no series on this instance")
    sid = records[0]["id"]
    result = await call("sonarr_get_series", id=sid)
    assert result.data["id"] == sid


async def test_get_tag_by_id_when_tags_exist():
    tags = await call("sonarr_list_tag")
    if not isinstance(tags.data, list) or not tags.data:
        pytest.skip("no tags on this instance")
    tid = tags.data[0]["id"]
    result = await call("sonarr_get_tag", id=tid)
    assert result.data["id"] == tid


async def test_get_episodefile_by_id_when_files_exist():
    files = await call("sonarr_list_episodefile")
    if not isinstance(files.data, list) or not files.data:
        pytest.skip("no episode files on this instance")
    fid = files.data[0]["id"]
    result = await call("sonarr_get_episodefile", id=fid)
    assert result.data["id"] == fid


# --- write tools: safe scratch-tag cycle (SONARR_WRITE_TESTS=1 only) ------------

@pytest.mark.skipif(not WRITES_ENABLED, reason="set SONARR_WRITE_TESTS=1 to run write tests")
async def test_tag_lifecycle():
    created = await call("sonarr_create_tag", body={"label": "mcp-test-tag"})
    tag = created.data
    assert tag["id"]
    try:
        fetched = await call("sonarr_get_tag", id=tag["id"])
        assert fetched.data["label"] == "mcp-test-tag"

        updated = await call("sonarr_update_tag", id=tag["id"], body={"id": tag["id"], "label": "mcp-test-tag-updated"})
        assert updated.data["label"] == "mcp-test-tag-updated"
    finally:
        await call("sonarr_delete_tag", id=tag["id"])

    listed = await call("sonarr_list_tag")
    assert not any(t["id"] == tag["id"] for t in listed.data)
