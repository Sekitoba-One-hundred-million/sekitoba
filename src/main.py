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
from today_data_get import today_data_listCreate
from data_manage import Storage
from data_manage import TodayData
from data_create import DataCreate
from data_collect import before_data_collect
from data_collect import just_before_data_collect

STOCK_DATA = "stock_data.pickle"

def race_wait( todayData: TodayData ):
    WAIT_SECONDS = 120
    dtNow = datetime.datetime.now()
    diff_timestamp = todayData.race_timestamp - dtNow.timestamp()
    sleep_seconds = int( diff_timestamp - WAIT_SECONDS )
    
    if sleep_seconds > 0:
        time.sleep( sleep_seconds )
    elif sleep_seconds < -WAIT_SECONDS:
        return False

    return True

def stock_dataCreate( today_data_list: list[TodayData], driver ):
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
        #if today_data_list[i].race_id in stock_data:
        #    continue
        
        print( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        storage = Storage( today_data_list[i] )
        before_data_collect.main( storage, driver ) # http通信のスクレイピングで入手するデータ
        stock_data[storage.today_data.race_id] = storage
        dm.pickle_upload( STOCK_DATA, stock_data )

    return stock_data

def main():
    driver = lib.driver_start()
    driver = lib.login( driver )
    today_data_list: list[TodayData] = today_data_listCreate( driver )
    stock_data = stock_dataCreate( today_data_list, driver )

    for i in range( 0, len( today_data_list ) ):
        if not race_wait( today_data_list[i] ):
            continue

        print( "\nstart predict {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        logger.info( "start predict {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        race_id = today_data_list[i].race_id
        just_before_data_collect.main( stock_data[race_id], driver )
        data_create = DataCreate( stock_data[race_id] )
        rank_score, recovery_score = predict.main( data_create )
        
        if rank_score == None:
            print( "skip {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
            logger.info( "skip {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
            continue

        #print( "bet {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        #logger.info( "bet {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        select_buy.main( stock_data[race_id], rank_score, recovery_score )
        #return

    driver.quit()

if __name__ == "__main__":
    main()
