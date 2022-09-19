import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def race_interval( horce_id, storage: Storage, data ):
    ymd = [ storage.today_data.year, storage.today_data.month, storage.today_data.day ]
    
    try:
        data[horce_id][name.race_interval+".users"] = min( max( storage.past_data[horce_id].race_interval( ymd = ymd ), 0 ), 20 )
        data[horce_id][name.race_interval+".rank"] = min( max( storage.past_data[horce_id].race_interval( ymd = ymd ), 0 ), 20 )
    except:
        data[horce_id][name.race_interval+".users"] = -1
        data[horce_id][name.race_interval+".rank"] = -1
