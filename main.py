import logging
import time

from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


# TODO: Join the .csv and .mp3 handlers and check extension in `on_created()`?
class CsvHandler(PatternMatchingEventHandler):
    # Step 0; Initialize Handlers.
    def __init__(self):
        super().__init__(
            patterns=["*.csv"], ignore_directories=True, case_sensitive=False
        )

    """
    NOTE: New CSV transcript file processed by MacWhisper locally using watch folder...
    Update SQLite DB with transcript CSV as text for specified file (using base filename as primary key).
    Once finished, delete both the .CSV and .MP3 files.
    """

    # Step 2; Handle generated .csv transcript file.
    def on_created(self, event: FileSystemEvent) -> None:
        logger.info(
            f"[csv] Watchdog recieved {event.event_type} event: {event.src_path}"
        )

    """
    NOTE: Not sure we need the `on_deleted()` handlers. Only reason I can think of is if we fetch more .MP3s to process,
    but that could also just be done when processing the .csv's `on_created()` handler.
    """

    # Step 4; Delete .csv file after it's been added to SQLite.
    def on_deleted(self, event: FileSystemEvent) -> None:
        logger.info(
            f"[csv] Watchdog recieved {event.event_type} event: {event.src_path}"
        )


class Mp3Handler(PatternMatchingEventHandler):
    # Step 0; Initialize Handlers.
    def __init__(self):
        super().__init__(
            patterns=["*.mp3"], ignore_directories=True, case_sensitive=False
        )

    # Step 1; Handle downloaded .mp3 file.
    def on_created(self, event: FileSystemEvent) -> None:
        logger.info(
            f"[mp3] Watchdog receieved {event.event_type} event: {event.src_path}"
        )

    # Step 4; Delete .mp3 file after the .csv transcript has been generated.
    def on_deleted(self, event: FileSystemEvent) -> None:
        logger.info(
            f"[mp3] Watchdog receieved {event.event_type} event: {event.src_path}"
        )


def main():
    src_path = "files"

    observer = Observer()
    observer.schedule(Mp3Handler(), path=src_path, recursive=True)
    observer.schedule(CsvHandler(), path=src_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nQuitting...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
