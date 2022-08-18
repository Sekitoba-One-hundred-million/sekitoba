from data_manage.storage import Storage
from config import name

def popular( horce_id, storage: Storage, data ):
    try:
        data[horce_id][name.popular] = storage.data[horce_id]["popular"]
    except:
        data[horce_id][name.popular] = -1
