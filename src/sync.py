# src/sync.py

import os
import time
import argparse
import logging
import hashlib
import subprocess

# Initialize the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_md5(file_path):
    """
    Calculate the MD5 hash of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: MD5 hash of the file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    """
    Synchronize the source folder with the replica folder using rsync.

    Args:
        source (str): Path to the source folder.
        replica (str): Path to the replica folder.
    """
    try:
        rsync_command = ["rsync", "-av", "--delete", source + "/", replica]
        subprocess.run(rsync_command, check=True)
        logger.info('Synchronization complete')
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during synchronization: {e}")
        logger.error(f"Command executed: {' '.join(rsync_command)}")

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments object.
    """
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('source', help='Source folder path')
    parser.add_argument('replica', help='Replica folder path')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', help='Log file path')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Validate source and replica paths
    if not os.path.isdir(args.source):
        logger.error(f"Source path '{args.source}' is not a valid directory.")
        return
    if not os.path.isdir(args.replica):
        logger.error(f"Replica path '{args.replica}' is not a valid directory.")
        return

    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
