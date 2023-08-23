import os
import sys
import inspect
import datetime

current_dir = os.getcwd()
test_data_dir = "{}/test_data".format( current_dir )
test_today_data_get_error_message = "test_today_data_get/data_get.py"

def show_erroe_message( test_dir, message ):
    print( test_dir )
    print( message )
