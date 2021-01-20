from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert 200 == response.status_code
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-leaflet-freedraw" in installed_plugins


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "script",
    [
        "datasette-leaflet-freedraw.js",
        "leaflet-freedraw.esm.js",
        "leaflet.js",
        "leaflet.css",
    ],
)
async def test_plugin_scripts(script):
    datasette = Datasette([], memory=True)
    response = await datasette.client.get(
        "/-/static-plugins/datasette-leaflet-freedraw/{}".format(script)
    )
    assert 200 == response.status_code
