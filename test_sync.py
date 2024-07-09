import os
import shutil
import time
import logging

def setup_logging(log_file):
    """Configura o logging para escrever em um arquivo específico."""
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sync_folders(source_dir, replica_dir, interval, log_file):
    """Sincroniza o conteúdo do diretório de origem com o diretório réplica em intervalos regulares."""
    setup_logging(log_file)
    logging.info(f'Starting synchronization from {source_dir} to {replica_dir} with interval of {interval} seconds.')

    try:
        while True:
            # Implemente a lógica de sincronização aqui
            for filename in os.listdir(source_dir):
                source_file = os.path.join(source_dir, filename)
                if os.path.isfile(source_file):
                    target_file = os.path.join(replica_dir, filename)
                    shutil.copy2(source_file, target_file)
                    logging.info(f'Copied {source_file} to {target_file}')
            
            logging.info('Synchronization complete.')
            time.sleep(interval)

    except KeyboardInterrupt:
        logging.info('Synchronization interrupted by user.')
    except Exception as e:
        logging.error(f'Error during synchronization: {e}')
        raise

if __name__ == "__main__":
    source_dir = "/tmp/tmpelvh5wlo"
    replica_dir = "/tmp/tmpnn9nfb02"
    interval = 1
    log_file = "/tmp/sync_log.txt"

    sync_folders(source_dir, replica_dir, interval, log_file)
