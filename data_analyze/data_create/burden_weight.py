from data_manage.storage import Storage
from config import name

def burden_weight( horce_id, storage: Storage, data ):
    try:
        data[horce_id][name.burden_weight+".users"] = min( storage.data[horce_id]["burden_weight"] - 50, 0 )
        data[horce_id][name.burden_weight+".rank"] = storage.data[horce_id]["burden_weight"]
    except:
        data[horce_id][name.burden_weight+".users"] = 0
        data[horce_id][name.burden_weight+".rank"] = 0
