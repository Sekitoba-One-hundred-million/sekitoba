from test_config.config import *

import sekitoba_data_manage as dm
from predict.last_passing_rank import LastPassingRank

def data_check( test_race_id, analyze_data ):
    last_passing_rank = LastPassingRank( analyze_data )
    last_passing_rank_simu_data = dm.pickle_load( "last_passing_rank_simu_data.pickle" )
    t_data = {}

    for race_id in last_passing_rank_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in last_passing_rank_simu_data[race_id].keys():
                t_data[horce_id] = last_passing_rank_simu_data[race_id][horce_id]["data"]

    create_data = last_passing_rank.create()

    for horce_id in create_data.keys():
        for i in range( 0, len( last_passing_rank.score_key_list ) ):

            if "true_skill" in last_passing_rank.score_key_list[i] \
              or "predict" in last_passing_rank.score_key_list[i] \
              or "judgment" in last_passing_rank.score_key_list[i]:
                continue

            if not create_data[horce_id][i] == t_data[horce_id][i]:
                print( "last_passing", horce_id, last_passing_rank.score_key_list[i], create_data[horce_id][i], t_data[horce_id][i] )
                pass

    return last_passing_rank.predict()
