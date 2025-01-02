import time
import math

import SekitobaDataManage as dm
from SekitobaLogger import logger
from data_manage.storage import Storage

from select_buy.auto_buy import one_buy
#from slack_lib import slack

LINE_EX_VALUE = 1.1

def softmax( data ):
    result = []
    sum_data = 0

    for i in range( 0, len( data ) ):
        sum_data += math.exp( data[i] )

    for i in range( 0, len( data ) ):
        result.append( math.exp( data[i] ) / sum_data )

    return result

def bet_select( storage: Storage, rank_score_data: dict ):
    score_list = []

    for horce_id in rank_score_data.keys():
        score_list.append( { "horce_id": horce_id, \
                            "rank_score_rate": rank_score_data[horce_id] } )

    select_horce_id = None
    rank_sort_list = sorted( score_list, key = lambda x:x["rank_score_rate"], reverse = True )

    for i in range( 0, len( rank_sort_list ) ):
        horce_id = rank_sort_list[i]["horce_id"]
        odds = storage.current_horce_data[horce_id].odds
        ex_value = odds * rank_sort_list[i]["rank_score_rate"]
        bet_count = int( 1 + max( min( ( ex_value - LINE_EX_VALUE ) * 10, 9 ), 0 ) )
        logger.info( "predict_horce race_id:{} index:{} horce_num:{} horce_id:{} odds:{}".format(
            storage.today_data.race_id, \
            i, \
            storage.current_horce_data[horce_id].horce_num,\
            horce_id,\
            odds ) )
    
    return select_horce_id, bet_count
    
def main( storage: Storage, rank_score_data ):
    bet_horce_id, bet_count = bet_select( storage, rank_score_data )

    if bet_horce_id == None:
        return False

    if not bet_horce_id in storage.current_horce_data:
        return False

    bet_horce_num = storage.current_horce_data[bet_horce_id].horce_num
    #print( "bet_count:{} horce_num:{}".format( bet_count, bet_horce_num ) )
    #logger.info( "bet_horce race_id:{} bet_count:{} horce_num:{}".format( storage.today_data.race_id, bet_count, bet_horce_num ) )
    #one_buy( storage, { "bet_count": bet_count, "horce_num": bet_horce_num } )

    return True
