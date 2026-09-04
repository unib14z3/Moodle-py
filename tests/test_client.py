import unittest

from moodlepy.client import TOKEN, MoodleClient


class BuildRequestParamsTests(unittest.TestCase):
    def test_lists_are_encoded_as_moodle_array_params(self):
        params = MoodleClient().build_request_params(
            "mod_assign_get_assignments", {"courseids": [6558], "userid": 10093}
        )

        self.assertEqual(params[0], ("wstoken", TOKEN))
        self.assertEqual(params[1], ("wsfunction", "mod_assign_get_assignments"))
        self.assertEqual(params[2], ("moodlewsrestformat", "json"))
        self.assertIn(("courseids[0]", 6558), params)
        self.assertIn(("userid", 10093), params)


if __name__ == "__main__":
    unittest.main()
