from data_manage.storage import Storage
from config import name

def before_diff( horce_id, storage: Storage, data ):
    data[horce_id][name.before_diff] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_diff] = max( int( before_cd.diff() * 10 ), 0 )
