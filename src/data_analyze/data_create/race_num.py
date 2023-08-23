from data_manage.storage import Storage
from config import name

def race_num( horce_id, storage: Storage, data ):
    n = len( storage.race_id )
    race_num = int( storage.race_id[int(n-2):n] )
    data[horce_id][name.race_num+".users"] = race_num
    data[horce_id][name.race_num+".rank"] = race_num
