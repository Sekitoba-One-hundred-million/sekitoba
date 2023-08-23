import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def trainer_true_skill( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    try:
        trainer_id = storage.data[horce_id]["trainer_id"]
        data[horce_id][name.trainer_true_skill+".users"] = int( common_past_data.true_skill_data["trainer"][trainer_id] )
        data[horce_id][name.trainer_true_skill+".rank"] = common_past_data.true_skill_data["trainer"][trainer_id]
    except:
        data[horce_id][name.trainer_true_skill+".users"] = 25
        data[horce_id][name.trainer_true_skill+".rank"] = 25        
