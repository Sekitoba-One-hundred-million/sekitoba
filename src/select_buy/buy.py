import time
import math

import sekitoba_data_manage as dm
from sekitoba_logger import logger
from data_manage.storage import Storage

from select_buy.wide_buy import wide_buy
#from slack_lib import slack

def softmax( data ):
    result = []
    sum_data = 0

    for i in range( 0, len( data ) ):
        sum_data += math.exp( data[i] )

    for i in range( 0, len( data ) ):
        result.append( math.exp( data[i] ) / sum_data )

    return result

def bet_select( storage: Storage, rank_score_data: dict ):
    all_score = 0
    min_score = 1000000
    softmax_score_list = softmax( list( rank_score_data.values() ) )

    for score in softmax_score_list:
        min_score = min( min_score, score )
        all_score += score

    all_score += min_score * len( softmax_score_list )
    score_list = []
    for i, horce_id in enumerate( rank_score_data.keys() ):
        score_list.append( { "horce_id": horce_id, \
                            "rank_score_rate": ( softmax_score_list[i] + min_score ) / all_score } )

    select_horce_id = None
    rank_sort_list = sorted( score_list, key = lambda x:x["rank_score_rate"], reverse = True )
    first_horce_id = rank_sort_list[0]["horce_id"]
    odds = storage.current_horce_data[first_horce_id].odds
    ex_value = odds * rank_sort_list[0]["rank_score_rate"]

    if 5 < odds or 1.1 < ex_value:
        select_horce_id = first_horce_id

    print( storage.current_horce_data[first_horce_id].horce_num, odds, rank_sort_list[0]["rank_score_rate"], ex_value )
    return select_horce_id, ex_value
    
def main( storage: Storage, rank_score_data ):
    bet_horce_id, ex_value = bet_select( storage, rank_score_data )

    if bet_horce_id == None:
        return False

    bet_count = int( 1 + max( min( ( ex_value - 1 ) * 10, 4 ), 0 ) )

    return True
