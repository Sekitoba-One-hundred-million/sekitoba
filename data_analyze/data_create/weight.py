from data_manage.storage import Storage
from config import name

def weight( horce_id, storage: Storage, data ):
    try:
        data[horce_id][name.weight+".users"] = int( storage.data[horce_id]["weight"] / 10 )
        data[horce_id][name.weight+".rank"] = storage.data[horce_id]["weight"] / 10
    except:
        data[horce_id][name.weight+".users"] = 0
        data[horce_id][name.weight+".rank"] = 0
