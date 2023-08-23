import numpy as np

import sekitoba_data_manage as dm
import sekitoba_library as lib

from data_analyze.users_data import UsersData

class RankScore:
    def __init__( self ):
        self.rank_model = dm.dl.data_get( lib.name.model_name() )
        self.rank_name_list = []
        self.rank_learn_name_create()

    def rank_learn_name_create( self ):
        f = open( "./config/rank_score_data.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.rank_name_list.append( str_data.replace( "\n", "" ) )

    def rank_score_create( self, users_data: UsersData, horce_id ):
        learn_data = []
        
        for rank_name in self.rank_name_list:
            rank_name += ".rank"
            learn_data.append( users_data.data[horce_id][rank_name] )

        score = self.rank_model.predict( np.array( [ learn_data ] ) )[0]
        return score
