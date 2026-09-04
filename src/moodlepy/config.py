import os
import tomllib
from datetime import timedelta, timezone
from pathlib import Path


def load_environment_file(file_path: Path) -> None:
    """Load simple KEY=VALUE entries without replacing existing variables."""
    if not file_path.exists():
        return

    for line in file_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent.parent
load_environment_file(PROJECT_ROOT / ".env")

with PACKAGE_DIR.joinpath("config.toml").open("rb") as config_file:
    CONFIG = tomllib.load(config_file)

MOODLE_URL = os.environ["MOODLE_URL"]
MOODLE_TOKEN = os.environ["MOODLE_TOKEN"]
TIMEZONE = CONFIG["TimeZone"]
_sign = -1 if TIMEZONE.startswith("UTC-") else 1
_hours, _minutes = TIMEZONE.removeprefix("UTC+").removeprefix("UTC-").split(":")
IST_TZ = timezone(
    _sign * timedelta(hours=int(_hours), minutes=int(_minutes)), name=TIMEZONE
)
