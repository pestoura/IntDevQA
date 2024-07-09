import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
import logging
import time

import sync_script  # Assuming the script is named sync_script.py

class TestSyncFolders(unittest.TestCase):
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()
        self.log_file = tempfile.mktemp()

    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        os.remove(self.log_file)

    def test_logging_setup(self):
        sync_script.setup_logging(self.log_file)
        self.assertTrue(os.path.exists(self.log_file))

    def test_sync_folders(self):
        sync_script.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir, 'test.txt')))

    @patch('sync_script.shutil.copy2', side_effect=Exception("Mocked error"))
    def test_sync_folders_error_handling(self, mock_copy):
        with self.assertRaises(Exception):
            sync_script.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        with open(self.log_file, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn('Error during synchronization', log_contents)
            self.assertIn('Mocked error', log_contents)

if __name__ == '__main__':
    unittest.main()

