import sys
import json

import SekitobaLibrary as lib
import SekitobaDataManage as dm

from config import data_name
from config import prod_dir

class RecoveryScore:
    def __init__( self, analyze_data ):
        self.analyze_data = analyze_data
        self.plus_score = self.json_load( prod_dir + "/plus_score.json" )
        self.minus_score = self.json_load( prod_dir + "/minus_score.json" )
        self.use_score = self.json_load( prod_dir + "/use_score_data.json" )

        self.score_key_list = list( self.plus_score.keys() )

    def json_load( self, file_name ):
        f = open( file_name, "r" )
        json_data = json.load( f )
        f.close()

        return json_data

    def create( self ):
        recovery_data = {}

        for horce_id in self.analyze_data.keys():
            if horce_id == "pace":
                continue

            recovery_data[horce_id] = {}

            for score_key in self.score_key_list:
                if not self.use_score[score_key]:
                    continue

                if not score_key in self.analyze_data[horce_id]:
                    print( "not found {}".format( score_key ) )
                    sys.exit( 1 )

                if self.analyze_data[horce_id][score_key] == None:
                    print( "score None {}".format( score_key ) )
                    sys.exit( 1 )

                recovery_data[horce_id][score_key] = self.analyze_data[horce_id][score_key]

        for horce_id in recovery_data.keys():
            recovery_data[horce_id][data_name.jockey_year_rank] = int( recovery_data[horce_id][data_name.jockey_year_rank] / 10 )
            recovery_data[horce_id][data_name.level_score] = int( recovery_data[horce_id][data_name.level_score] * 10 )

            for score_key in recovery_data[horce_id].keys():
                recovery_data[horce_id][score_key] = int( recovery_data[horce_id][score_key] )

        return recovery_data

    def predict( self ):
        recovery_score_data = {}
        recovery_data = self.create()

        for horce_id in recovery_data.keys():
            recovery_score_data[horce_id] = 0
            
            for score_key in recovery_data[horce_id].keys():                
                if recovery_data[horce_id][score_key] in self.plus_score[score_key]:
                    recovery_score_data[horce_id] += 1
                elif recovery_data[horce_id][score_key] in self.minus_score[score_key]:
                    recovery_score_data[horce_id] -= 1

        return recovery_score_data
