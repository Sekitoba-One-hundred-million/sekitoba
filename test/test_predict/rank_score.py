from test_config.config import *

import sekitoba_data_manage as dm
from predict.rank_score import RankScore

def data_check( test_race_id, analyze_data ):
    print( "\nrank_score check" )
    rank_score = RankScore( analyze_data )
    rank_simu_data = dm.pickle_load( "rank_simu_data.pickle" )
    t_data = {}

    for race_id in rank_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in rank_simu_data[race_id].keys():
                t_data[horce_id] = rank_simu_data[race_id][horce_id]["data"]

            break

    create_data = rank_score.create()

    for horce_id in create_data.keys():
        for i in range( 0, len( rank_score.score_key_list ) ):
            if "predict" in rank_score.score_key_list[i]:# \
              #or "predict" in rank_score.score_key_list[i] \
              #or "judgment" in rank_score.score_key_list[i]:
                continue

            if not create_data[horce_id][i] == t_data[horce_id][i]:
                print( "rank_score", horce_id, rank_score.score_key_list[i], create_data[horce_id][i], t_data[horce_id][i] )

    return rank_score.predict()
