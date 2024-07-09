import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
import logging
import time
import sys

# Adicione o diretório 'src' ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import sync  # Importa o script sync.py do diretório src

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
        sync.setup_logging(self.log_file)
        self.assertTrue(os.path.exists(self.log_file))

    def test_sync_folders(self):
        sync.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir, 'test.txt')))

    @patch('sync.shutil.copy2', side_effect=Exception("Mocked error"))
    def test_sync_folders_error_handling(self, mock_copy):
        with self.assertRaises(Exception):
            sync.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        with open(self.log_file, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn('Error during synchronization', log_contents)
            self.assertIn('Mocked error', log_contents)

if __name__ == '__main__':
    unittest.main()

