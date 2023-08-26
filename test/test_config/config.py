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

def load_test_race_id_list():
    test_race_id_list = []
    f = open( "{}/race_id_list.txt".format( test_data_dir ), "r" )
    all_data = f.readlines()

    for str_data in all_data:
        test_race_id_list.append( str_data.replace( "\n", "" ) )

    return sorted( test_race_id_list )

def load_today_data_race_id_list():
    test_race_id_list = []
    f = open( "{}/today_data_race_id_list.txt".format( test_data_dir ), "r" )
    all_data = f.readlines()

    for str_data in all_data:
        test_race_id_list.append( str_data.replace( "\n", "" ) )

    return test_race_id_list
