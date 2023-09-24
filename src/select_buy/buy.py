import time
import math

import sekitoba_data_manage as dm
from sekitoba_logger import logger
from data_manage.storage import Storage

from select_buy.wide_buy import wide_buy
#from slack_lib import slack

def wide_bet_select( storage: Storage, rank_data: dict, recovery_data: dict ):
    score_list = []

    for horce_id in rank_data.keys():
        if horce_id in storage.skip_horce_id_list:
            continue
        
        score_list.append( { "horce_id": horce_id, \
                            "rank_score": rank_data[horce_id], \
                            "recovery_score": recovery_data[horce_id] } )

    select_list = []
    check_formation_count = [ 3, 2 ]
    rank_sort_list = sorted( score_list, key = lambda x:x["rank_score"], reverse = True )
    recovery_sort_list = sorted( score_list, key = lambda x:x["recovery_score"], reverse = True )
    rank_horce_num = [ storage.current_horce_data[rank_sort_list[0]["horce_id"]].horce_num, \
                      storage.current_horce_data[rank_sort_list[1]["horce_id"]].horce_num ]

    for i in range( 0, len( check_formation_count ) ):
        horce_id_1 = rank_sort_list[i]["horce_id"]
        horce_num_1 = int( storage.current_horce_data[horce_id_1].horce_num )
        formation_count = 0

        for r in range( 0, len( recovery_sort_list ) ):
            if formation_count == check_formation_count[i]:
                break

            horce_id_2 = rank_sort_list[r]["horce_id"]
            horce_num_2 = int( storage.current_horce_data[horce_id_2].horce_num )

            if horce_num_2 in rank_horce_num:
                continue

            select_list.append( { "horce_num_1": min( horce_num_1, horce_num_2 ), \
                                 "horce_num_2": max( horce_num_1, horce_num_2 ) } )
            formation_count += 1

    return select_list
    
def main( storage: Storage, rank_data, recovery_data ):
    wide_select_list = wide_bet_select( storage, rank_data, recovery_data )

    bet_money = 5
    check_horce_num = int( storage.all_horce_num - len( storage.cansel_horce_id_list ) )

    if check_horce_num < 9:
        bet_money *= 2

    bet_money = int( bet_money )
