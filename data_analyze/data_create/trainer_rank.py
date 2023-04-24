import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

def trainer_rank( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    data[horce_id][name.trainer_rank+".users"] = -1
    data[horce_id][name.trainer_rank+".rank"] = -1

    before_year = str( int( int( storage.race_id[0:4] ) - 1 ) )
    dist = lib.dist_check( storage.dist )
    kind = storage.race_kind
    baba = storage.baba
    key_dict = { "baba": str( baba ), "dist": str( dist ), "kind": str( kind ) }

    try:
        trainer_id = storage.data[horce_id]["trainer_id"]
        trainer_data = common_past_data.trainer_data[trainer_id][before_year]
    except:
        return

    rank = 0
    count = 0
    
    for check_key in key_dict.keys():
        try:
            rank += trainer_data[check_key][key_dict[check_key]]["rank"]
            count += 1
        except:
            continue

    if not count == 0:
        rank /= count

    data[horce_id][name.trainer_rank+".users"] = int( rank )
    data[horce_id][name.trainer_rank+".rank"] = rank
