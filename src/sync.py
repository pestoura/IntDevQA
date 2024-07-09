import argparse
import shutil
import os
import time
import logging

def sync_folders(source_dir, replica_dir, interval, log_file):
    # Configurar o logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Verificar se já existe um manipulador para a console
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        # Adicionar um manipulador para log para a saída da console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)

    logger.info(f"Iniciando sincronização de {source_dir} para {replica_dir} com intervalo de {interval} segundos.")

    while True:
        try:
            # Lógica de sincronização
            for root, _, files in os.walk(source_dir):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file_path, source_dir)
                    dst_file_path = os.path.join(replica_dir, rel_path)

                    # Exemplo: Copiar arquivo de origem para réplica
                    shutil.copy2(src_file_path, dst_file_path)
                    logger.info(f"Arquivo copiado: {src_file_path} para {dst_file_path}")

            logger.info("Sincronização completa.")

            # Aguardar o intervalo especificado
            time.sleep(interval)

        except Exception as e:
            logger.error(f"Erro durante a sincronização: {str(e)}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de sincronização de diretórios")
    parser.add_argument("source_dir", help="Caminho para o diretório de origem")
    parser.add_argument("replica_dir", help="Caminho para o diretório de réplica")
    parser.add_argument("interval", type=int, help="Intervalo de sincronização em segundos")
    parser.add_argument("log_file", help="Caminho para o arquivo de log")

    args = parser.parse_args()

    sync_folders(args.source_dir, args.replica_dir, args.interval, args.log_file)
