import logging
import datetime

current_datetime=datetime.datetime.now()
str_date = current_datetime.strftime("%d%m%Y%H%M%S")

logging.basicConfig(filename=('Logs/script_execution'+ str_date +'.log'), level=logging.DEBUG)
    
def get_logger():
    return logging
        
        