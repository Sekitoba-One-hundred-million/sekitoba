from test_config.config import *

import sekitoba_data_manage as dm
from predict.race_pace_simulation import RacePaceSimulation

def data_check( race_id, analyze_data ):
    print( "\ncheck race_pace_simulation" )
    race_pace_simulation = RacePaceSimulation( analyze_data )
    race_pace_data = dm.pickle_load( "pace_learn_data.pickle" )
    t_data = []

    for i in range( 0, len( race_pace_data["teacher"] ) ):
        if race_id == race_pace_data["race_id"][i]:
            t_data = race_pace_data["teacher"][i]

    create_data = race_pace_simulation.create()

    for i in range( 0, len( race_pace_simulation.score_key_list ) ):
        if "true_skill" in race_pace_simulation.score_key_list[i]:
            continue
        
        if not create_data[i] == t_data[i]:
            print( "race_pace: {}: create:{} teacher:{}".format( \
                    race_pace_simulation.score_key_list[i], create_data[i], t_data[i] ) )

    return race_pace_simulation.predict()
