import copy

import sekitoba_data_manage as dm
import sekitoba_library as lib
from data_manage.storage import Storage

WRAP_DATA = "wrap_data.pickle"
RACE_MONEY_DATA = "race_money_data.pickle"
JOCKEY_DATA = "prod_jockey_data.pickle"
JOCKEY_YEAR_RANK_DATA = "jockey_year_rank_data.pickle"
TRAINER_DATA = "prod_trainer_data.pickle"
TRUE_SKILL_DATA = "true_skill_data.pickle"

dm.dl.file_set( WRAP_DATA )
dm.dl.file_set( RACE_MONEY_DATA )
dm.dl.file_set( JOCKEY_DATA )
dm.dl.file_set( JOCKEY_YEAR_RANK_DATA )
dm.dl.file_set( TRAINER_DATA )
dm.dl.file_set( TRUE_SKILL_DATA )

class CommonPastData:
    def __init__( self ):
        self.wrap = dm.dl.data_get( WRAP_DATA )
        self.race_money = dm.dl.data_get( RACE_MONEY_DATA )
        self.jockey_data = dm.dl.data_get( JOCKEY_DATA )
        self.jockey_year_rank_data = dm.dl.data_get( JOCKEY_YEAR_RANK_DATA )
        self.trainer_data = dm.dl.data_get( TRAINER_DATA )
        self.true_skill_data = dm.dl.data_get( TRUE_SKILL_DATA )
