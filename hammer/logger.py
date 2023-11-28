import logging
from datetime import datetime
import pytz
logger = logging.getLogger('common_logging')

# Set up the loggig services
# Create a logger
logger.setLevel(logging.DEBUG)
# #For logging to file
#
#  # Create a file handler
file_handler = logging.FileHandler("./logs.log")
file_handler.setLevel(logging.DEBUG)

 # Create a format for the logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S %Z%z')
formatter.converter = lambda *args: datetime.now(pytz.timezone('Asia/Kolkata')).timetuple()
file_handler.setFormatter(formatter)

 # Add the file handler to the logger
logger.addHandler(file_handler)


##For logging to console
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# # Create a formatter for the log messages
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#
# # Add the formatter to the console handler
# console_handler.setFormatter(formatter)
#
# # Add the console handler to the logger
# logger.addHandler(console_handler)
