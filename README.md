# Internal Development in QA (SDET)

This Python script facilitates one-way synchronization of two folders: a source folder and a replica folder. The synchronization ensures that the replica folder maintains an identical copy of the source folder's contents, handling file creations, updates, and deletions as necessary.

## Project Structure and Conventions

IntDevQA/  
│  
├── src/  
│   ├── __init__.py  
│   └── sync.py  
│  
├── tests/  
│   ├── __init__.py  
│   └── test_sync.py  
│  
├── README.md  
├── requirements.txt  
└── setup.py 

## Features

- **One-way Synchronization**: Automatically updates the replica folder to match the source folder's content.
- **Periodic Execution**: Synchronization process runs at intervals specified by the user.
- **Logging**: Detailed logs of file operations (create, copy, delete) are generated to a specified log file and console output.
- **Command Line Arguments**: Configure source folder path, replica folder path, synchronization interval, and log file path via command line arguments.
- **Python Modules Used**: `os`, `shutil`, `time`, `argparse`, `logging`, `hashlib`, `subprocess`.

## How to Use

1. **Clone Repository:** Clone this repository to your local machine.
   
   ```bash
   git clone https://github.com/pestoura/IntDevQA.git

2. **Navigate to Directory:** Enter the project directory.
   ```bash
   cd IntDevQA

3. **Install Dependencies:** Install the necessary dependencies listed in requirements.txt. It's recommended to do this in a virtual environment.
   ```bash
   pip install -r requirements.txt

4. **Run the Script:** Execute the synchronization script with required command line arguments.
    ```bash
    python src/sync.py /path/to/source /path/to/replica 60 /path/to/logfile.log
 Replace **/path/to/source**, **/path/to/replica**, 60, and **/path/to/logfile.log** with appropriate values for your setup.

## Running Tests
To run the unit tests, use the following command:
    ```bash
    python -m unittest discover -s tests
    
The tests will verify the following functionalities:

`*`**File Creation:** Checks if files created in the source directory are copied to the replica directory.  

`*`**File Deletion:** Checks if files deleted from the source directory are removed from the replica directory. 

`*`**File Update:** Checks if files updated in the source directory are updated in the replica directory.  

`*`**Logging:** Verifies that log entries are recorded correctly after synchronization, including creation, deletion, and update of files.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
