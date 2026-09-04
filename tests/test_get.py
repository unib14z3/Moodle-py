import unittest
from unittest.mock import Mock

from moodlepy.api.assignments import get_all_assignments, get_assignments_for_course
from moodlepy.api.courses import (
    get_course_contents,
    get_course_info,
    get_enrolled_courses,
)


class AssignmentFetchTests(unittest.TestCase):
    def test_fetches_assignments_for_one_course(self):
        client = Mock()
        response = {"courses": [{"id": 12, "assignments": []}]}
        client.call.return_value = response

        result = get_assignments_for_course(client, 12)

        self.assertEqual(result, response)
        client.call.assert_called_once_with(
            "mod_assign_get_assignments", {"courseids": [12]}
        )

    def test_fetches_and_groups_assignments_for_each_course(self):
        client = Mock()
        client.call.side_effect = [{"course": 12}, {"course": 34}]

        result = get_all_assignments(client, [12, 34])

        self.assertEqual(result, {12: {"course": 12}, 34: {"course": 34}})
        self.assertEqual(
            client.call.call_args_list,
            [
                unittest.mock.call("mod_assign_get_assignments", {"courseids": [12]}),
                unittest.mock.call("mod_assign_get_assignments", {"courseids": [34]}),
            ],
        )

    def test_accepts_a_single_course_id(self):
        client = Mock()
        client.call.return_value = {"course": 12}

        result = get_all_assignments(client, 12)

        self.assertEqual(result, {12: {"course": 12}})
        client.call.assert_called_once_with(
            "mod_assign_get_assignments", {"courseids": [12]}
        )


class CourseFetchTests(unittest.TestCase):
    def setUp(self):
        self.client = Mock()

    def test_get_enrolled_courses_uses_user_id(self):
        self.client.call.return_value = [{"id": 12}]

        self.assertEqual(get_enrolled_courses(self.client, 99), [{"id": 12}])
        self.client.call.assert_called_once_with(
            "core_enrol_get_users_courses", {"userid": 99}
        )

    def test_get_course_info_uses_course_id_field(self):
        self.client.call.return_value = {"courses": [{"id": 12}]}

        self.assertEqual(get_course_info(self.client, 12), {"courses": [{"id": 12}]})
        self.client.call.assert_called_once_with(
            "core_course_get_courses_by_field", {"field": "id", "value": 12}
        )

    def test_get_course_contents_uses_course_id(self):
        self.client.call.return_value = [{"id": 7}]

        self.assertEqual(get_course_contents(self.client, 12), [{"id": 7}])
        self.client.call.assert_called_once_with(
            "core_course_get_contents", {"courseid": 12}
        )
