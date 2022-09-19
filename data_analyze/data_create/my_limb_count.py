import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def my_limb_count( horce_id, storage: Storage, data ):
    data[horce_id][name.limb+".rank"] = -1
    data[horce_id][name.limb+".users"] = -1
    check_limb = {}
    my_limb_key = ""

    for hi in storage.horce_id_list:
        limb = lib.limb_math( storage.past_data[hi] )
        key_limb = str( int( limb ) )
        lib.dic_append( check_limb, key_limb, 0 )
        check_limb[key_limb] += 1

        if hi == horce_id:
            my_limb_key = key_limb

    if len( my_limb_key ) == 0:
        return
        
    data[horce_id][name.my_limb_count+".users"] = check_limb[my_limb_key]
    data[horce_id][name.my_limb_count+".rank"] = check_limb[my_limb_key]
