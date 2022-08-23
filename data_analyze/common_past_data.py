import copy

import sekitoba_data_manage as dm
import sekitoba_library as lib
from data_manage.storage import Storage
from data_analyze import past_get

WRAP = "wrap"
RACEMONEY="race_money"
JOCKEY_DATA = "jockey_data"
JOCKEY_YEAR_RANK_DATA = "jockey_year_rank_data"
TRAINER_DATA = "trainer_data"

class CommonPastData:
    def __init__( self ):
        self.wrap = {}
        self.race_money = {}
        self.jockey_data = {}
        self.jockey_year_rank_data = {}
        self.trainer_data = {}
        self.data_set()

    def data_set( self ):
        past_race_data = dm.pickle_load( "prod_past_data.pickle", prod = True )

        if past_race_data == None:
            return

        if WRAP in past_race_data.keys():
            self.wrap = copy.deepcopy( past_race_data[WRAP] )

        if RACEMONEY in past_race_data.keys():
            self.race_money = copy.deepcopy( past_race_data[RACEMONEY] )

        if JOCKEY_DATA in past_race_data.keys():
            self.jockey_data = copy.deepcopy( past_race_data[JOCKEY_DATA] )

        if JOCKEY_YEAR_RANK_DATA in past_race_data.keys():
            self.jockey_year_rank_data = copy.deepcopy( past_race_data[JOCKEY_YEAR_RANK_DATA] )

        if TRAINER_DATA in past_race_data.keys():
            self.trainer_data = copy.deepcopy( past_race_data[TRAINER_DATA] )

        past_race_data.clear()

    def data_upload( self ):
        past_race_data = {}
        past_race_data[WRAP] = self.wrap
        past_race_data[RACEMONEY] = self.race_money
        past_race_data[JOCKEY_DATA] = self.jockey_data
        past_race_data[JOCKEY_YEAR_RANK_DATA] = self.jockey_year_rank_data
        past_race_data[TRAINER_DATA] = self.trainer_data
        dm.pickle_upload( "prod_past_data.pickle", prod = True )

    def data_collect( self, stock_data: dict[ str, Storage ] ):
        self.wrap_get( stock_data )
        self.race_money_get( stock_data )
        self.jockey_get( stock_data )
        self.trainer_data( stock_data )

    def collect_race_id( self, stock_data: dict[ str, Storage ], check_dict ):
        race_id_dict = {}

        for k in stock_data.keys():
            for horce_id in stock_data[k].horce_id_list:
                past_cd_list = stock_data[k].past_data[horce_id].past_cd_list()

                for past_cd in past_cd_list:
                    past_race_id = past_cd.race_id()
                    if not past_race_id in check_dict.keys():
                        race_id_dict[past_race_id] = True

        race_id_list = list( race_id_dict.keys() )
        return race_id_list

    def jockey_get( self, stock_data: dict[ str, Storage ] ):
        jockey_id_dict = {}
        
        for k in stock_data.keys():
            for horce_id in stock_data[k].horce_id_list:
                jockey_id = stock_data[k][horce_id]["jockey_id"]
                if not jockey_id in self.jockey_data.keys():
                    jockey_id_dict[jockey_id] = True

        jockey_id_list = list( jockey_id_dict.keys() )
        base_url = "https://db.netkeiba.com/?pid=jockey_detail&id="
        jockey_year_base_url = "https://db.netkeiba.com/jockey/result/"
        add_jockey_data = lib.thread_scraping( jockey_id_list, jockey_id_list ).data_get( past_get.joceky_data_collect )
        add_jockey_year_data = lib.thread_scraping( jockey_id_list, jockey_id_list ).data_get( past_get.jockey_year_rank )

        for k in add_jockey_data.keys():
            self.jockey_data[k] = add_jockey_data[k]

        for k in add_jockey_year_data.keys():
            self.jockey_year_rank_data[k] = add_jockey_year_data[k]

    def trainer_get( self, stock_data: dict[ str, Storage ] ):
        trainer_id_dict = {}
        
        for k in stock_data.keys():
            for horce_id in stock_data[k].horce_id_list:
                trainer_id = stock_data[k][horce_id]["trainer_id"]
                if not trainer_id in self.trainer_data.keys():
                    trainer_id_dict[trainer_id_dict] = True

        trainer_id_list = list( trainer_id_dict.keys() )
        add_trainer_data = lib.thread_scraping( trainer_id_list, trainer_id_list ).data_get( past_get.trainer_data_collect )

        for k in add_trainer_data.keys():
            self.trainer_data[k] = add_trainer_data[k]
        
    def wrap_get( self, stock_data: dict[ str, Storage ] ):
        race_id_list = self.collect_race_id( stock_data, self.wrap )
        wrap_add_data = lib.thread_scraping( race_id_list, race_id_list ).data_get( past_get.wrap_get )
        for k in wrap_add_data.keys():
            self.wrap[k] = wrap_add_data[k]

    def race_money_get( self, stock_data: dict[ str, Storage ] ):
        race_id_list = self.collect_race_id( stock_data, self.race_money )
        race_money_add_data = lib.thread_scraping( race_id_list, race_id_list ).data_get( past_get.race_money_get )

        for k in race_money_add_data.keys():
            self.race_money[k] = race_money_add_data[k]
