import os
import logging
from pathlib import Path
from data.config import LOG_PATH
from datetime import datetime

def get_today_date():
    today = datetime.today()
    return today.strftime("%d-%m-%Y")


CWD = Path(os.getcwd())
LOG_FILE = os.path.join(CWD, Path(f"{LOG_PATH}/{get_today_date()}.log"))


logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
is_existing_file_handler = os.path.exists(LOG_FILE)

if not is_existing_file_handler:
    with open(LOG_FILE, "a") as f:
        f.write("Start log\n")

file_handler = logging.FileHandler(LOG_FILE)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
