import logging
import os
#from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


# Setup logging
def log_init():
    # Create a logs directory if it does not exist
    logs_directory = 'logs'
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Define the log files pattern with a custom date format
    #log_files_pattern = os.path.join(logs_directory, f"bot_{datetime.now().strftime('%Y-%m-%d')}.log")
    log_files_pattern = os.path.join(logs_directory, f"bot.log")

    # Setup logging with TimedRotatingFileHandler
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %Z',
        handlers=[
            TimedRotatingFileHandler(log_files_pattern, when="midnight", interval=1, backupCount=7),  # Rotates daily, keeps 7 days of logs
            logging.StreamHandler()  # Outputs logs to the console
        ]
    )
    return