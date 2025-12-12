from test_config.config import *
from test_predict.lib import skip_key

import SekitobaDataManage as dm
from predict.first_passing_rank import FirstPassingRank

def data_check( test_race_id, analyze_data ):
    print( "\ncheck first_passing_rank" )
    odds_index = 0
    first_passing_rank = FirstPassingRank( analyze_data )
    first_passing_rank_simu_data = dm.pickle_load( "first_passing_rank_simu_data.pickle" )
    t_data = {}

    for race_id in first_passing_rank_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in first_passing_rank_simu_data[race_id].keys():
                t_data[horce_id] = first_passing_rank_simu_data[race_id][horce_id][odds_index]["data"]

    create_data = first_passing_rank.create()
    #or "true_skill" in first_passing_rank.score_key_list[i] \
    for horce_id in create_data.keys():
        for i in range( 0, len( first_passing_rank.score_key_list ) ):
            if skip_key( first_passing_rank.score_key_list[i]):
                continue

            if not round( create_data[horce_id][i], 4 ) == round( t_data[horce_id][i], 4 ):
                print( "first_passing_rank", horce_id, first_passing_rank.score_key_list[i], create_data[horce_id][i], t_data[horce_id][i] )

    return first_passing_rank.predict()
