import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def limb_horce_number( horce_id, storage: Storage, data ):
    limb_math = lib.limb_search( storage.past_data[horce_id] )
    horce_num = storage.data[horce_id]["horce_num"]
    data[horce_id][name.limb_horce_number] = int( limb_math * 100 + int( horce_num / 2 ) )
