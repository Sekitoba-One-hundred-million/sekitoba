import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def true_skill( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    data[horce_id][name.true_skill] = -1
    before_cd = storage.past_data[horce_id].before_cd()

    if before_cd == None:
        return

    before_race_id = before_cd.race_id()
    data[horce_id][name.true_skill] = common_past_data.true_skill_data[before_race_id][horce_id]
