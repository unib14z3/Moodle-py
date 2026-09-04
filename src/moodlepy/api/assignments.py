import logging

from moodlepy import client

logger = logging.getLogger(__name__)


def get_assignments_for_course(client: client.MoodleClient, course_id: int):
    """Fetch assignments for one course using the Moodle API."""
    logger.info("Fetching assignments for course %s.", course_id)

    assignments = client.call("mod_assign_get_assignments", {"courseids": [course_id]})
    return assignments


def get_all_assignments(client: client.MoodleClient, course_ids: int | list[int]):
    """Fetch assignments for one or more courses, keyed by course ID."""
    logger.info("Fetching assignments for courses %s.", course_ids)

    if isinstance(course_ids, int):
        course_ids = [course_ids]

    all_assignments = {}
    for course_id in course_ids:
        assignments = get_assignments_for_course(client, course_id)
        all_assignments[course_id] = assignments
    return all_assignments
