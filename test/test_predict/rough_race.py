from test_config.config import *

import sekitoba_data_manage as dm
from predict.rough_race import RoughRace

def data_check( race_id, analyze_data ):
    print( "\ncheck rough_race" )
    rough_race = RoughRace( analyze_data )
    rough_race_data = dm.pickle_load( "rough_race_learn_data.pickle" )
    t_data = []

    for i in range( 0, len( rough_race_data["teacher"] ) ):
        if race_id == rough_race_data["race_id"][i]:
            t_data = rough_race_data["teacher"][i]

    create_data = rough_race.create()

    for i in range( 0, len( rough_race.score_key_list ) ):
        if "predict" in rough_race.score_key_list[i]:# or \
          #"true_skill" in rough_race.score_key_list[i]:
            continue
        
        if not create_data[i] == t_data[i]:
            print( "rough_race: {}: create:{} teacher:{}".format( \
                    rough_race.score_key_list[i], create_data[i], t_data[i] ) )

    return rough_race.predict()
