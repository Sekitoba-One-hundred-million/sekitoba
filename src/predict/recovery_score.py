import sys
import numpy as np

import SekitobaLibrary as lib
import SekitobaDataManage as dm
from SekitobaLogger import logger
from SekitobaLibrary import ManageRecoveryScore

from predict.lib import *
from config import pickle_name
from config import prod_dir

dm.dl.file_set( "recovery_cluster_data.pickle" )

class RecoveryScore:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.model = dm.dl.data_get( "recovery_cluster_data.pickle" )
        self.data_type = self.model["type"]
        self.log_data = {}
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( prod_dir + "/recovery_score_data_name.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

    def create( self ):
        learn_data = {}
        not_found = False
        
        for horce_id in self.analyze_data.keys():            
            for score_key in self.score_key_list:
                if not score_key in self.analyze_data[horce_id]:
                    print( "not found {}".format( score_key ) )
                    not_found = True
                    continue

                if self.analyze_data[horce_id][score_key] == None:
                    print( "score None {}".format( score_key ) )
                    sys.exit( 1 )

                score = self.analyze_data[horce_id][score_key]

                if self.data_type[score_key] == int:
                    score = int( score )

                lib.dic_append( learn_data, score_key, [] )
                learn_data[score_key].append( score )
                lib.dic_append( self.log_data, horce_id, {} )
                self.log_data[horce_id][score_key] = score

            if not_found:
                sys.exit( 1 )
            
        return learn_data

    def predict( self ):
        predict_data = {}
        learn_data = self.create()
        
        if len( learn_data ) == 0:
            return None

        for score_key in learn_data.keys():
            if self.data_type[score_key] == float:
                learn_data[score_key] = lib.standardization( learn_data[score_key], abort = [ lib.escapeValue ] )

        for i, horce_id in enumerate( self.analyze_data.keys() ):
            score = 0
            cluster_list = self.model["cluster"]

            for cluster in cluster_list:
                manage_recovery_score = ManageRecoveryScore( {},
                                                             data_name_list = self.model["name"],
                                                             data_type = self.model["type"],
                                                             cd = cluster )
            
                for score_key in learn_data.keys():
                    score += manage_recovery_score.check_float_score( learn_data[score_key][i], score_key )

            predict_data[horce_id] = score / len( learn_data )

        return predict_data
