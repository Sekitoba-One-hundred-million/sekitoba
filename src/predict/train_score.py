import sys

import SekitobaLibrary as lib
import SekitobaDataManage as dm
from SekitobaLogger import logger

from config import pickle_name
from config import prod_dir

class TrainScore:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data

        self.log_data = {}
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/train_score_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.textReplace( str_data ) )

    def create( self ):
        learn_data = {}
        
        for horce_id in self.analyze_data.keys():
            instance_data = []

            not_found = False
            for score_key in self.score_key_list:
                if not score_key in self.analyze_data[horce_id]:
                    print( "not found {}".format( score_key ) )
                    not_found = True
                    continue
                    #sys.exit( 1 )

                if self.analyze_data[horce_id][score_key] == None:
                    print( "score None {}".format( score_key ) )
                    sys.exit( 1 )

                instance_data.append( self.analyze_data[horce_id][score_key] )
                lib.dicAppend( self.log_data, horce_id, {} )
                self.log_data[horce_id][score_key] = self.analyze_data[horce_id][score_key]
                
            if not_found:
                sys.exit( 1 )

            learn_data[horce_id] = instance_data

        return learn_data

    def predict( self ):
        learn_data = self.create()
        
        if len( learn_data ) == 0:
            return None

        score_list = []
        predict_data = {}

        for horce_id in learn_data.keys():
            predict_data[horce_id] = {}
            predict_data[horce_id]["score"] = self.model.predict( [ learn_data[horce_id] ] )[0]
            score_list.append( predict_data[horce_id]["score"] )

        stand_score_list = lib.standardization( score_list )
        sort_score_list = sorted( score_list, reverse = True )

        for i, horce_id in enumerate( learn_data.keys() ):
            predict_data[horce_id]["stand"] = stand_score_list[i]
            predict_data[horce_id]["index"] = sort_score_list.index( predict_data[horce_id]["score"] )

        return predict_data
