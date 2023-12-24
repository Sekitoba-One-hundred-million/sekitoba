from test_config.config import *

import sekitoba_data_manage as dm
from predict.first_passing_rank import FirstPassingRank

def data_check( test_race_id, analyze_data ):
    print( "\ncheck first_passing_rank" )
    first_passing_rank = FirstPassingRank( analyze_data )
    first_passing_rank_simu_data = dm.pickle_load( "first_passing_rank_simu_data.pickle" )
    t_data = {}

    for race_id in first_passing_rank_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in first_passing_rank_simu_data[race_id].keys():
                t_data[horce_id] = first_passing_rank_simu_data[race_id][horce_id]["data"]

    create_data = first_passing_rank.create()
    #or "true_skill" in first_passing_rank.score_key_list[i] \
    for horce_id in create_data.keys():
        for i in range( 0, len( first_passing_rank.score_key_list ) ):
            if "predict" in first_passing_rank.score_key_list[i]:# \
              #or "judgment" in first_passing_rank.score_key_list[i]:
                continue
            
            if not create_data[horce_id][i] == t_data[horce_id][i]:
                print( "first_passing_rank", horce_id, first_passing_rank.score_key_list[i], create_data[horce_id][i], t_data[horce_id][i] )
                pass

    return first_passing_rank.predict()
