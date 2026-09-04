import json
import logging
from datetime import UTC, datetime, timedelta, timezone

from moodlepy import client
from moodlepy.api import assignments, courses
from moodlepy.data import data_io, temporal_utils

moodle = client.MoodleClient()

IST_TIMEZONE = timezone(timedelta(hours=5, minutes=30))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("moodle_py")


def get_site_info():
    logger.info("Checking user info...")
    try:
        return moodle.call("core_webservice_get_site_info")
    except Exception:  # pragma: no cover - protects the command-line entry point
        logger.exception("Could not get site info")
        return {}


class Sem:
    def __init__(self, sdt, edt):
        self.start_dt: datetime = sdt
        self.end_dt: datetime = edt
        self.course_ids: list = []

    def add_course(self, course_id: int) -> None:
        self.course_ids.append(course_id)

    def remove_course(self, course_id: int) -> None:
        self.course_ids.pop(course_id)

    def display_courses(self) -> None:
        print(f"Courses in this semester: {self.course_ids}")


def start_dt(course_data):
    course_sdt = {}

    for item in course_data:
        if isinstance(item, dict) and "id" in item:
            startdate = item.get("startdate")
            if startdate:
                utc_dt = datetime.fromtimestamp(startdate, tz=UTC)
                ist_dt = utc_dt.astimezone(IST_TIMEZONE)
                course_sdt[item["id"]] = ist_dt
            else:
                course_sdt[item["id"]] = None

    logger.info("Course start dates:")
    msg = ["Printing enrolled course IDs:", "ID: start date"]
    for course_id, start_dt in course_sdt.items():
        if start_dt is not None:
            msg.append(f"{course_id}: {start_dt.strftime('%d-%m-%Y %H:%M:%S')}")
        else:
            msg.append(f"{course_id}: No start date")

    logger.info("\n".join(msg))
    return course_sdt

def generate_semesters():
    """Create semesters from event data stored in ``event_db.json``."""
    events = data_io.load_events_data()

    sem_dict = {}
    if isinstance(events, dict):
        semester_items = events.get("sems", events)
    else:
        semester_items = events

    if isinstance(semester_items, dict):
        for sem_name, sem_info in semester_items.items():

            if not isinstance(sem_info, dict):
                continue

            start_date_str = sem_info.get("startdate")
            end_date_str = sem_info.get("enddate")

            if not (start_date_str and end_date_str):
                continue

            start_dt = temporal_utils.str_to_ist(start_date_str)
            end_dt = temporal_utils.str_to_ist(end_date_str)
            sem_dict[sem_name] = Sem(start_dt, end_dt)

    else:
        logger.warning(
            "Unsupported semester data format: %s",
            type(semester_items).__name__,
        )

    logger.info("Loaded %d semesters", len(sem_dict))
    return sem_dict

def sort_by_sem(course_dates, sem_dict):
    for course_id, start_dt in course_dates.items():
        if start_dt is None:
            logger.warning("Course %s has no start date. Skipping.", course_id)
            continue

        assigned = False
        for sem in sem_dict.values():
            if sem.start_dt <= start_dt <= sem.end_dt:
                sem.add_course(course_id)
                assigned = True
                break

        if not assigned:
            logger.warning(
                "Course %s with start date %s does not fall into any semester.",
                course_id,
                start_dt,
            )

    return sem_dict


def fetch_and_save_courses(user_id):
    """Fetch the user's courses from Moodle and persist them locally."""
    course_data = courses.get_enrolled_courses(moodle, user_id)
    if not isinstance(course_data, list):
        logger.error("Moodle returned invalid course data: %r", course_data)
        return []

    data_io.save_course_data(course_data)
    logger.info("Saved %d enrolled courses", len(course_data))
    return course_data


def get_course_ids(course_data):
    """Return valid Moodle course IDs from an enrolled-course response."""
    return [
        course["id"]
        for course in course_data
        if isinstance(course, dict) and course.get("id") is not None
    ]


def run_tests():
    """Fetch Moodle data, save the course database, and display assignments."""
    site_info = get_site_info()
    user_id = site_info.get("userid")
    if user_id is None:
        logger.error("Could not determine the Moodle user ID.")
        return

    logger.info("User ID: %s", user_id)
    course_data = fetch_and_save_courses(user_id)
    course_ids = get_course_ids(course_data)

    if not course_ids:
        logger.info("No enrolled courses found.")
        return

    semesters = generate_semesters()
    if semesters:
        sort_by_sem(start_dt(course_data), semesters)

    assignment_data = assignments.get_all_assignments(moodle, course_ids)
    print(json.dumps(assignment_data, indent=4))
    logger.info("Execution finished.")


if __name__ == "__main__":
    run_tests()
