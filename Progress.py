# global variable to store log file name for access from anywhere within application.
progress_text_global = ""
progress_value_global = 0

def update_progress(text: str, value: float = None):
    global progress_text_global
    progress_text_global = text

    if value is not None:
        global progress_value_global
        progress_value_global = value