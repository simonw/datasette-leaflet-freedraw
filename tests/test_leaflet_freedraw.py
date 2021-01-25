from datasette.app import Datasette
from datasette_leaflet_freedraw import extra_body_script, extra_js_urls
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
    ],
)
async def test_plugin_scripts(script):
    datasette = Datasette([], memory=True)
    response = await datasette.client.get(
        "/-/static-plugins/datasette-leaflet-freedraw/{}".format(script)
    )
    assert 200 == response.status_code


def test_extra_template_vars():
    assert extra_js_urls(
        datasette=Datasette([], memory=True), view_name="database"
    ) == [
        {
            "url": "/-/static-plugins/datasette-leaflet-freedraw/datasette-leaflet-freedraw.js",
            "module": True,
        }
    ]


def test_extra_body_script():
    assert extra_body_script(datasette=Datasette([], memory=True)).strip() == (
        "window.datasette = window.datasette || {};\n"
        "datasette.leaflet_freedraw = {\n"
        "    FREEDRAW_URL: '/-/static-plugins/datasette-leaflet-freedraw/leaflet-freedraw.esm.js',\n"
        "};"
    )
