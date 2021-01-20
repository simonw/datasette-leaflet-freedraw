from datasette import hookimpl


@hookimpl
def extra_js_urls(view_name):
    print("extra_js_urls", view_name)
    if view_name == "database":
        return [
            "/-/static-plugins/datasette-leaflet-freedraw/leaflet.js",
            {
                "url": "/-/static-plugins/datasette-leaflet-freedraw/leaflet-freedraw.esm.js",
                "module": True,
            },
            "/-/static-plugins/datasette-leaflet-freedraw/datasette-leaflet-freedraw.js",
        ]


@hookimpl
def extra_css_urls(view_name):
    if view_name == "database":
        return [
            "/-/static-plugins/datasette-leaflet-freedraw/leaflet.css",
        ]
