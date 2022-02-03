from datasette.app import Datasette
from datasette.utils.sqlite import sqlite3
from datasette.utils.asgi import Request
from datasette.utils import find_spatialite
from datasette_leaflet_freedraw import extra_body_script, extra_js_urls
import pytest
import secrets


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


@pytest.mark.asyncio
async def test_extra_body_script():
    assert (
        await extra_body_script(
            datasette=Datasette([], memory=True),
            request=Request.fake("/"),
            database=None,
            table=None,
        )()
    ).strip() == (
        "window.datasette = window.datasette || {};\n"
        "datasette.leaflet_freedraw = {\n"
        "    FREEDRAW_URL: '/-/static-plugins/datasette-leaflet-freedraw/leaflet-freedraw.esm.js',\n"
        "    show_for_table: false,\n"
        "    current_geojson: null\n"
        "};"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "table,expect_map,expect_spatial_index",
    (
        (
            "places_no_spatialite",
            False,
            False,
        ),
        (
            "places_spatialite",
            True,
            False,
        ),
        (
            "places_spatialite_spatial_index",
            True,
            True,
        ),
    ),
)
@pytest.mark.skipif(find_spatialite() is None, reason="Could not find SpatiaLite")
async def test_show_for_table_only_if_spatialite(
    table, expect_map, expect_spatial_index
):
    dbname = "geodb{}".format(secrets.token_hex(4))
    datasette = Datasette(memory=True, files=[], sqlite_extensions=["spatialite"])
    db = datasette.add_memory_database(dbname)

    def setup(db):
        db.enable_load_extension(True)
        db.execute("SELECT load_extension(?)", [find_spatialite()])
        db.execute("SELECT InitSpatialMetadata(1)")
        db.execute(
            "CREATE TABLE places_no_spatialite (id integer primary key, name text)"
        )
        db.execute("CREATE TABLE places_spatialite (id integer primary key, name text)")
        db.execute(
            "SELECT AddGeometryColumn('places_spatialite', 'geometry', 4326, 'POINT', 'XY');"
        )
        db.execute(
            "CREATE TABLE places_spatialite_spatial_index (id integer primary key, name text)"
        )
        db.execute(
            "SELECT AddGeometryColumn('places_spatialite_spatial_index', 'geometry', 4326, 'POINT', 'XY');"
        )
        db.execute(
            "SELECT CreateSpatialIndex('places_spatialite_spatial_index', 'geometry');"
        )

    await db.execute_write_fn(setup, block=True)

    html = (await datasette.client.get("/{}/{}".format(dbname, table))).text
    if expect_map:
        assert "show_for_table: true," in html
    else:
        assert "show_for_table: false," in html

    if expect_spatial_index:
        # Feed it some GeoJSON and see if the SQL changes to the right value
        html2 = (
            await datasette.client.get(
                "/{}/{}?_freedraw={}".format(dbname, table, "{}")
            )
        ).text
        # Extract the SQL from the "View and edit SQL" link
        sql = html2.split('<p><a class="not-underlined" title="')[1].split('" href')[0]
        assert sql == (
            "select id, name, geometry from places_spatialite_spatial_index "
            "where Intersects(GeomFromGeoJSON(:freedraw), [geometry]) = 1 "
            "and [places_spatialite_spatial_index].rowid in "
            "(select rowid from SpatialIndex where f_table_name = :freedraw_table\n"
            "and search_frame = GeomFromGeoJSON(:freedraw)) order by id limit 101"
        )
