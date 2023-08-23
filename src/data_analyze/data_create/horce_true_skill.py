import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def horce_true_skill( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    try:
        data[horce_id][name.horce_true_skill+".users"] = int( common_past_data.true_skill_data["horce"][horce_id] )
        data[horce_id][name.horce_true_skill+".rank"] = common_past_data.true_skill_data["horce"][horce_id]
    except:
        data[horce_id][name.horce_true_skill+".users"] = 25
        data[horce_id][name.horce_true_skill+".rank"] = 25        
