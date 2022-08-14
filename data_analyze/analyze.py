import sekitoba_library as lib
import sekitoba_data_manage as dm
from config import name
from sekitoba_logger import logger
from data_analyze.users_data import UsersData
from data_manage.storage import Storage

def main( stock_data: dict[str, Storage] ):
    users_data_dict: dict[ str, UsersData ] = dm.pickle_load( "prod_users_score_data", prod = True )

    if users_data_dict == None:
        users_data_dict: dict[ str, UsersData ] = {}
    
    for k in stock_data.keys():
        race_id = lib.id_get( k )
        print( "before users score create {}".format( race_id ))
        
        if race_id in users_data_dict.keys():
            continue

        users_data_dict[race_id] = UsersData()
        users_data_dict[race_id].before_users_data_analyze( stock_data[k] )

        for horce_id in users_data_dict[race_id].data.keys():
            for name in users_data_dict[race_id].data[horce_id].keys():
                logger.info( "id:{} name:{} data:{}\n".format( horce_id, name, users_data_dict[race_id].data[horce_id][name] ) )
                
        dm.pickle_upload( "prod_users_score_data", users_data_dict, prod = True )

    return users_data_dict
