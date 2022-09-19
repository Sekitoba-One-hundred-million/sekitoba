import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def trainer_rank( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    data[horce_id][name.trainer_rank+".users"] = -1
    data[horce_id][name.trainer_rank+".rank"] = -1
    dist = lib.dist_check( storage.dist )
    kind = storage.race_kind
    baba = storage.baba
        
    try:
        trainer_id = storage.data[horce_id]["trainer_id"]
        trainer_data = common_past_data.trainer_data[trainer_id]
    except:
        return

    rank_data = 0
    count = 0
        
    for day in trainer_data.keys():
        for race_num in trainer_data[day].keys():
            check_dist, check_kind = lib.dist( trainer_data[day][race_num]["dist"] )
            check_baba = lib.baba( trainer_data[day][race_num]["baba"] )

            try:
                rank = int( trainer_data[day][race_num]["rank"] )
            except:
                continue
                
            if dist == check_dist:
                rank_data += rank
                count += 1

            if baba == check_baba:
                rank_data += rank
                count += 1
                    
            if kind == check_kind:
                rank_data += rank
                count += 1

    if not count == 0:
        rank_data /= count

    data[horce_id][name.trainer_rank+".users"] = int( rank_data )
    data[horce_id][name.trainer_rank+".rank"] = rank_data
