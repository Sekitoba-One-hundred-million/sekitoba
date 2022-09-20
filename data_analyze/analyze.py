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

USERS_DATA_FILE_NAME = "users_data_instance.pickle"
PROD_USERS_SCORE_DATA = "prod_users_score_data.pickle"

def main( stock_data: dict[ str, Storage] ):
    if rank == 0:
        users_data_dict: dict[ str, UsersData ] = dm.pickle_load( PROD_USERS_SCORE_DATA, prod = True )

        if users_data_dict == None:
            users_data_dict: dict[ str, UsersData ] = {}

        # 必要なレースを分割して各スレッドにお願いする
        stock_key_array = np.array( list( stock_data.keys() ) )
        stock_key_array_list = list( np.array_split( stock_key_array, int( size - 1 ) ) )

        for i in range( 0, len( stock_key_array_list ) ):
            s = i + 1
            comm.send( stock_key_array_list[i], dest = s, tag = 0 )

        # 各スレッドが処理したデータを受け取る
        for i in range( 0, len( stock_key_array_list ) ):
            s = i + 1
            file_name = comm.recv( source = s, tag = 0 )
            users_data_instance = dm.pickle_load( file_name, prod = True )

            if users_data_instance == None:
                continue

            users_data_dict.update( users_data_instance )

        dm.pickle_upload( PROD_USERS_SCORE_DATA, users_data_dict, prod = True )
        
        return users_data_dict
    else:
        file_name = USERS_DATA_FILE_NAME + ".{}".format( rank )
        users_data_instance = dm.pickle_load( file_name, prod = True )

        if users_data_instance == None:
            users_data_instance = {}
        
        stock_key_list = comm.recv( source = 0, tag = 0 )

        # 今回のレースで使用しないデータが入っている場合は削除
        delete_key_list = list( users_data_instance.keys() )
        check_key_list = []

        for sk in stock_key_list:
            check_key_list.append( lib.id_get( sk ) )

        for dk in delete_key_list:
            if not dk in check_key_list:
                users_data_instance.pop( dk, None )
    
        for k in stock_key_list:
            race_id = lib.id_get( k )
            print( "before users score create {}".format( race_id ) )
        
            if race_id in users_data_instance.keys():
                continue

            users_data_instance[race_id] = UsersData()
            users_data_instance[race_id].before_users_data_analyze( stock_data[k] )
            dm.pickle_upload( file_name, users_data_instance, prod = True )

            logger_data = ""
            for horce_id in users_data_instance[race_id].data.keys():
                for name in users_data_instance[race_id].data[horce_id].keys():
                    logger_data += "id:{} name:{} data:{}\n".format( horce_id, name, users_data_instance[race_id].data[horce_id][name] )
            logger.info( logger_data )
 
        comm.send( file_name, dest = 0, tag = 0 )
        return None
