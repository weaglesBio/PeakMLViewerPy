from datetime import datetime

# global variable to store log file name for access from anywhere within application.
logger_file_name = ""

def get_current_time():
    return datetime.now().strftime("%H:%M:%S.%f")

def get_datetime_string():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_datetime_full_string():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def initalise_logging_session():
#    self._log_records = []
    global logger_file_name
    logger_file_name = f"peakmlviewerpy_log_{get_datetime_string()}.txt"

    # Create log file
    r = open(logger_file_name, "w")

    r.write(f"PeakMLViewerPy Log - for session beginning {get_datetime_full_string()}")
    r.write("\n")
    r.write(f"=========================================================================")

    r.close()

def log_error(details):
    add_log_record_to_file(details, "ERROR")

def log_progress(details):
    add_log_record_to_file(details, "PROGRESS")

def log_actions(details):
    add_log_record_to_file(details, "ACTION")

def add_log_record_to_file(details, type):

    log_entry = f"{get_current_time()}: {type}: {details}"
    print(log_entry)

    #Open file in append mode
    r = open(logger_file_name, "a")

    # Add newline
    r.write("\n")

    # Add log entry
    r.write(log_entry)
    r.close()

def get_log():
    f = open(logger_file_name, "r")
    return f.read()



