# read about sys package 
from src.logger import logging
import sys 

def error_message_details(error,error_detail:sys):
    # the last variable (exc_tb) will include which line and folder the error is happened
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in pythn script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno,str(error))
    return error_message

class CustomerException(Exception):
    def __init__(self, error_message, error_detail:sys):
        # we creating error message variable to hold the error 
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    
