import os
import unittest
import tempfile
import shutil
import logging
from src.sync import sync_folders  # Assuming sync_folders is defined in src.sync

class TestFolderSync(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for source and replica
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()
        self.log_file = tempfile.mktemp()

        # Set up logging
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        # Remove temporary directories and log file
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_file_creation(self):
        # Create a file in the source directory
        test_file_path = os.path.join(self.source_dir, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is a test file.')

        # Run synchronization
        sync_folders(self.source_dir, self.replica_dir, self.logger)

        # Check if the file was copied to the replica directory
        replica_file_path = os.path.join(self.replica_dir, 'test_file.txt')
        self.assertTrue(os.path.exists(replica_file_path))

        # Check if the contents are the same
        with open(replica_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'This is a test file.')

    def test_file_deletion(self):
        # Create a file in the source and replica directories
        test_file_path = os.path.join(self.source_dir, 'test_file.txt')
        replica_file_path = os.path.join(self.replica_dir, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is a test file.')
        shutil.copy2(test_file_path, replica_file_path)

        # Delete the file from the source directory
        os.remove(test_file_path)

        # Run synchronization
        sync_folders(self.source_dir, self.replica_dir, self.logger)

        # Check if the file was deleted from the replica directory
        self.assertFalse(os.path.exists(replica_file_path))

    def test_file_update(self):
        # Create a file in the source directory
        test_file_path = os.path.join(self.source_dir, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is the original file.')

        # Run initial synchronization
        sync_folders(self.source_dir, self.replica_dir, self.logger)

        # Update the file in the source directory
        with open(test_file_path, 'w') as f:
            f.write('This is the updated file.')

        # Run synchronization
        sync_folders(self.source_dir, self.replica_dir, self.logger)

        # Check if the file was updated in the replica directory
        replica_file_path = os.path.join(self.replica_dir, 'test_file.txt')
        with open(replica_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'This is the updated file.')

    def test_logging(self):
        # Create a file in the source directory
        test_file_path = os.path.join(self.source_dir, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is a test file.')

        # Run synchronization
        sync_folders(self.source_dir, self.replica_dir, self.logger)

        # Check if log file contains the expected log entries
        with open(self.log_file, 'r') as log:
            log_content = log.read()
        self.assertIn('Synchronization complete', log_content)
        self.assertIn('Copied file', log_content)  # Adjust according to your actual log messages

if __name__ == '__main__':
    unittest.main()

