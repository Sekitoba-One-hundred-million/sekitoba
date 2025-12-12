from test_config.config import *
from test_predict.lib import skip_key

import SekitobaDataManage as dm
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
        if skip_key( race_pace_simulation.score_key_list[i]):
                continue

        if not round( create_data[i], 2 ) == round( t_data[i], 2 ):
            print( "race_pace: {}: create:{} teacher:{}".format( \
                    race_pace_simulation.score_key_list[i], round( create_data[i], 4 ), round( t_data[i], 4 ) ) )

    return race_pace_simulation.predict()
