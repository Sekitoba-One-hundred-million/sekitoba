from data_manage.storage import Storage
from config import name

def before_last_passing_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.before_last_passing_rank] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        try:
            data[horce_id][name.before_last_passing_rank] = int( before_cd.passing_rank().split( "-" )[-1] )
        except:
            data[horce_id][name.before_last_passing_rank] = 0
