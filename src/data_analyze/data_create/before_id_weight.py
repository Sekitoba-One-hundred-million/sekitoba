from data_manage.storage import Storage
from config import name

def division( score, d ):
    if score < 0:
        score *= -1
        score /= d
        score *= -1
    else:
        score /= d
            
    return int( score )

def before_id_weight( horce_id, storage: Storage, data ):
    data[horce_id][name.before_id_weight+".users"] = 100
    data[horce_id][name.before_id_weight+".rank"] = 100
    before_cd = storage.past_data[horce_id].before_cd()

    if not before_cd == None and before_cd.race_check():
        data[horce_id][name.before_id_weight+".users"] = division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )
        data[horce_id][name.before_id_weight+".rank"] = division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )
