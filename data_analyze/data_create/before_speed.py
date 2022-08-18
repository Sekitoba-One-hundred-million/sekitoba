from data_manage.storage import Storage
from config import name

def before_speed( horce_id, storage: Storage, data ):
    data[horce_id][name.before_speed] = -1
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_speed] = int( before_cd.speed() )
