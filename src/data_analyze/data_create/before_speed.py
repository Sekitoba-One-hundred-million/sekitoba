from data_manage.storage import Storage
from config import name

def before_speed( horce_id, storage: Storage, data ):
    data[horce_id][name.before_speed+".rank"] = -1
    data[horce_id][name.before_speed+".users"] = -1
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_speed+".rank"] = int( before_cd.speed() )
        data[horce_id][name.before_speed+".users"] = before_cd.speed()
