import datetime
import time
import sys
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_logger import logger

dm.dl.prod_on()

from today_data_get import TodayData
from data_manage.storage import Storage

from config import name
import today_data_get
import http_data_collect
import driver_data_collect
import before_data_collect
import data_analyze
import predict_and_buy

comm = MPI.COMM_WORLD   #COMM_WORLDは全体
size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

def race_wait( today_data: TodayData ):
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

def day_search( test = False ):
    result = []

    if test:
        result.append( datetime.datetime( 2022, 5, 28 ) )
        return result
    
    now_time = datetime.datetime.now()
    #now_time = datetime.datetime( int( now_time.year ), int( now_time.month ), int( now_time.day ) + 1 )
    
    if now_time.isoweekday() == 7:
        result.append( now_time )
    elif now_time.isoweekday() == 6:
        result.append( now_time )
        
        try:
            result.append( datetime.datetime( int( now_time.year ), int( now_time.month ), \
                                              int( now_time.day ) + 1 ) )
        except:
            try:
                result.append( datetime.datetime( int( now_time.year ), int( now_time.month ) + 1, 1 ) )
            except:
                result.append( datetime.datetime( int( now_time.year ) + 1, 1, 1 ) )
    else:
        count = 0
        add_day = 6 - now_time.isoweekday()
        
        for r in range( 1, add_day + 1 ):
            try:
                check = datetime.datetime( int( now_time.year ), int( now_time.month ), \
                                           int( now_time.day ) + r )
            except:
                count = r - 1
                break
            
        for i in range( 0, 2 ):                            
            try:
                result.append( datetime.datetime( int( now_time.year ), int( now_time.month ), \
                                                  int( now_time.day ) + add_day + i - count ) )
            except:
                try:
                    result.append( datetime.datetime( int( now_time.year ), \
                                                      int( now_time.month ) + 1, add_day + i - count ) )
                except:
                    result.append( datetime.datetime( int( now_time.year ) + 1, 1, add_day + i - count ) )
        
    return result

def stock_data_create( today_data_list ) -> dict[Storage]:
    logger.info( "stock start" )
    
    #stock_data = dm.pickle_load( name.stock_name, prod = True )
    stock_data = dm.pickle_load( "stock_data.pickle", prod = True )

    if stock_data == None:
        stock_data: dict[Storage] = {}
        
    # 今回のレースで使用しないデータが入っている場合は削除
    use_key_list = []
    delete_key_list = list( stock_data.keys() )
    
    for i in range( 0, len( today_data_list ) ):
        use_key_list.append( today_data_list[i].url )

    for dk in delete_key_list:
        if not dk in use_key_list:
            stock_data.pop( dk, None )

    for i in range( 0, len( today_data_list ) ):
        print( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )
        logger.info( "stock {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )
        
        if not today_data_list[i].url in stock_data.keys():
            storage = Storage()
            storage.race_id = today_data_list[i].race_id
            storage.today_data = today_data_list[i]
            storage.place_num = lib.place_num( today_data_list[i].place )
            http_data_collect.main( storage )#http通信のスクレイピングで入手するデータ
            driver_data_collect.main( storage )#driverの必要な情報を取得
            stock_data[today_data_list[i].url] = storage
            logger.info( "stockdata create {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )
            dm.pickle_upload( "stock_data.pickle", stock_data, prod = True )
        else:
            logger.info( "stockdata existing {} {}R".format( today_data_list[i].place, today_data_list[i].num ) )


    logger.info( "stock finish" )
    return stock_data

def test_check():
    result = None

    while 1:
        test = input( "test start (y/n): " )

        if test == "y":
            result = True
            break
        elif test == "n":
            result = False
            break
        else:
            print( "Your enter is {}".format( test ) )
            print( "Please enter y or n" )

    return result

def http_data_check( stock_data: dict[ str, Storage ] ):
    count = 0
    
    while 1:
        finish = True
        
        for k in stock_data.keys():
            if stock_data[k].dist == None: # distは必ず取れるので取れていないとおかしい
                print( "not get data {} {}R".format( stock_data[k].today_data.place, stock_data[k].today_data.num ) )
                http_data_collect.main( stock_data[k] )
                finish = False
                dm.pickle_upload( "stock_data.pickle", stock_data, prod = True )

        if finish:
            break

def main():
    test = False#test_check()

    if rank == 0:
        today_data_list = today_data_get.main( test = test )
        stock_data: dict[ str, Storage ] = stock_data_create( today_data_list )
        http_data_check( stock_data )

        for i in range( 1, size ):
            comm.send( True, dest = i, tag = 0 )
    else:
        check = comm.recv( source = 0, tag = 0 )

        if check:
            stock_data = dm.pickle_load( "stock_data.pickle", prod = True )
        else:
            sys.exit( 1 )
        
    users_score_data = data_analyze.main( stock_data )

    if not rank == 0:
        print( "finish rank:{}".format( rank ) )
        sys.exit( 0 )

    print( "race start!" )
    
    for today_data in today_data_list:
        url = today_data.url
        race_id = lib.id_get( url )
        stock_data[url].today_data = today_data
            
        if race_wait( today_data ):
            logger.info( "{} {}R users score create start".format( today_data.place, today_data.num ) )
            print( "{} {}R users score create start".format( today_data.place, today_data.num ) )
            before_data_collect.main( stock_data[url] )
            users_score_data[race_id].after_users_data_analyze( stock_data[url] )
            predict_and_buy.main( stock_data[url], users_score_data[race_id] )
        
if __name__ == "__main__":
    main()
