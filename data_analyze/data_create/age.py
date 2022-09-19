from data_manage.storage import Storage
from config import name

def age( horce_id, storage: Storage, data ):
    current_year = int( storage.race_id[0:4] )
    horce_birth_day = int( horce_id[0:4] )
    data[horce_id][name.age+".users"] = current_year - horce_birth_day
    data[horce_id][name.age+".rank"] = current_year - horce_birth_day
