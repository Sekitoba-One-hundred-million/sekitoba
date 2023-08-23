from data_manage.storage import Storage
from config import name

def all_horce_num( horce_id, storage: Storage, data ):
    data[horce_id][name.all_horce_num+".users"] = storage.all_horce_num
    data[horce_id][name.all_horce_num+".rank"] = storage.all_horce_num
