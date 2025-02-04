import os
import sys
import inspect
import datetime
from data_manage import TodayData
from today_data_get.data_get import predict_race_id_get

from test_config.config import *

def predict_race_id_get_test():
    error_func = "{}:{}".format( test_today_data_get_error_message, \
                                          inspect.currentframe().f_code.co_name )

    test_day = datetime.datetime( 2023, 7, 9 )
    race_id_list = predict_race_id_get( test_day )

    if len( race_id_list ) == 0:
        show_erroe_message( error_func, "fail get race_id_list" )
        sys.exit( 1 )

    race_id_list = sorted( race_id_list )

    if not len( race_id_list ) == len( test_race_id_list ):
        show_erroe_message( error_func, \
                           "not match length race_id_list\n{}\n{}".format( race_id_list, test_race_id_list ) )
        sys.exit( 1 )

    for i in range( 0, len( race_id_list ) ):
        if not race_id_list[i] == test_race_id_list[i]:
            show_erroe_message( error_func, \
                            "not match race_id\n{}\n{}".format( race_id_list, test_race_id_list ) )
            sys.exit( 1 )

def today_data_test():
    error_func = "{}:{}".format( test_today_data_get_error_message, \
                                          inspect.currentframe().f_code.co_name )
    test_day = datetime.datetime( 2023, 7, 9 )
    race_id_list, race_day = predict_race_id_get( test_day )

    today_data_list = []
    #test_race_id_list = load_test_race_id_list()
    
    for race_id in race_id_list:
        today_data = TodayData( race_id, race_day )
    
        for i in range( 0, 5 ):
            today_data.race_time_get()

            if today_data.race_timestamp == -1:
                continue

            if today_data.bet_race:
                today_data_list.append( today_data )
                
            break

    today_data_list = sorted( today_data_list, key = lambda x: x.race_timestamp )

    if not len( today_data_list ) == len( test_today_data_race_id_list ):
        show_erroe_message( error_func, \
                           "not match length today_race_id_list\n{}\n{}".format( len( today_data_list ), len( test_today_data_race_id_list ) ) )
        sys.exit( 1 )

    for i in range( 0, len( today_data_list ) ):
        if not today_data_list[i].race_id == test_today_data_race_id_list[i]:
            show_erroe_message( error_func, \
                            "not match today_race_id\n{}\n{}".format( today_data_list[i].race_id, test_today_data_race_id_list[i] ) )
            sys.exit( 1 )
