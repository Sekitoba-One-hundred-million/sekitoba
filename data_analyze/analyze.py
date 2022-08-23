import numpy as np
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm
from config import name
from sekitoba_logger import logger
from data_analyze.users_data import UsersData
from data_manage.storage import Storage
from data_analyze.common_past_data import CommonPastData

comm = MPI.COMM_WORLD   #COMM_WORLDは全体
size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

PROD_USERS_SCORE_DATA = "prod_users_score_data.pickle"

def main( stock_data: dict[ str, Storage] ):
    common_past_data = CommonPastData()
    common_past_data.data_collect( stock_data )
    common_past_data.data_upload()
    
    users_data_dict: dict[ str, UsersData ] = dm.pickle_load( PROD_USERS_SCORE_DATA, prod = True )

    if users_data_dict == None:
        users_data_dict: dict[ str, UsersData ] = {}

    if rank == 0:
        stock_key_array = np.array( list( stock_data.keys() ) )
        stock_key_array_list = list( np.array_split( stock_key_array, int( size - 1 ) ) )

        for i in range( 0, len( stock_key_array_list ) ):
            s = i + 1
            comm.send( stock_key_array_list[i], dest = s, tag = 0 )

        else:
            stock_key_list = comm.recv( source = 0, tag = 0 )
    
            for k in stock_key_list:
                race_id = lib.id_get( k )
                print( "before users score create {}".format( race_id ) )
        
                if race_id in users_data_dict.keys():
                    continue

                users_data_dict[race_id] = UsersData()
                users_data_dict[race_id].before_users_data_analyze( stock_data[k], common_past_data )

        for horce_id in users_data_dict[race_id].data.keys():
            for name in users_data_dict[race_id].data[horce_id].keys():
                logger.info( "id:{} name:{} data:{}".format( horce_id, name, users_data_dict[race_id].data[horce_id][name] ) )
            
        dm.pickle_upload( PROD_USERS_SCORE_DATA, users_data_dict, prod = True )

    return users_data_dict
