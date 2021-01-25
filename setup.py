from setuptools import setup
import os

VERSION = "0.2.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-leaflet-freedraw",
    description="Draw polygons on maps in Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-leaflet-freedraw",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-leaflet-freedraw/issues",
        "CI": "https://github.com/simonw/datasette-leaflet-freedraw/actions",
        "Changelog": "https://github.com/simonw/datasette-leaflet-freedraw/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_leaflet_freedraw"],
    entry_points={"datasette": ["leaflet_freedraw = datasette_leaflet_freedraw"]},
    install_requires=["datasette>=0.54", "datasette-leaflet>=0.2"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-leaflet-freedraw[test]"],
    package_data={
        "datasette_leaflet_freedraw": [
            "static/*.js",
            "static/*.css",
            "static/*.js.map",
        ],
    },
    python_requires=">=3.6",
)
