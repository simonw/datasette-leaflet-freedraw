# datasette-leaflet-freedraw

[![PyPI](https://img.shields.io/pypi/v/datasette-leaflet-freedraw.svg)](https://pypi.org/project/datasette-leaflet-freedraw/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-leaflet-freedraw?include_prereleases&label=changelog)](https://github.com/simonw/datasette-leaflet-freedraw/releases)
[![Tests](https://github.com/simonw/datasette-leaflet-freedraw/workflows/Test/badge.svg)](https://github.com/simonw/datasette-leaflet-freedraw/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-leaflet-freedraw/blob/main/LICENSE)

Draw polygons on maps in Datasette

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-leaflet-freedraw

Note that this uses a feature that will be released in Datasette 0.54 - so it currently requires the Datasette 0.54a0 alpha.

## Usage

This plugin looks for input fields on a page with names ending in `_freedraw` - it replaces them with a Leaflet map interface that includes the [FreeDraw](https://freedraw.herokuapp.com/) Leaflet plugin.

Configure canned queries with inputs called `freedraw` or ending in `_freedraw` to trigger the map interface.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-leaflet-freedraw
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
