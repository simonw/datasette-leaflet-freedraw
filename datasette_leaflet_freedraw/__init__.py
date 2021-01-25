from datasette import hookimpl
import textwrap


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
