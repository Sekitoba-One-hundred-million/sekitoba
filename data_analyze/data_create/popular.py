from data_manage.storage import Storage
from config import name

def popular( horce_id, storage: Storage, data ):
    try:
        data[horce_id][name.popular+".users"] = storage.data[horce_id]["popular"]
        data[horce_id][name.popular+".rank"] = storage.data[horce_id]["popular"]
    except:
        data[horce_id][name.popular+".users"] = -1
        data[horce_id][name.popular+".rank"] = -1
