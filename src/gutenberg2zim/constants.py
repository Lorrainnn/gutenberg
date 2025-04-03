import logging
import pathlib
import base64
from zimscraperlib.logging import getLogger

from gutenberg2zim.__about__ import __version__

ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name

VERSION = __version__

SCRAPER = f"{NAME} {VERSION}"

# when modifiying this list, update list in hatch_build.py as well
JS_DEPS: list[str] = [
    "datatables/datatables.min.css",
    "datatables/datatables.min.js",
    "jquery/jquery-1.11.1.min.js",
]

logger = getLogger(NAME, level=logging.INFO)

TMP_FOLDER = "tmp"
TMP_FOLDER_PATH = pathlib.Path(TMP_FOLDER).resolve()

transparent_icon = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwAQMAAABtzGvEAAAAGXRFWHRTb2Z0d2FyZQBB"
        "ZG9iZSBJbWFnZVJlYWR5ccllPAAAAANQTFRFR3BMgvrS0gAAAAF0Uk5TAEDm2GYAAAAN"
        "SURBVBjTY2AYBdQEAAFQAAGn4toWAAAAAElFTkSuQmCC"
    )