from data_manage.storage import Storage
from config import name

def burden_weight( horce_id, storage: Storage, data ):
    data[horce_id][name.burden_weight] = storage.data[horce_id]["burden_weight"]
