import unittest
from unittest.mock import patch, MagicMock, mock_open
import logging
import os
import hashlib
import shutil

from src.sync import setup_logging, calculate_file_hash, sync_folders

class TestSyncFolders(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test.log'
        self.source_dir = 'source'
        self.replica_dir = 'replica'
        self.interval = 1
        
        # Cria diretórios temporários para os testes
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.replica_dir, exist_ok=True)

    def tearDown(self):
        # Remove diretórios temporários após os testes
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_setup_logging(self):
        setup_logging(self.log_file)
        logger = logging.getLogger()
        
        self.assertEqual(len(logger.handlers), 2)
        self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers))
        self.assertTrue(any(isinstance(handler, logging.FileHandler) for handler in logger.handlers))

    def test_calculate_file_hash(self):
        file_content = b"test content"
        file_path = os.path.join(self.source_dir, "test.txt")
        with open(file_path, 'wb') as f:
            f.write(file_content)

        expected_hash = hashlib.sha256(file_content).hexdigest()
        calculated_hash = calculate_file_hash(file_path)

        self.assertEqual(expected_hash, calculated_hash)

    @patch('src.sync.os.walk')
    @patch('src.sync.shutil.copy2')
    @patch('src.sync.calculate_file_hash')
    @patch('src.sync.time.sleep', return_value=None)
    def test_sync_folders(self, mock_sleep, mock_calculate_file_hash, mock_copy2, mock_os_walk):
        # Simula os arquivos retornados por os.walk
        mock_os_walk.return_value = [
            (self.source_dir, [], ['test1.txt', 'test2.txt'])
        ]

        # Simula o cálculo do hash para os arquivos
        def mock_file_hash_side_effect(file_path):
            return {
                os.path.join(self.source_dir, 'test1.txt'): 'hash1',
                os.path.join(self.source_dir, 'test2.txt'): 'hash2',
                os.path.join(self.replica_dir, 'test1.txt'): 'hash1',  # Simula que o arquivo já existe no destino com o mesmo hash
            }.get(file_path, None)
        
        mock_calculate_file_hash.side_effect = mock_file_hash_side_effect

        # Executa a função de sincronização
        with patch('src.sync.open', mock_open()) as mocked_file:
            sync_folders(self.source_dir, self.replica_dir, self.interval, self.log_file, max_iterations=1)
        
        # Verifica se shutil.copy2 foi chamado corretamente
        mock_copy2.assert_any_call(os.path.join(self.source_dir, 'test1.txt'), os.path.join(self.replica_dir, 'test1.txt'))
        mock_copy2.assert_any_call(os.path.join(self.source_dir, 'test2.txt'), os.path.join(self.replica_dir, 'test2.txt'))
        self.assertEqual(mock_copy2.call_count, 2)  # Verifica se copy2 foi chamado duas vezes

    @patch('src.sync.os.walk')
    @patch('src.sync.shutil.copy2')
    @patch('src.sync.calculate_file_hash')
    @patch('src.sync.time.sleep', return_value=None)
    @patch('src.sync.logging.getLogger')
    def test_sync_folders_error_handling(self, mock_get_logger, mock_sleep, mock_calculate_file_hash, mock_copy2, mock_os_walk):
        mock_os_walk.side_effect = Exception("Test error")

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with self.assertRaises(Exception):
            sync_folders(self.source_dir, self.replica_dir, self.interval, self.log_file, max_iterations=1)
        
        mock_logger.error.assert_called_once_with("Error during synchronization: Test error")

if __name__ == '__main__':
    unittest.main()
