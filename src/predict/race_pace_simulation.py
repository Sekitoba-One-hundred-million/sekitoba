import sys

import sekitoba_library as lib
import sekitoba_data_manage as dm

from config import pickle_name
from config import prod_dir

dm.dl.file_set( pickle_name.pace_model )

class RacePaceSimulation:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.model = dm.dl.data_get( pickle_name.pace_model )
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/race_pace_simulation_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

    def create( self ):
        pace_key = "pace"
        learn_data = []

        if len( self.analyze_data ) == 0:
            return learn_data
        
        horce_id = list( self.analyze_data.keys() )[-1]
        
        for score_key in self.score_key_list:
            if not score_key in self.analyze_data[horce_id]:
                print( "not found {}".format( score_key ) )
                sys.exit( 1 )

            if self.analyze_data[horce_id][score_key] == None:
                print( "score None {}".format( score_key ) )
                sys.exit( 1 )

            if score_key in self.analyze_data[pace_key]:
                learn_data.append( self.analyze_data[pace_key][score_key] )
            else:
                learn_data.append( self.analyze_data[horce_id][score_key] )

        return learn_data

    def predict( self ):
        learn_data = self.create()
        return self.model.predict( [ learn_data ] )[0]
