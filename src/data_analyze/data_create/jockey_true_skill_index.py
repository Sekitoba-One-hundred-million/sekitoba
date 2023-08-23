import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def jockey_true_skill_index( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    my_true_skill = None
    true_skill_list = []

    for diff_horce_id in storage.horce_id_list:
        try:
            jockey_id = storage.data[horce_id]["jockey_id"]
            true_skill = common_past_data.true_skill_data["jockey"][jockey_id]
            true_skill_list.append( true_skill )

            if diff_horce_id == horce_id:
                my_true_skill = true_skill
        except:
            true_skill_list.append( 25 )
            continue

    true_skill_list = sorted( true_skill_list, reverse = True )
    if my_true_skill == None:
        data[horce_id][name.jockey_true_skill_index+".users"] = -1
        data[horce_id][name.jockey_true_skill_index+".rank"] = -1
    else:
        data[horce_id][name.jockey_true_skill_index+".users"] = int( true_skill_list.index( my_true_skill ) )
        data[horce_id][name.jockey_true_skill_index+".rank"] = true_skill_list.index( my_true_skill )
