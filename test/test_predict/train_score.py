from test_config.config import *

import sekitoba_data_manage as dm
from predict.train_score import TrainScore

def data_check( test_race_id, analyze_data ):
    print( "\ncheck train_score" )
    train_score = TrainScore( analyze_data )
    train_simu_data = dm.pickle_load( "train_simu_data.pickle" )
    t_data = {}

    for race_id in train_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in train_simu_data[race_id].keys():
                t_data[horce_id] = train_simu_data[race_id][horce_id]["data"]

    create_data = train_score.create()

    for horce_id in create_data.keys():
        for i in range( 0, len( train_score.score_key_list ) ):
            if not create_data[horce_id][i] == t_data[horce_id][i]:
                print( "train_score", horce_id, train_score.score_key_list[i], create_data[i], t_data[i] )

    return train_score.predict()
