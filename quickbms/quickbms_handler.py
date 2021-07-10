# Import statements
import subprocess
import os

# Global variables
from StandardFileOperations.PathOperations import recursive_create_folder

current_dir = os.path.abspath(os.path.dirname(__file__))

quickbms_exe = f'{current_dir}/quickbms.exe'

# Command to list the TOC files included within the ELF
# .\quickbms -l "D:\Programming\Git\Github\GameReversing\PS2\Fatal Frame 2\QuickBmsScripts\project_zero.bms"
#               "D:\Reverse\Fatal Frame II\Files\SLUS_207.66" "D:\DecompressFiles\bms\output"


# Available scripts to run
tim2_script = 'tim2.bms'
deless_script = 'deless.bms'


def launch_quickbms_script(script_file_name, scan_folder_for_files, scan_extraction_folder_path, scan_file_extension,
                           scan_file_name, stop_on_errors=False):
    """ Launches a subprocess for extracting file with quickbms, all paths should be absolute for best results
    :param scan_folder_for_files: Folder containing the files to scan for
    :param stop_on_errors: If errors are detected by bms, then this will halt the program
    :param scan_file_name: Name of the file to scan, if scanning for files in a folder, put '{}'
    :param scan_file_extension: Extension of the file, if all extension, put '{}'
    :param scan_extraction_folder_path: Folder where the extracted files will be put
    :param script_file_name: Name of the bms script file
    """

    stop_on_errors_option = ''
    if not stop_on_errors:
        stop_on_errors_option = '-.'

    recursive_create_folder(scan_extraction_folder_path)

    subprocess.run([quickbms_exe, stop_on_errors_option, '-F', f'{scan_file_name}.{scan_file_extension}',
                    f'{current_dir}/scripts/{script_file_name}', scan_folder_for_files, scan_extraction_folder_path])
