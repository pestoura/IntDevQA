import argparse
import shutil
import os
import time
import logging

def sync_folders(source_dir, replica_dir, interval, log_file):
    """
    Synchronize folders from source directory to replica directory at specified intervals,
    logging operations to both a log file and console.

    Args:
    - source_dir (str): Path to source directory.
    - replica_dir (str): Path to replica directory.
    - interval (int): Synchronization interval in seconds.
    - log_file (str): Path to the log file.

    Raises:
    - Exception: If any error occurs during synchronization.
    """
    # Configure logging to file
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check if a console handler already exists
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        # Add a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)

    logger.info(f"Starting synchronization from {source_dir} to {replica_dir} with interval of {interval} seconds.")

    while True:
        try:
            # Synchronization logic
            for root, _, files in os.walk(source_dir):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file_path, source_dir)
                    dst_file_path = os.path.join(replica_dir, rel_path)

                    # Example: Copy file from source to replica
                    shutil.copy2(src_file_path, dst_file_path)
                    logger.info(f"File copied: {src_file_path} to {dst_file_path}")

            logger.info("Synchronization complete.")

            # Wait for the specified interval
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

    # Ensure log file directory exists
    log_dir = os.path.dirname(args.log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    sync_folders(args.source_dir, args.replica_dir, args.interval, args.log_file)
