from data_manage.storage import Storage
from config import name

def burden_weight( horce_id, storage: Storage, data ):
    try:
        data[horce_id][name.burden_weight] = min( storage.data[horce_id]["burden_weight"] - 50, 0 )
    except:
        data[horce_id][name.burden_weight] = 0
