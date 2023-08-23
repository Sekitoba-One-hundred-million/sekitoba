import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def dist_kind( horce_id, storage: Storage, data ):
    dist_kind = lib.dist_check( storage.dist )
    data[horce_id][name.dist_kind+".users"] = dist_kind
    data[horce_id][name.dist_kind+".rank"] = dist_kind
