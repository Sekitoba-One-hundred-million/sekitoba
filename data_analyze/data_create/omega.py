from data_manage.storage import Storage
from config import name

def omega( horce_id, storage: Storage, data ):
    horce_num = storage.data[horce_id]["horce_num"]
    key_horce_num = str( int( horce_num ) )
    try:
        data[horce_id][name.omega] = int( storage.data["omega"][key_horce_num] / 5 )
    except:
        data[horce_id][name.omega] = -1
