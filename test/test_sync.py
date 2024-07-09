import unittest
from unittest.mock import patch
from src import sync  # Importa o script sync.py do diretório src

class TestSync(unittest.TestCase):
    
    @patch('sync.start_sync')
    def test_sync_started(self, mock_start_sync):
        sync.main()
        mock_start_sync.assert_called_once()

    @patch('sync.start_sync')
    def test_sync_complete(self, mock_start_sync):
        sync.main()
        self.assertTrue(mock_start_sync.called)

    def test_file_existence(self):
        # Aqui você pode adicionar um teste para verificar se os arquivos de sincronização existem
        pass

    def test_sync_interval(self):
        # Aqui você pode adicionar um teste para verificar o intervalo de sincronização
        pass

if __name__ == '__main__':
    unittest.main()
