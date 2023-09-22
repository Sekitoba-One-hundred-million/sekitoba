from test_config.config import *

import sekitoba_data_manage as dm
from predict.recovery_score import RecoveryScore

def data_check( test_race_id, analyze_data ):
    recovery_score = RecoveryScore( analyze_data )
    users_data = dm.pickle_load( "users_data.pickle" )
    t_data = {}

    for race_id in users_data.keys():
        if race_id == test_race_id:
            for horce_id in users_data[race_id].keys():
                t_data[horce_id] = users_data[race_id][horce_id]

            break

    create_data = recovery_score.create()
    
    for horce_id in create_data.keys():
        if not horce_id in t_data:
            continue

        for score_key in create_data[horce_id].keys():
            if "true_skill" in score_key:
                continue

            if not create_data[horce_id][score_key] == int( t_data[horce_id][score_key] ):
                print( "recovery_score", horce_id, score_key, create_data[horce_id][score_key], t_data[horce_id][score_key] )

    return recovery_score.predict()
