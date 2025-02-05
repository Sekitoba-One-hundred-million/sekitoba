import sys
import json
import requests

import SekitobaLibrary as lib
import SekitobaDataManage as dm

from config import pickle_name
from config import prod_dir

dm.dl.file_set( "pace_model.pickle" )
dm.dl.file_set( "race_pace_analyze_data.pickle" )

class RacePaceSimulation:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.modelList = dm.dl.data_get( "pace_model.pickle" )
        self.race_pace_analyze_data = dm.dl.data_get( "race_pace_analyze_data.pickle" )
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/race_pace_simulation_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

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
        horce_id = list( self.analyze_data.keys() )[-1]
        keyKind = str( int( self.analyze_data[horce_id]["kind"] ) )
        keyDist = str( int( self.analyze_data[horce_id]["dist"] ) )

        for key in self.modelList.keys():
            score = 0
            
            for model in self.modelList[key]:
                score += model.predict( [ learn_data ] )[0]

            result[key] = ( score / len( self.modelList[key] ) ) + self.race_pace_analyze_data[keyKind][keyDist][key]

        return result
