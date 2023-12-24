from test_config.config import *

import sekitoba_data_manage as dm
from predict.up3 import Up3

def data_check( test_race_id, analyze_data ):
    print( "\ncheck up3" )
    up3 = Up3( analyze_data )
    up3_simu_data = dm.pickle_load( "up3_simu_data.pickle" )
    t_data = {}

    for race_id in up3_simu_data.keys():
        if race_id == test_race_id:
            for horce_id in up3_simu_data[race_id].keys():
                t_data[horce_id] = up3_simu_data[race_id][horce_id]["data"]

    create_data = up3.create()

    for horce_id in create_data.keys():
        for i in range( 0, len( up3.score_key_list ) ):

            if "predict" in up3.score_key_list[i]:
              #or "true_skill" in up3.score_key_list[i] \
              #or "judgment" in up3.score_key_list[i]:
                continue

            if not create_data[horce_id][i] == t_data[horce_id][i]:
                print( "up3", horce_id, up3.score_key_list[i], create_data[horce_id][i], t_data[horce_id][i] )
                pass

    return up3.predict()
