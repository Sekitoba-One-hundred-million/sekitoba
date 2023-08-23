import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def straight_flame( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    key_place = str( int( storage.place_num ) )
    key_dist = str( int( storage.dist ) )
    key_kind = str( int( storage.race_kind ) )

    if storage.outside:
        key_dist += "外"

    straight_flame_score = -1
    
    try:
        straight_dist = int( common_past_data.race_cource_info[key_place][key_kind][key_dist]["dist"][0] / 100 )
        
        if storage.data[horce_id]["horce_num"] < storage.all_horce_num / 3:
            straight_flame_score = int( 100 + straight_dist )
        elif storage.all_horce_num / 3 < storage.data[horce_id]["horce_num"]:
            straight_flame_score = int( 200 + straight_dist )
    except:
        straight_flame_score = -1
        
    data[horce_id][name.straight_flame+".users"] = straight_flame_score
    data[horce_id][name.straight_flame+".rank"] = straight_flame_score
