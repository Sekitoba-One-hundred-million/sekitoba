from data_manage.storage import Storage
from config import name

def weight( horce_id, storage: Storage, data ):
    try:
        self.data[horce_id][name.weight] = int( storage.data[horce_id]["weight"] / 10 )
    except:
        self.data[horce_id][name.weight] = 0
