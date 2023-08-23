import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def limb( horce_id, storage: Storage, data ):
    limb_math = lib.limb_search( storage.past_data[horce_id] )
    data[horce_id][name.limb+".users"] = limb_math
    data[horce_id][name.limb+".rank"] = limb_math
