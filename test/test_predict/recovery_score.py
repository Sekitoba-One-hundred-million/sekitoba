from test_config.config import *
from test_predict.lib import skip_key

import SekitobaDataManage as dm
from predict.recovery_score import RecoveryScore

def data_check( test_race_id, analyze_data ):
    odds_index = 0
    recovery_score = RecoveryScore( analyze_data )
    recovery_simu_data = dm.pickle_load( "recovery_simu_data.pickle" )
    t_data = {}

    for race_id in recovery_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in recovery_simu_data[race_id].keys():
                t_data[horce_id] = recovery_simu_data[race_id][horce_id][odds_index]

            break

    create_data = recovery_score.create()

    for r, horce_id in enumerate( analyze_data.keys() ):
        for i in range( 0, len( recovery_score.score_key_list ) ):
            score_key = recovery_score.score_key_list[i]

            if skip_key( score_key ):
                continue

            #print( score_key )
            #print( create_data[score_key] )
            #print( t_data[horce_id] )
            if not round( create_data[score_key][r], 4 ) == round( t_data[horce_id]["data"][i], 4 ):
                print( "recovery_score", horce_id, score_key, create_data[score_key][r], t_data[horce_id]["data"][i] )

    return recovery_score.predict()
