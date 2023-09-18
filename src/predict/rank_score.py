import sys
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from config import pickle_name
from config import prod_dir

dm.dl.file_set( pickle_name.rank_model )

class RankScore:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.model = dm.dl.data_get( pickle_name.rank_model )

        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/rank_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

    def create( self ):
        learn_data = {}
        
        for horce_id in self.analyze_data.keys():
            instance_data = []
            
            if horce_id == "pace":
                continue

            for score_key in self.score_key_list:
                if not score_key in self.analyze_data[horce_id]:
                    print( "not found {}".format( score_key ) )
                    sys.exit( 1 )

                if self.analyze_data[horce_id][score_key] == None:
                    print( "score None {}".format( score_key ) )
                    sys.exit( 1 )

                instance_data.append( self.analyze_data[horce_id][score_key] )

            learn_data[horce_id] = instance_data

        return learn_data

    def predict( self ):
        learn_data = self.create()
        
        if len( learn_data ) == 0:
            return None

        predict_data = {}
        score_list = []

        for horce_id in learn_data.keys():
            predict_data[horce_id] = self.model.predict( [ learn_data[horce_id] ] )[0]

        return predict_data
