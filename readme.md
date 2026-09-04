# Moodle-py

Moodle-py is a small Python client for Moodle's REST web-service API. It can
retrieve a user's enrolled courses and course assignments, save course data
locally, and group courses by semester dates.

## Requirements

- Python 3.11 or later
- A Moodle site with web services enabled
- A Moodle web-service token with access to the required functions

## Setup

Create and activate a virtual environment, then install the project:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --editable .
```

Create a local environment file from the template:

```bash
cp .env.example .env
```

Set these values in `.env`:

```dotenv
MOODLE_URL=https://your-moodle.example/webservice/rest/server.php
MOODLE_TOKEN=your_moodle_web_service_token
```

Do not commit `.env`; it contains credentials and is ignored by Git.

## Run

Run the command-line workflow from the project root:

```bash
python -m moodlepy.main
```

The workflow obtains the authenticated user's ID, fetches enrolled courses,
saves them to `src/moodlepy/data/course_db.json`, organizes them by semester,
and prints assignment data as JSON.

Semester dates and the default timezone are configured in
`src/moodlepy/config.toml`. Event and semester data is read from
`src/moodlepy/data/event_db.json`.

## Test

Run the built-in test runner:

```bash
python tests/run_tests.py
```

Alternatively, when the package is not installed, run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Project layout

```text
src/moodlepy/
├── api/       Moodle API helpers for courses and assignments
├── data/      JSON persistence and date/time helpers
├── client.py  REST client and request-parameter builder
├── config.py  Environment and TOML configuration loader
└── main.py    Command-line workflow
```

See [features.md](features.md) for the supported functionality.
