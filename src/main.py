import sys
import time
import datetime
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm
from SekitobaLogger import logger

dm.dl.prod_on()

import predict
import select_buy
from today_data_get import today_data_list_create
from data_manage import Storage
from data_manage import TodayData
from data_create import DataCreate
from data_collect import before_data_collect
from data_collect import just_before_data_collect

STOCK_DATA = "stock_data.pickle"

def race_wait( today_data ): # :TodayData
    dt_now = datetime.datetime.now()
    diff_timestamp = today_data.race_timestamp - dt_now.timestamp()
    wait_time = 120
    sleep_min = int( diff_timestamp - wait_time )
    
    if sleep_min > 0:
        #logger.info( "sleep:{}".format( sleep_min ) )
        time.sleep( sleep_min )
    elif sleep_min < -wait_time:
        return False
    
    return True

def stock_data_create( today_data_list: list[TodayData] ):
    stock_data: dict[Storage] = dm.pickle_load( STOCK_DATA )

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
        if today_data_list[i].race_id in stock_data:
            continue
        
        print( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        #logger.info( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        storage = Storage( today_data_list[i] )
        before_data_collect.main( storage ) # http通信のスクレイピングで入手するデータ
        stock_data[storage.today_data.race_id] = storage
        dm.pickle_upload( STOCK_DATA, stock_data )

    return stock_data

def main():
    today_data_list: list[TodayData] = today_data_list_create()
    stock_data = stock_data_create( today_data_list )

    for i in range( 0, len( today_data_list ) ):
        if not race_wait( today_data_list[i] ):
            continue

        print( "\nstart predict {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        logger.info( "start predict {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        race_id = today_data_list[i].race_id
        just_before_data_collect.main( stock_data[race_id] )
        data_create = DataCreate( stock_data[race_id] )
        rank_score = predict.main( data_create )

        if rank_score == None:
            print( "skip {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
            logger.info( "skip {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
            continue

        print( "bet {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        logger.info( "bet {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        select_buy.main( stock_data[race_id], rank_score )

if __name__ == "__main__":
    main()
