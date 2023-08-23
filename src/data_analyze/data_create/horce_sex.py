from data_manage.storage import Storage
from config import name

def horce_sex( horce_id, storage: Storage, data ):
    data[horce_id][name.horce_sex+".users"] = storage.data[horce_id]["sex"]
    data[horce_id][name.horce_sex+".rank"] = storage.data[horce_id]["sex"]
