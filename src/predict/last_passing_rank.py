import sys
import numpy as np

import SekitobaLibrary as lib
import SekitobaDataManage as dm

from predict.lib import *
from config import pickle_name
from config import prod_dir

dm.dl.file_set( "last_passing_rank_model.pickle" )

class LastPassingRank:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.modelList = dm.dl.data_get( "last_passing_rank_model.pickle" )
        self.log_data = {}
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/last_passing_rank_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

    def create( self ):
        learn_data = {}
        #move_odds_rate = ramdom_odds_rate( list( self.analyze_data.keys() ) )
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
                instance_data.append( score )
                lib.dic_append( self.log_data, horce_id, {} )
                self.log_data[horce_id][score_key] = score
                
            learn_data[horce_id] = instance_data

        if not_found:
            sys.exit( 1 )

        return learn_data

    def predict( self ):
        predict_data = {}
        score_list = []
        learn_data = self.create()
        
        if len( learn_data ) == 0:
            return None

        for horce_id in learn_data.keys():
            lib.dic_append( predict_data, horce_id, {} )
            lib.dic_append( predict_data[horce_id], "score", 0 )
            score = 0

            for model in self.modelList:
                score += model.predict( [ learn_data[horce_id] ] )[0]
                
            predict_data[horce_id]["score"] += ( score / len( self.modelList ) )
            score_list.append( predict_data[horce_id]["score"] )

        stand_score_list = lib.standardization( score_list )
        sort_score_list = sorted( score_list, reverse = True )

        for i, horce_id in enumerate( predict_data.keys() ):
            predict_data[horce_id]["index"] = sort_score_list.index( predict_data[horce_id]["score"] )
            predict_data[horce_id]["stand"] = stand_score_list[i]

        return predict_data
