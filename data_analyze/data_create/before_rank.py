from data_manage.storage import Storage
from config import name

def before_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.before_rank+".users"] = -1
    data[horce_id][name.before_rank+".rank"] = -1
    before_cd = storage.past_data[horce_id].before_cd()
    
    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_rank+".users"] = int( before_cd.rank() )
        data[horce_id][name.before_rank+".rank"] = before_cd.rank()
