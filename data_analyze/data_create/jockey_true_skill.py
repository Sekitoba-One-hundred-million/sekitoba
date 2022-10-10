import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def jockey_true_skill( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    try:
        jockey_id = storage.data[horce_id]["jockey_id"]
        data[horce_id][name.jockey_true_skill+".users"] = int( common_past_data.true_skill_data["jockey"][jockey_id] )
        data[horce_id][name.jockey_true_skill+".rank"] = common_past_data.true_skill_data["jockey"][jockey_id]
    except:
        data[horce_id][name.jockey_true_skill+".users"] = 25
        data[horce_id][name.jockey_true_skill+".rank"] = 25        
