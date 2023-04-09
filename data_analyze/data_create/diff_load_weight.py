from data_manage.storage import Storage
from config import name

def diff_load_weight( horce_id, storage: Storage, data ):
    before_cd = storage.past_data[horce_id].before_cd()

    try:
        dlw = int( before_cd.burden_weight() - storage.data[horce_id]["burden_weight"] )
        data[horce_id][name.diff_load_weight+".users"] = dlw
        data[horce_id][name.diff_load_weight+".rank"] = dlw
    except:
        data[horce_id][name.diff_load_weight+".users"] = 100
        data[horce_id][name.diff_load_weight+".rank"] = 100
