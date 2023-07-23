import os
import shutil
from unittest import TestCase

from util.file_system_emulator import FileSystemEmulator


class TestFileSystemEmulator(TestCase):
    def setUp(self):
        self.fs = FileSystemEmulator("test", "test_delete")

    def tearDown(self) -> None:
        # clear test folders
        shutil.rmtree(self.fs.directory)
        shutil.rmtree(self.fs.deleted_directory)

    def test_add_random_sample(self):
        sample = self.fs.add_random_sample()
        self.assertIsNotNone(sample)

    def test_read_files(self):
        sample1 = self.fs.add_random_sample()
        sample2 = self.fs.add_random_sample()
        sample3 = self.fs.add_random_sample()
        samples = self.fs.read_files()

        self.assertIn(sample1, samples)
        self.assertIn(sample2, samples)
        self.assertIn(sample3, samples)
        self.assertEqual(3, len(samples))

    def test_soft_delete_file(self):
        sample1 = self.fs.add_random_sample()
        sample_exists = os.path.exists(f"{self.fs.directory}/{sample1}")

        # assert file was added to the folder
        self.assertTrue(sample_exists)

        self.fs.soft_delete_file(sample1)
        sample_exists = os.path.exists(f"{self.fs.directory}/{sample1}")

        # assert file doesn't exist anymore in the main directory
        self.assertFalse(sample_exists)

        sample_deleted = os.path.exists(f"{self.fs.deleted_directory}/{sample1}")

        # assert it exists in the directory of deleted files
        self.assertTrue(sample_deleted)

    def test_clear_directory(self):
        self.fs.add_random_sample()
        self.fs.add_random_sample()

        # there should be two files in the main directory
        files = self.fs.read_files()
        self.assertEqual(2, len(files))

        self.fs.clear_directory(self.fs.directory)
        files = self.fs.read_files()

        self.assertEqual(0, len(files))
    def test_read_content(self):
        sample = self.fs.add_random_sample()
        self.fs.read_content(sample)
        self.assertIsNotNone(sample)
        self.assertIsInstance(sample, str)
