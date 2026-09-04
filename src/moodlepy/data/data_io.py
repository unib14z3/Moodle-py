import json
import logging
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
logger = logging.getLogger(__name__)


def read_from(file_name: str):
    file_path = DATA_DIR / file_name
    try:
        with file_path.open("r", encoding="utf-8") as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        logger.warning("%s not found. Please generate it first.", file_name)
        return []
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in %s: %s", file_name, exc)
        return []


def write_to(file_name: str, data) -> None:
    file_path = DATA_DIR / file_name
    with file_path.open("w", encoding="utf-8") as data_file:
        json.dump(data, data_file)


def save_course_data(course_data) -> None:
    write_to("course_db.json", course_data)


def load_course_data():
    return read_from("course_db.json")


def load_events_data():
    return read_from("event_db.json")
