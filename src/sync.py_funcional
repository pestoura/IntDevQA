import argparse
import shutil
import os
import time
import logging
import hashlib

def setup_logging(log_file):
    """
    Set up logging configuration to log to both console and file.

    Args:
    - log_file (str): Path to the log file.
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def calculate_file_hash(file_path):
    """
    Calculate the SHA-256 hash of a file.

    Args:
    - file_path (str): Path to the file.

    Returns:
    - str: Hexadecimal representation of the hash.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def sync_folders(source_dir, replica_dir, interval, log_file):
    """
    Synchronize folders from source directory to replica directory at specified intervals.

    Args:
    - source_dir (str): Path to source directory.
    - replica_dir (str): Path to replica directory.
    - interval (int): Synchronization interval in seconds.
    - log_file (str): Path to the log file.

    Raises:
    - Exception: If any error occurs during synchronization.
    """
    setup_logging(log_file)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting synchronization from {source_dir} to {replica_dir} with interval of {interval} seconds.")

    while True:
        try:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file_path, source_dir)
                    dst_file_path = os.path.join(replica_dir, rel_path)

                    src_hash = calculate_file_hash(src_file_path)
                    dst_hash = calculate_file_hash(dst_file_path) if os.path.exists(dst_file_path) else None

                    if src_hash != dst_hash:
                        shutil.copy2(src_file_path, dst_file_path)
                        logger.info(f"File copied: {src_file_path} to {dst_file_path}")
                    else:
                        logger.debug(f"File {src_file_path} unchanged, skipping copy.")

            logger.info("Synchronization complete.")

            time.sleep(interval)

        except Exception as e:
            logger.error(f"Error during synchronization: {str(e)}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory synchronization script")
    parser.add_argument("source_dir", help="Path to source directory")
    parser.add_argument("replica_dir", help="Path to replica directory")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    sync_folders(args.source_dir, args.replica_dir, args.interval, args.log_file)
