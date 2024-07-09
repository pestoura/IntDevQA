# Internal Development in QA (SDET) 
This Python script facilitates one-way synchronization of two folders: a source folder and a replica folder. The synchronization ensures that the replica folder maintains an identical copy of the source folder's contents, handling file creations, updates, and deletions as necessary.

## Features

- **One-way Synchronization**: Automatically updates the replica folder to match the source folder's content.
- **Periodic Execution**: Synchronization process runs at intervals specified by the user.
- **Logging**: Detailed logs of file operations (create, copy, delete) are generated to a specified log file and console output.
- **Command Line Arguments**: Configure source folder path, replica folder path, synchronization interval, and log file path via command line arguments.
- **Python Modules Used**: `os`, `shutil`, `time`, `argparse`, `logging`, `filecmp`.

## How to Use

1. **Clone Repository**: Clone this repository to your local machine.

   ```bash
   git clone https://github.com/pestoura/IntDevQA.git

# Project Structure and Conventions

folder-sync/  
│  
├── src/  
│ ├── init.py  
│ └── sync.py  
│  
├── tests/  
│ ├── init.py  
│ └── test_sync.py  
│  
├── README.md  
├── requirements.txt  
└── setup.py  

# How to Use
Clone Repository: Clone this repository to your local machine.

git clone https://github.com/your-username/folder-sync.git

Navigate to Directory: Enter the project directory.
cd folder-sync

Run the Script: Execute the synchronization script with required command line arguments.
python src/sync.py /path/to/source /path/to/replica 60 /path/to/logfile.log
Replace /path/to/source, /path/to/replica, 60, and 
