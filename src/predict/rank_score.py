import sys
import numpy as np

import SekitobaLibrary as lib
import SekitobaDataManage as dm
from SekitobaLogger import logger

from predict.lib import *
from config import pickle_name
from config import prod_dir

dm.dl.file_set( pickle_name.rank_model )

class RankScore:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.models = dm.dl.data_get( pickle_name.rank_model )

        self.log_data = {}
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/rank_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.textReplace( str_data ) )

    def create( self ):
        learn_data = {}
        move_odds_rate = ramdom_odds_rate( list( self.analyze_data.keys() ) )
        not_found = False
        
        for horce_id in self.analyze_data.keys():
            instance_data = []
            
            for score_key in self.score_key_list:
                if not score_key in self.analyze_data[horce_id]:
                    print( "not found {}".format( score_key ) )
                    not_found = True
                    continue

                if self.analyze_data[horce_id][score_key] == None:
                    print( "score None {}".format( score_key ) )
                    sys.exit( 1 )

                score = self.analyze_data[horce_id][score_key]

                if score_key == "odds":
                    score += score * move_odds_rate[horce_id]
                    score = round( score, 1 )
                
                instance_data.append( score )
                lib.dicAppend( self.log_data, horce_id, {} )
                self.log_data[horce_id][score_key] = score

            if not_found:
                sys.exit( 1 )

            learn_data[horce_id] = instance_data

        return learn_data

    def predict( self ):
        predict_data = {}
        N = len( self.models )

        for i in range( roop_count ):
            learn_data = self.create()
        
            if len( learn_data ) == 0:
                return None

            for horce_id in learn_data.keys():
                lib.dicAppend( predict_data, horce_id, 0 )

                for model in self.models:
                    predict_data[horce_id] += model.predict( [ learn_data[horce_id] ] )[0]

        for horce_id in predict_data.keys():
            predict_data[horce_id] /= N
            
        return predict_data
