import logging

from moodlepy import client

logger = logging.getLogger(__name__)


def get_enrolled_courses(client : client.MoodleClient, user_id: int):
    logger.info("Fetching enrolled courses...")
    courses = client.call("core_enrol_get_users_courses", {"userid": user_id})
    return courses


def get_course_info(client : client.MoodleClient, course_id: int):
    logger.info("Fetching course info for course ID %s...", course_id)
    course_info = client.call(
        "core_course_get_courses_by_field", {"field": "id", "value": course_id}
    )
    return course_info


def get_course_contents(client : client.MoodleClient, course_id: int):
    logger.info("Fetching course contents for course ID %s...", course_id)
    course_contents = client.call("core_course_get_contents", {"courseid": course_id})
    return course_contents
