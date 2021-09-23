from datetime import datetime
import os
import sys
import platform

# global variable to store log file name for access from anywhere within application.
logger_file_name = ""
current_directory = ""

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")

def get_datetime_string() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_datetime_full_string() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def initalise_logging_session():

    if platform.system() == 'Darwin':
        path = __file__
    else:
        path = sys.argv[0]

    global current_directory
    current_directory = os.path.split(path)[0]

    global logger_file_name
    logger_file_name = f"peakmlviewerpy_log_{get_datetime_string()}.txt"

    # Create log file
    r = open(os.path.join(current_directory,logger_file_name), "w", encoding='utf-8')

    r.write(f"PeakMLViewerPy Log - for session beginning {get_datetime_full_string()}")
    r.write("\n")
    r.write(f"=========================================================================")

    r.close()

def log_error(details: str):
    add_log_record_to_file(details, "ERROR")

def log_progress(details: str):
    add_log_record_to_file(details, "PROGRESS")

def log_actions(details: str):
    add_log_record_to_file(details, "ACTION")

def add_log_record_to_file(details: str, type: str):

    global current_directory
    # Skip if not currently in session (e.g. during automated testing)
    if current_directory != "":

        log_entry = f"{get_current_time()}: {type}: {details}"

        #Open file in append mode
        r = open(os.path.join(current_directory,logger_file_name), "a", encoding='utf-8')

        # Add newline
        r.write("\n")

        # Add log entry
        r.write(log_entry)
        r.close()


def get_log():
    f = open(os.path.join(current_directory,logger_file_name), "r", encoding='utf-8')
    return f.read()



