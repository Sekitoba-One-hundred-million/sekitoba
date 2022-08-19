from data_manage.storage import Storage
from config import name

def baba( horce_id, storage: Storage, data ):
    data[horce_id][name.baba] = storage.baba
