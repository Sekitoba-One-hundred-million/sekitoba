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

    return users_data_dict
