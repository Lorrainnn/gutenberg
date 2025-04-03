import pathlib
import threading
from datetime import date

from zimscraperlib.zim.creator import Creator

from gutenberg2zim.constants import VERSION, logger
from zimscraperlib.zim.metadata import (
    StandardMetadataList,
    TitleMetadata,
    DescriptionMetadata,
    LongDescriptionMetadata,
    CreatorMetadata,
    PublisherMetadata,
    NameMetadata,
    LanguageMetadata,
    TagsMetadata,
    ScraperMetadata,
    DateMetadata,
)


class Global:
    """Shared context accross all scraper components"""

    creator: Creator
    _lock = threading.Lock()

    total = 0
    progress = 0

    @staticmethod
    def set_total(total):
        with Global._lock:
            Global.total = total

    @staticmethod
    def reset_progress():
        with Global._lock:
            Global.progress = 0

    @staticmethod
    def inc_progress():
        with Global._lock:
            Global.progress += 1

    @staticmethod
    def setup(filename, language, title, description, long_description, name, publisher):
        Global.creator = Creator(
            filename=filename,
            main_path="Home.html",
            workaround_nocancel=False,
        ).config_metadata(
            std_metadata=StandardMetadataList(
                title=TitleMetadata(title),
                description=DescriptionMetadata(description),
                long_description=LongDescriptionMetadata(long_description),
                creator=CreatorMetadata("gutenberg.org"),
                publisher=PublisherMetadata(publisher),
                name=NameMetadata(name),
                language=LanguageMetadata([language]),
                tags=TagsMetadata("_category:gutenberg;gutenberg"),
                scraper=ScraperMetadata(f"gutenberg2zim-{VERSION}"),
                date=DateMetadata(date.today()),
            )
        ).config_verbose(True)


    @staticmethod
    def add_item_for(
        path: str,
        title: str | None = None,
        fpath: pathlib.Path | None = None,
        content: bytes | None = None,
        mimetype: str | None = None,
        is_front: bool | None = None,
        should_compress: bool | None = None,
        *,
        delete_fpath: bool | None = False,
    ):
        logger.debug(f"\t\tAdding ZIM item at {path}")
        if not mimetype and path.endswith(".epub"):
            mimetype = "application/epub+zip"
        with Global._lock:
            Global.creator.add_item_for(
                path=path,
                title=title,
                fpath=fpath,
                content=content,
                mimetype=mimetype,
                is_front=is_front,
                should_compress=should_compress,
                delete_fpath=delete_fpath,
            )

    @staticmethod
    def add_illustration(illus_fpath, illus_size):
        with open(illus_fpath, "rb") as fh:
            with Global._lock:
                Global.creator.add_illustration(illus_size, fh.read())

    @staticmethod
    def start():
        Global.creator.start()

    @staticmethod
    def finish():
        if Global.creator.can_finish:
            logger.info("Finishing ZIM file")
            with Global._lock:
                Global.creator.finish()
            logger.info(
                f"Finished Zim {Global.creator.filename.name} "
                f"in {Global.creator.filename.parent}"
            )
