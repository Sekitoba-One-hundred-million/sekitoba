from data_manage.storage import Storage
from config import name

def jockey_year_rank( horce_id, storage: Storage, data ):
    year = int( storage.today_data.year )
    key_before_year = str( int( year - 1 ) )
    
    try:
        data[horce_id][name.jockey_year_rank] = int( storage.data[horce_id]["jockey_year_rank"][key_before_year] / 10 )
    except:
        data[horce_id][name.jockey_year_rank] = -1
