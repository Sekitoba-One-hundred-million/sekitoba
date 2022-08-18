import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def limb( horce_id, storage: Storage, data ):
    data[horce_id][name.limb] = lib.limb_search( storage.past_data[horce_id] )
