import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def speed_index( horce_id, storage: Storage, data ):
    my_speed_index = 0
    speed_index_list = []

    for diff_horce_id in storage.horce_id_list:
        speed, up_speed, pace_speed = storage.past_data[diff_horce_id].speed_index( storage.data[horce_id]["baba_index"] )
        speed_inedx = lib.max_check( speed ) + lib.max_check( up_speed ) + lib.max_check( pace_speed ) + lib.max_check( storage.data[horce_id]["time_index"] )
        speed_index_list.append( speed_inedx )

        if diff_horce_id == horce_id:
            my_speed_index = speed_inedx

    speed_index_list = sorted( speed_index_list, reverse = True )
    data[horce_id][name.speed_index+".users"] = speed_index_list.index( my_speed_index )
    data[horce_id][name.speed_index+".rank"] = speed_index_list.index( my_speed_index )
