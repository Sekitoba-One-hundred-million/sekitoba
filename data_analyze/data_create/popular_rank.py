from data_manage.storage import Storage
from config import name

def popular_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.popular_rank] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.popular_rank] = int( before_cd.rank() - before_cd.popular() )
