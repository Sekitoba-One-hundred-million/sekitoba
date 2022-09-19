from data_manage.storage import Storage
from config import name

def place( horce_id, storage: Storage, data ):
    data[horce_id][name.place+".users"] = storage.place_num
    data[horce_id][name.place+".rank"] = storage.place_num
