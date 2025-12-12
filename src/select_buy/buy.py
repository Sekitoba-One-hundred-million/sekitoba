import time
import math

import SekitobaDataManage as dm
from SekitobaLogger import logger
from data_manage.storage import Storage

from select_buy.auto_buy import autoBuy

def create_rate_score( rank_score_data: dict ):
    result = {}
    min_score = min( list( rank_score_data.values() ) )
    
    for horce_id in rank_score_data.keys():
        result[horce_id] = max( rank_score_data[horce_id] - min_score * 1.1, 0 )
        result[horce_id] *= ( 2 - ( i / 10 ) )
        result[horce_id] = math.pow( result[horce_id], 2 )
        all_score += result[horce_id]

    for horce_id in rank_score_data.keys():
        result[horce_id] /= all_score

    return result

def bet_select( storage: Storage, rank_score_data: dict, recovery_score: dict ):
    score_list = []
    #rate_score = create_rate_score( rank_score_data )

    for horce_id in rank_score_data.keys():
        score_list.append( { "horce_id": horce_id, \
                             "rank_score": rank_score_data[horce_id],
                             #"rate_score": rate_score[horce_id],
                             "recovery_score": recovery_score[horce_id] } )
        logger.info( "predict_horce race_id:{} horce_num:{} rank_score:{} recovery_score:{}".format(
            storage.today_data.race_id, \
            storage.current_horce_data[horce_id].horce_num, \
            rank_score_data[horce_id],
            #rate_score[horce_id],
            recovery_score[horce_id] ) )

    betData = []
    t = 1
    score_list = sorted( score_list, key = lambda x:x["recovery_score"], reverse = True )

    for i in range( 0, len( score_list ) ):
        score_list[i]["recovery_score"] = int( i + 1 )
    
    rank_sort_list = sorted( score_list, key = lambda x:x["rank_score"], reverse = True )

    for i in range( 0, min( len( score_list ), t ) ):
        horce_id = rank_sort_list[i]["horce_id"]
        odds = storage.current_horce_data[horce_id].odds
        #ex_value = odds * rank_sort_list[i]["rate_score"]
        recovery_score = rank_sort_list[i]["recovery_score"]

        #if ex_value < 1:
        #    continue

        if 5 < recovery_score:
            continue

        horce_num = int( storage.current_horce_data[horce_id].horce_num )

        for r in range( 1, len( rank_sort_list ) ):
            if rank_sort_list[r]["recovery_score"] < 5:
                horce_id_2 = rank_sort_list[r]["horce_id"]
                horce_num_2 = int( storage.current_horce_data[horce_id_2].horce_num )
                betData.append( { "horce_num_1": horce_num, "horce_num_2": horce_num_2 } )
                logger.info( "bet quinella race_id:{} horce_num_1:{} horce_num_2:{}".format(
                    storage.today_data.race_id, horce_num, horce_num_2 ) )

    return betData
    
def main( storage: Storage, rank_score_data, recovery_score ):
    betData = bet_select( storage, rank_score_data, recovery_score )

    if len( betData ) == 0:
        return False

    #autoBuy( storage, betData )

    return True
