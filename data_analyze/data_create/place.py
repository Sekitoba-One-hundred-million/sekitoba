from data_manage.storage import Storage
from config import name

def place( horce_id, storage: Storage, data ):
    data[horce_id][name.place] = storage.place_num
