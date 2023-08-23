import os
import sys
import inspect
import datetime
from today_data_get import predict_race_id_get

from test_config.config import *

def predict_race_id_get_test():
    error_func = "{}:{}".format( test_today_data_get_error_message, \
                                          inspect.currentframe().f_code.co_name )

    test_day = datetime.datetime( 2023, 7, 9 )
    race_id_list = predict_race_id_get( test_day )

    if len( race_id_list ) == 0:
        show_erroe_message( error_func, "fail get race_id_list" )
        sys.exit( 1 )

    test_race_id_list = []
    race_id_list = sorted( race_id_list )

    f = open( "{}/race_id_list.txt".format( test_data_dir ), "r" )
    all_data = f.readlines()

    for str_data in all_data:
        test_race_id_list.append( str_data.replace( "\n", "" ) )

    test_race_id_list = sorted( test_race_id_list )

    if not len( race_id_list ) == len( test_race_id_list ):
        show_erroe_message( error_func, \
                           "not match length race_id_list\n{}\n{}".format( race_id_list, test_race_id_list ) )
        sys.exit( 1 )

    for i in range( 0, len( race_id_list ) ):
        if not race_id_list[i] == test_race_id_list[i]:
            show_erroe_message( error_func, \
                            "not match race_id\n{}\n{}".format( race_id_list, test_race_id_list ) )
            sys.exit( 1 )
