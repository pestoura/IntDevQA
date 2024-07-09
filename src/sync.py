import argparse
import shutil
import os
import time
import logging

def sync_folders(source_dir, replica_dir, interval, log_file):
    # Set up logging
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info(f"Starting synchronization from {source_dir} to {replica_dir} with interval {interval} seconds.")

    while True:
        try:
            # Your synchronization logic here
            for root, _, files in os.walk(source_dir):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file_path, source_dir)
                    dst_file_path = os.path.join(replica_dir, rel_path)

                    # Example: Copy file from source to replica
                    shutil.copy2(src_file_path, dst_file_path)
                    logger.info(f"Copied file: {src_file_path} to {dst_file_path}")

            logger.info("Synchronization complete.")

            # Sleep for the specified interval
            time.sleep(interval)

        except Exception as e:
            logger.error(f"Error during synchronization: {str(e)}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization script")
    parser.add_argument("source_dir", help="Path to source directory")
    parser.add_argument("replica_dir", help="Path to replica directory")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to log file")

    args = parser.parse_args()

    sync_folders(args.source_dir, args.replica_dir, args.interval, args.log_file)
