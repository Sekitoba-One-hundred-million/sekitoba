from data_manage.storage import Storage
from config import name

def horce_num( horce_id, storage: Storage, data ):
    data[horce_id][name.horce_num] = storage.data[horce_id]["horce_num"]