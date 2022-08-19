import sekitoba_library as lib
import sekitoba_data_manage as dm
from config import name
from sekitoba_logger import logger
from data_analyze.users_data import UsersData
from data_manage.storage import Storage

from data_analyze import past_get

def past_data_get( stock_data: dict[ str, Storage ], past_race_data ):
    print( "past start" )
    past_race_id_dict = {}
    
    for k in stock_data.keys():
        for horce_id in stock_data[k].past_data.keys():
            pact_cd_list = stock_data[k].past_data[horce_id].past_cd_list()

            for pace_cd in pact_cd_list:
                past_race_id_dict[pace_cd.race_id()] = True

    if past_race_data == None:
        past_race_data = {}
        past_race_data["wrap"] = {}
        past_race_data["race_money"] = {}
    
    race_id_list = []
    
    for race_id in past_race_id_dict.keys():
        if not race_id in past_race_data["wrap"].keys() or not race_id in past_race_data["race_money"].keys():
            race_id_list.append( race_id )
    
    wrap_add_data = lib.thread_scraping( race_id_list, race_id_list ).data_get( past_get.wrap_get )
    race_money_add_data = lib.thread_scraping( race_id_list, race_id_list ).data_get( past_get.race_money_get )

    for k in race_money_add_data.keys():
        past_race_data["wrap"][k] = wrap_add_data[k]
        past_race_data["race_money"][k] = race_money_add_data[k]

    dm.pickle_upload( "prod_past_data.pickle", past_race_data,  prod = True )
    return past_race_data

def main( stock_data: dict[ str, Storage] ):
    past_race_data = dm.pickle_load( "prod_past_data.pickle", prod = True )
    past_race_data = past_data_get( stock_data, past_race_data )
    
    users_data_dict: dict[ str, UsersData ] = dm.pickle_load( "prod_users_score_data.pickle", prod = True )

    if users_data_dict == None:
        users_data_dict: dict[ str, UsersData ] = {}
    
    for k in stock_data.keys():
        race_id = lib.id_get( k )
        print( "before users score create {}".format( race_id ) )
        
        if race_id in users_data_dict.keys():
            continue

        users_data_dict[race_id] = UsersData()
        users_data_dict[race_id].before_users_data_analyze( stock_data[k], past_race_data )

        for horce_id in users_data_dict[race_id].data.keys():
            for name in users_data_dict[race_id].data[horce_id].keys():
                logger.info( "id:{} name:{} data:{}\n".format( horce_id, name, users_data_dict[race_id].data[horce_id][name] ) )
            
        dm.pickle_upload( "prod_users_score_data.pickle", users_data_dict, prod = True )

    return users_data_dict
