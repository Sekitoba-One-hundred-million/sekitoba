import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def true_skill_index( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    data[horce_id][name.true_skill_index+".users"] = -1
    data[horce_id][name.true_skill_index+".rank"] = -1

    true_skill_list = []
    my_true_skill = -1
    
    for check_horce_id in storage.horce_id_list:
        before_cd = storage.past_data[check_horce_id].before_cd()

        if before_cd == None:
            continue

        before_race_id = before_cd.race_id()

        try:
            ts = common_past_data.true_skill_data[before_race_id][check_horce_id]
        except:
            continue

        if horce_id == check_horce_id:
            my_true_skill = ts

        true_skill_list.append( ts )

    if not my_true_skill == -1:
        true_skill_list = sorted( true_skill_list, reverse = True )
        data[horce_id][name.true_skill_index+".users"] = true_skill_list.index( my_true_skill )
        data[horce_id][name.true_skill_index+".rank"] = true_skill_list.index( my_true_skill )
