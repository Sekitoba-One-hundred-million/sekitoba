import time
import math

import SekitobaDataManage as dm
from SekitobaLogger import logger
from data_manage.storage import Storage

from select_buy.auto_buy import autoBuy

def bet_select( storage: Storage, rank_score_data: dict ):
    score_list = []

    for horce_id in rank_score_data.keys():
        score_list.append( { "horce_id": horce_id, \
                            "rank_score_rate": rank_score_data[horce_id] } )
        logger.info( "predict_horce race_id:{} horce_num:{} score:{}".format(
            storage.today_data.race_id, \
            storage.current_horce_data[horce_id].horce_num, \
            rank_score_data[horce_id] ) )

    betData = []
    index_data = [ [ 3, 5 ], [ 6, 7, 8 ] ]
    rank_sort_list = sorted( score_list, key = lambda x:x["rank_score_rate"], reverse = True )

    for i in range( 0, len( index_data ) ):
        horce_id = rank_sort_list[i]["horce_id"]
        popular = storage.current_horce_data[horce_id].popular

        #if not popular in index_data[i]:
        #    continue

        horce_num = int( storage.current_horce_data[horce_id].horce_num )
        betData.append( { "kind": "one", "horce_num": horce_num, "count": 1 } )
        logger.info( "bet_horce race_id:{} horce_num:{} kind:{}".format(
            storage.today_data.race_id, \
            storage.current_horce_data[horce_id].horce_num,\
            "one" ) )

        for r in range( 0, min( len( rank_sort_list ), 4 ) ):
            horce_id2 = rank_sort_list[r]["horce_id"]
            horce_num2 = int( storage.current_horce_data[horce_id2].horce_num )

            if horce_num == horce_num2:
                continue

            betData.append( { "kind": "wide", "horce_num": [ horce_num, horce_num2 ], "count": 1 } )
            logger.info( "bet_horce race_id:{} horce_num:{},{} kind:{}".format(
                storage.today_data.race_id, \
                storage.current_horce_data[horce_id].horce_num,\
                storage.current_horce_data[horce_id2].horce_num, \
                "wide" ) )

    return betData
    
def main( storage: Storage, rank_score_data ):
    betData = bet_select( storage, rank_score_data )

    if len( betData ) == 0:
        return False

    autoBuy( storage, betData )

    return True
