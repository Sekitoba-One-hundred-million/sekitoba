import sys
import time
import datetime
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_logger import logger

dm.dl.prod_on()

import predict
import select_buy
from today_data_get import today_data_list_create
from data_manage import Storage
from data_manage import TodayData
from data_create import DataCreate
from data_collect import before_data_collect
from data_collect import just_before_data_collect

def race_wait( today_data ): # :TodayData
    dt_now = datetime.datetime.now()
    diff_timestamp = today_data.race_timestamp - dt_now.timestamp()
    wait_time = 600
    sleep_min = int( diff_timestamp - wait_time )
    
    if sleep_min > 0:
        #logger.info( "sleep:{}".format( sleep_min ) )
        time.sleep( sleep_min )
    elif sleep_min < -wait_time:
        return False
    
    return True

def bet_check( storage: Storage ):
    check_all_horce_num = storage.all_horce_num - len( storage.cansel_horce_id_list )
    
    if storage.all_horce_num > 10:
        return False

    skip_horce_len = len( storage.skip_horce_id_list )
    horce_len = len( storage.horce_id_list )

    if horce_len - skip_horce_len < 5:
        return False

    return True

def stock_data_create( today_data_list: list[TodayData] ):
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
        storage = Storage( today_data_list[i] )
        before_data_collect.main( storage ) # http通信のスクレイピングで入手するデータ
        stock_data[storage.today_data.race_id] = storage

    return stock_data

def main():
    today_data_list: list[TodayData] = today_data_list_create()
    stock_data = stock_data_create( today_data_list )

    for i in range( 0, len( today_data_list ) ):
        race_wait( today_data_list[i] )
        race_id = today_data_list[i].race_id
        just_before_data_collect.main( stock_data[race_id] )

        print( "\nstart predict {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        data_create = DataCreate( stock_data[race_id] )
        rank_score, recovery_score = predict.main( data_create )

        if rank_score == None or \
          recovery_score == None or \
          not bet_check( stock_data[race_id] ):
            print( "skip {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
            continue

        print( "bet {} {}R".format( today_data_list[i].place, today_data_list[i].race_num ) )
        select_buy.main( stock_data[race_id], rank_score, recovery_score )

if __name__ == "__main__":
    main()
