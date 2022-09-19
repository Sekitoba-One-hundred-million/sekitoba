from data_manage.storage import Storage
from data_analyze.common_past_data import CommonPastData
from config import name

def jockey_year_rank( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    year = int( storage.today_data.year )
    key_before_year = str( int( year - 1 ) )

    try:
        jockey_id = storage.data[horce_id]["jockey_id"]
        data[horce_id][name.jockey_year_rank+".users"] = int( common_past_data.jockey_year_rank_data[jockey_id][key_before_year] / 10 )
        data[horce_id][name.jockey_year_rank+".rank"] = common_past_data.jockey_year_rank_data[jockey_id][key_before_year]
    except:
        data[horce_id][name.jockey_year_rank+".users"] = -1
        data[horce_id][name.jockey_year_rank+".rank"] = -1
