# src/sync.py

import os
import shutil
import time
import argparse
import logging
import hashlib
from filecmp import dircmp

# Initialize logger
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
    Synchronize source folder to replica folder.

    Args:
        source (str): Path to the source folder.
        replica (str): Path to the replica folder.
    """
    comparison = dircmp(source, replica)
    copy_files_and_dirs(comparison, source, replica)
    remove_extra_files_and_dirs(comparison, replica)
    logger.info('Synchronization complete')

def copy_files_and_dirs(comparison, source, replica):
    """
    Copy files and directories from source to replica based on comparison.

    Args:
        comparison (filecmp.dircmp): Comparison object between source and replica.
        source (str): Path to the source folder.
        replica (str): Path to the replica folder.
    """
    for file_name in comparison.left_only:
        src_path = os.path.join(source, file_name)
        dst_path = os.path.join(replica, file_name)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
            logger.info(f"Directory created: {dst_path}")
        else:
            shutil.copy2(src_path, dst_path)
            logger.info(f"File copied: {dst_path}")

    for file_name in comparison.diff_files:
        src_path = os.path.join(source, file_name)
        dst_path = os.path.join(replica, file_name)
        shutil.copy2(src_path, dst_path)
        logger.info(f"File updated: {dst_path}")

    for common_dir in comparison.common_dirs:
        new_source = os.path.join(source, common_dir)
        new_replica = os.path.join(replica, common_dir)
        sync_folders(new_source, new_replica)

def remove_extra_files_and_dirs(comparison, replica):
    """
    Remove files and directories from replica that are not in source.

    Args:
        comparison (filecmp.dircmp): Comparison object between source and replica.
        replica (str): Path to the replica folder.
    """
    for file_name in comparison.right_only:
        path = os.path.join(replica, file_name)
        if os.path.isdir(path):
            shutil.rmtree(path)
            logger.info(f"Directory removed: {path}")
        else:
            os.remove(path)
            logger.info(f"File removed: {path}")

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
    while True:
        try:
            sync_folders(args.source, args.replica)
        except Exception as e:
            logger.error(f"Error during synchronization: {e}")
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
