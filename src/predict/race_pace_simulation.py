import sys

import SekitobaLibrary as lib
import SekitobaDataManage as dm

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
            self.score_key_list.append( lib.textReplace( str_data ) )

    def create( self ):
        learn_data = []

        if len( self.analyze_data ) == 0:
            return learn_data
        
        horce_id = list( self.analyze_data.keys() )[-1]
        not_found = False
        
        for score_key in self.score_key_list:
            if not score_key in self.analyze_data[horce_id]:
                print( "not found {}".format( score_key ) )
                not_found = True
                continue

            if self.analyze_data[horce_id][score_key] == None:
                print( "score None {}".format( score_key ) )
                sys.exit( 1 )

            if score_key in self.analyze_data:
                learn_data.append( self.analyze_data[score_key] )
            else:
                learn_data.append( self.analyze_data[horce_id][score_key] )

        if not_found:
            sys.exit( 1 )

        return learn_data

    def predict( self ):
        result = {}
        learn_data = self.create()

        for key in self.model.keys():
            score = 0
            for m in self.model[key]:
                score += m.predict( [ learn_data ] )[0]
                
            result[key] = score / len( self.model[key] )
            print( key, result[key] )

        return result
