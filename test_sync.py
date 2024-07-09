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

    def test_sync_folders_directories_exist(self):
        # Executar sincronização
        sync.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        # Verificar se o diretório de origem e o diretório réplica existem
        self.assertTrue(os.path.exists(self.source_dir))
        self.assertTrue(os.path.exists(self.replica_dir))

    def test_sync_folders_interval(self):
        interval = 2  # Intervalo de sincronização de 2 segundos
        sync.sync_folders(self.source_dir, self.replica_dir, interval, self.log_file)
        time.sleep(interval + 1)  # Aguardar intervalo + 1 segundo

        # Verificar se a sincronização ocorreu ao menos uma vez no intervalo especificado
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir, 'test.txt')))

    def test_sync_folders_clean_replica(self):
        # Criar um arquivo pré-existente no diretório réplica
        test_file = os.path.join(self.replica_dir, 'existing_file.txt')
        with open(test_file, 'w') as f:
            f.write("Existing file content")

        # Executar sincronização
        sync.sync_folders(self.source_dir, self.replica_dir, 1, self.log_file)

        # Verificar se o arquivo pré-existente foi removido
        self.assertFalse(os.path.exists(test_file))


if __name__ == '__main__':
    unittest.main()
