# Features

## Moodle REST client

- Sends Moodle REST requests with a token, web-service function name, and JSON
  response format.
- Encodes list parameters in Moodle's indexed-array format, such as
  `courseids[0]` and `courseids[1]`.
- Uses a 15-second HTTP timeout.
- Returns a structured error dictionary when a request fails or Moodle returns
  invalid JSON.

## Course support

- Retrieves the courses in which a user is enrolled.
- Retrieves course information by course ID.
- Retrieves the contents of a course.
- Extracts valid course IDs from Moodle course responses.

## Assignment support

- Retrieves assignments for a single course.
- Retrieves assignments for one or more courses and returns results keyed by
  course ID.

## Local data and time utilities

- Stores and loads enrolled-course data in `data/course_db.json`.
- Loads semester event data from `data/event_db.json`.
- Handles missing or malformed JSON files without terminating the application.
- Converts Unix timestamps and formatted date strings to the timezone defined
  in `config.toml`.
- Groups enrolled courses into configured semester date ranges.

## Configuration and testing

- Loads Moodle URL and token values from `.env` without overwriting existing
  environment variables.
- Reads timezone and semester-date configuration from `config.toml`.
- Includes unit tests for request construction, course and assignment helpers,
  and local data persistence.
