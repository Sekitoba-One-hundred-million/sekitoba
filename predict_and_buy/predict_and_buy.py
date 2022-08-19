import time

import sekitoba_data_manage as dm
from sekitoba_logger import logger
from data_manage.storage import Storage
from data_analyze.users_data import UsersData

from slack_lib import slack
from predict_and_buy import score_func
from predict_and_buy import auto_buy

dm.dl.file_set( "users_score_rate.pickle" )
buy_kind_list = [ "one" ]
buy_score_check = { "one": 25 }

def main( storage: Storage, usres_score_data: UsersData ):
    buy_data = {}
    users_score_function = score_func.UsersScoreFunction()
    users_score_function.set_function()
    users_score_rate = dm.dl.data_get( "users_score_rate.pickle" )

    for buy_kind in buy_kind_list:
        buy_data[buy_kind] = []
        
        for horce_id in storage.horce_id_list:
            score = 0
            for data_name in users_score_function.function.keys():
                score_key = data_name.replace( "_minus", "" )

                try:
                    score += users_score_function.function[data_name]( usres_score_data.data[horce_id][score_key] ) * users_score_rate[buy_kind][data_name]
                except:
                    logger.error( "users_score_create not found data {}".format( score_key ) )
                    continue

            score = int( int( score / 5 ) * 5 )
            logger.info( "users_score race_id:{} horce_num:{} score:{}".format( storage.race_id, \
                                                                               storage.data[horce_id]["horce_num"], \
                                                                               score ) )
            
            if buy_score_check[buy_kind] <= score:
                buy_data[buy_kind].append( { "horce_num": storage.data[horce_id]["horce_num"], "money": 1 } )

        if len( buy_data[buy_kind] ) == 0:
            continue
        
        buy = False

        for t in range( 3 ):
            try:
                auto_buy.one_buy( buy_data[buy_kind], storage.today_data )
                buy = True
                break
            except:
                time.sleep( 3 )
                continue
        
        if buy:
            for bd in buy_data[buy_kind]:
                buy_str_data = "buyresult:{} race_id:{} horce_num:{} money:{}".format( buy_kind, \
                                                                                    storage.race_id, \
                                                                                    bd["horce_num"], \
                                                                                    bd["money"] * 100 )
                logger.info( buy_str_data )
                slack.send_message( buy_str_data )
