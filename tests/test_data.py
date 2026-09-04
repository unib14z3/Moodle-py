import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from moodlepy.data import data_io


class DataIoTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)
        self.data_dir_patch = patch.object(data_io, "DATA_DIR", self.data_dir)
        self.data_dir_patch.start()

    def tearDown(self):
        self.data_dir_patch.stop()
        self.temp_dir.cleanup()

    def test_write_to_and_read_from_round_trip_json_data(self):
        expected = {"courses": [{"id": 12, "name": "Physics"}]}

        data_io.write_to("sample.json", expected)

        self.assertEqual(data_io.read_from("sample.json"), expected)
        saved_data = json.loads(
            (self.data_dir / "sample.json").read_text(encoding="utf-8")
        )
        self.assertEqual(saved_data, expected)

    def test_read_from_missing_file_returns_empty_list(self):
        with self.assertLogs(data_io.logger, level="WARNING"):
            self.assertEqual(data_io.read_from("missing.json"), [])

    def test_save_and_load_course_data_use_course_database(self):
        expected = [{"id": 12, "fullname": "Physics"}]

        data_io.save_course_data(expected)

        self.assertEqual(data_io.load_course_data(), expected)

    def test_load_events_data_reads_event_database(self):
        expected = [{"id": 5, "name": "Exam"}]
        (self.data_dir / "event_db.json").write_text(
            json.dumps(expected), encoding="utf-8"
        )

        self.assertEqual(data_io.load_events_data(), expected)
