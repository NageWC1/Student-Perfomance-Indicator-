# what ever the excution happen we have to store in the log information 
import logging 
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # this will be file name lo
logs_path= os.path.join(os.getcwd(),"logs",LOG_FILE)
# even though there is a file, the log file will be included there 
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,

)


# if __name__ == "__main__":
#     logging.info("Logging Has started")