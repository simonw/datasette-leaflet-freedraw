from datasette import hookimpl
from datasette.filters import FilterArguments
import json
import textwrap


async def geometry_columns_for_table(datasette, database, table):
    # Returns [{"column": spatial_index_enabled (boolean)}]
    sql = """
        select f_geometry_column, spatial_index_enabled
        from geometry_columns
        where lower(f_table_name) = lower(:table)
    """
    db = datasette.get_database(database)
    return {
        r["f_geometry_column"]: bool(r["spatial_index_enabled"])
        for r in await db.execute(sql, {"table": table})
    }


@hookimpl
def filters_from_request(request, database, table, datasette):
    async def inner():
        geometry_columns = await geometry_columns_for_table(datasette, database, table)
        if not geometry_columns:
            return
        freedraw = request.args.get("_freedraw", "")
        try:
            geojson = json.loads(freedraw)
        except ValueError:
            return
        # Just use the first geometry column
        column, spatial_index_enabled = list(geometry_columns.items())[0]
        where_clauses = [
            "Intersects(GeomFromGeoJSON(:freedraw), [{}]) = 1".format(column)
        ]
        params = {"freedraw": json.dumps(geojson)}
        # Spatial index support, if possible
        if spatial_index_enabled:
            where_clauses.append(
                textwrap.dedent(
                    """
            [{table}].rowid in (select rowid from SpatialIndex where f_table_name = :freedraw_table
            and search_frame = GeomFromGeoJSON(:freedraw))
            """.format(
                        table=table
                    )
                ).strip()
            )
            params["freedraw_table"] = table
        return FilterArguments(
            where_clauses,
            params=params,
            human_descriptions=["geometry intersects the specified map area"],
        )

    return inner


@hookimpl
def extra_js_urls(view_name, datasette):
    if view_name == "database":
        return [
            {
                "url": datasette.urls.static_plugins(
                    "datasette-leaflet-freedraw", "datasette-leaflet-freedraw.js"
                ),
                "module": True,
            }
        ]


@hookimpl
def extra_body_script(datasette):
    return textwrap.dedent(
        """
    window.datasette = window.datasette || {{}};
    datasette.leaflet_freedraw = {{
        FREEDRAW_URL: '{}',
    }};
    """.format(
            datasette.urls.static_plugins(
                "datasette-leaflet-freedraw", "leaflet-freedraw.esm.js"
            ),
        )
    )
