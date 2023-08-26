import sys
import time
import datetime
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_logger import logger

dm.dl.prod_on()

from today_data_get import today_data_list_create
from data_manage import Storage
from data_manage import TodayData

#from config import data_name
#import today_data_get
import http_data_collect
import driver_data_collect
#import before_data_collect
#import data_analyze
#import predict_and_buy

def race_wait( today_data ): # :TodayData
    dt_now = datetime.datetime.now()
    diff_hour = today_data.hour - dt_now.hour
    diff_minute = today_data.minutue - dt_now.minute
    wait_time = 600
    sleep_min = diff_hour * 3600 + diff_minute * 60 - wait_time
    
    if sleep_min > 0:
        logger.info( "sleep:{}".format( sleep_min ) )
        time.sleep( int( sleep_min ) )
    elif sleep_min < -wait_time:
        return False
    
    return True

def stock_data_create( today_data_list: list[TodayData] ):
    #logger.info( "stock start" )

    #stock_data = dm.pickle_load( name.stock_name, prod = True )
    stock_data = dm.pickle_load( "stock_data.pickle", prod = True )

    if stock_data == None:
        stock_data: dict[Storage] = {}

    # 今回のレースで使用しないデータが入っている場合は削除
    use_key_list = []
    delete_key_list = list( stock_data.keys() )

    for i in range( 0, len( today_data_list ) ):
        use_key_list.append( today_data_list[i].race_id )

    for dk in delete_key_list:
        if not dk in use_key_list:
            stock_data.pop( dk, None )

    for i in range( 0, len( today_data_list ) ):
        print( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        #logger.info( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )

        #if not today_data_list[i].race_id in stock_data:
        storage = Storage( today_data_list[i] )
        http_data_collect.main( storage ) # http通信のスクレイピングで入手するデータ
        driver_data_collect.main( storage )
        #driver_data_collect.main( storage ) # driverの必要な情報を取得
        #stock_data[today_data_list[i].url] = storage
        #logger.info( "stockdata create {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )
        #dm.pickle_upload( "stock_data.pickle", stock_data, prod = True )
        #else:
        #    logger.info( "stockdata existing {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )

    #logger.info( "stock finish" )
    return stock_data

def main():
    today_data_list: list[TodayData] = today_data_list_create()
    stock_data_create( today_data_list )

if __name__ == "__main__":
    main()
