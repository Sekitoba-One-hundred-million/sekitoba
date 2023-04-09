import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def jockey_rank( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    data[horce_id][name.jockey_rank+".users"] = -1
    data[horce_id][name.jockey_rank+".rank"] = -1
    
    dist = lib.dist_check( storage.dist )
    kind = storage.race_kind
    baba = storage.baba
    
    try:
        jockey_id = storage.data[horce_id]["jockey_id"]
        jockey_data = common_past_data.jockey_data[jockey_id]
    except:
        return

    rank_data = 0
    count = 0

    for day in jockey_data.keys():
        for race_num in jockey_data[day].keys():
            check_dist, check_kind = lib.dist( jockey_data[day][race_num]["dist"] )
            check_baba = lib.baba( jockey_data[day][race_num]["baba"] )

            try:
                rank = int( jockey_data[day][race_num]["rank"] )
            except:
                continue
                
            rank_data += rank
            count += 1

    if not count == 0:
        rank_data /= count

    data[horce_id][name.jockey_rank+".users"] = int( rank_data )
    data[horce_id][name.jockey_rank+".rank"] = rank_data
