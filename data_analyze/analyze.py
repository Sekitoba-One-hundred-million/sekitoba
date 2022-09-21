import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm
from config import name
from sekitoba_logger import logger
from data_analyze.users_data import UsersData
from data_manage.storage import Storage
from data_analyze.common_past_data import CommonPastData

def main( stock_data: dict[ str, Storage] ):
    users_data_dict: dict[ str, UsersData ] = {}
            
    for k in stock_data.keys():
        race_id = lib.id_get( k )
        print( "before users score create {}".format( race_id ) )
        
        users_data_dict[race_id] = UsersData()
        users_data_dict[race_id].before_users_data_analyze( stock_data[k] )

        logger_data = ""
        for horce_id in users_data_dict[race_id].data.keys():
            for name in users_data_dict[race_id].data[horce_id].keys():
                logger_data += "id:{} name:{} data:{}\n".format( horce_id, name, users_data_dict[race_id].data[horce_id][name] )
                
        logger.info( logger_data )

    return users_data_dict
