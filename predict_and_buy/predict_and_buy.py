import time

import sekitoba_data_manage as dm
from sekitoba_logger import logger
from data_manage.storage import Storage
from data_analyze.users_data import UsersData

from slack_lib import slack
from predict_and_buy import score_func
from predict_and_buy import auto_buy

buy_score_check = { "one": 55 }

users_score_function = score_func.UsersScoreFunction()
users_score_function.set_function()

def score_list_create( buy_kind: str, horce_id_list: list, usres_score_data: UsersData ):
    score_list = []

    for horce_id in horce_id_list:
        score = 0
        for data_name in users_score_function.function.keys():
            score_key = data_name.replace( "_minus", "" )

            try:
                score += users_score_function.function[data_name]( usres_score_data.data[horce_id][score_key] )
            except:
                logger.error( "{} users_score_create not found data {}".format( buy_kind, score_key ) )
                continue

        score = int( int( score / 5 ) * 5 )
        score_list.append( { "score": score, "horce_id": horce_id } )

    return score_list

def one_buy( storage: Storage, usres_score_data: UsersData ):
    buy_kind = "one"
    buy_data = []
    score_list = score_list_create( buy_kind, storage.horce_id_list, usres_score_data )

    for score_data in score_list:
        horce_id = score_data["horce_id"]
        horce_num = storage.data[horce_id]["horce_num"]
        score = score_data["score"]
        logger.info( "users_score kind:{} race_id:{} horce_num:{} score:{}".format( buy_kind, \
                                                                                   storage.race_id, \
                                                                                   horce_num, \
                                                                                   score ) )
        
        if buy_score_check[buy_kind] <= score:
            buy_data.append( { "horce_num": horce_num, "money": 2 } )

    if len( buy_data ) == 0:
        return

    buy = False
    for t in range( 3 ):
        try:
            auto_buy.one_buy( buy_data, storage.today_data )
            buy = True
            break
        except Exception as err:
            print( err )
            time.sleep( 3 )
            continue
        
    if buy:
        for bd in buy_data:
            buy_str_data = "buyresult:{} race_id:{} horce_num:{} money:{}".format( buy_kind, \
                                                                                  storage.race_id, \
                                                                                  bd["horce_num"], \
                                                                                  bd["money"] * 100 )
            logger.info( buy_str_data )
            slack.send_message( buy_str_data )

def quinella_buy( storage: Storage, usres_score_data: UsersData ):
    buy_kind = "quinella"
    buy_data = []
    score_list = score_list_create( buy_kind, storage.horce_id_list, usres_score_data )

    for i in range( 0, len( score_list ) ):
        for r in range( i + 1, len( score_list ) ):
            horce_id_1 = score_list[i]["horce_id"]
            horce_id_2 = score_list[r]["horce_id"]
            horce_num_1 = storage.data[horce_id_1]["horce_num"]
            horce_num_2 = storage.data[horce_id_2]["horce_num"]
            score = score_list[i]["score"] + score_list[r]["score"]
            logger.info( "users_score kind:{} race_id:{} horce_num:{}-{} score:{}".format( buy_kind, \
                                                                                          storage.race_id, \
                                                                                          horce_num_1, \
                                                                                          horce_num_2, \
                                                                                          score ) )
        
        if buy_score_check[buy_kind] <= score:
            buy_data.append( { "horce_num_1": horce_num_1, "horce_num_2": horce_num_2, "money": 1 } )
            
        if len( buy_data ) == 3:
            break

    if len( buy_data ) == 0:
        return

    buy = False
    for t in range( 3 ):
        try:
            auto_buy.quinella_buy( buy_data, storage.today_data )
            buy = True
            break
        except Exception as err:
            print( err )
            time.sleep( 3 )
            continue
        
    if buy:
        for bd in buy_data:
            buy_str_data = "buyresult:{} race_id:{} horce_num:{}-{} money:{}".format( buy_kind, \
                                                                                     storage.race_id, \
                                                                                     bd["horce_num_1"], \
                                                                                     bd["horce_num_2"], \
                                                                                     bd["money"] * 100 )
            logger.info( buy_str_data )
            slack.send_message( buy_str_data )

def main( storage: Storage, usres_score_data: UsersData ):
    try:
        one_buy( storage, usres_score_data )
    except Exception as err:
        print( err )

    #try:
    #    quinella_buy( storage, usres_score_data )
    #except Exception as err:
    #    print( err )
