from data_manage.storage import Storage
from config import name

def before_popular( horce_id, storage: Storage, data ):
    data[horce_id][name.before_popular] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_popular] = int( before_cd.popular() )
