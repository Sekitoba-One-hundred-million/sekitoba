import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def dist_kind_count( horce_id, storage: Storage, data ):
    dist_kind = lib.dist_check( storage.dist )
    data[horce_id][name.dist_kind_count] = storage.past_data[horce_id].dist_kind_count( dist_kind = dist_kind )