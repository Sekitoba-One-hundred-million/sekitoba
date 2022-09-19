from data_manage.storage import Storage
from config import name

def popular_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.popular_rank+".users"] = -100
    data[horce_id][name.popular_rank+".rank"] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.popular_rank+".users"] = int( before_cd.rank() - before_cd.popular() )
        data[horce_id][name.popular_rank+".rank"] = int( before_cd.rank() - before_cd.popular() )
