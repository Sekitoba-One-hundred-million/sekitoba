import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def jockey_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.jockey_rank] = -1
    dist = lib.dist_check( storage.dist )
    kind = storage.race_kind
    baba = storage.baba
        
    try:
        jockey_data = storage.data[horce_id]["jockey"]
    except:
        return

    rank_data = 0
    count = 0

    if jockey_data == None:
        return

    for day in jockey_data.keys():
        for race_num in jockey_data[day].keys():
            check_dist, check_kind = lib.dist( jockey_data[day][race_num]["dist"] )
            check_baba = lib.baba( jockey_data[day][race_num]["baba"] )

            try:
                rank = int( jockey_data[day][race_num]["rank"] )
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

    data[horce_id][name.jockey_rank] = rank_data