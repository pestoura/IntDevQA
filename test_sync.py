import unittest
import os
import tempfile
import shutil
import logging
import time
from unittest.mock import patch

import sync_script  # Assuming the script is named sync_script.py

class TestSyncFolders(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()
        
        # Create a temporary log file
        self.log_file = tempfile.mktemp()

    def tearDown(self):
        # Remove temporary directories and log file
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        os.remove(self.log_file)

    def test_logging_setup(self):
        # Test if logging setup function works
        sync_script.setup_logging(self.log_file)

        # Check if log file is created
        self.assertTrue(os.path.exists(self.log_file))

    def test_sync_folders(self):
        # Test basic synchronization functionality
        sync_script.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        # Check if files are copied correctly
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir, 'test.txt')))  # Replace with actual test file name

    @patch('sync_script.shutil.copy2', side_effect=Exception("Mocked error"))
    def test_sync_folders_error_handling(self, mock_copy):
        # Test error handling during synchronization
        with self.assertRaises(Exception):
            sync_script.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        # Check if error is logged
        with open(self.log_file, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn('Error during synchronization', log_contents)
            self.assertIn('Mocked error', log_contents)

if __name__ == '__main__':
    unittest.main()

