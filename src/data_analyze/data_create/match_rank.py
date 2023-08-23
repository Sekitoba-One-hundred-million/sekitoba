import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def match_rank( horce_id, storage: Storage, data ):
    pd = storage.past_data[horce_id]
    place_num = storage.place_num
    baba_status = storage.baba
    dist_kind = lib.dist_check( storage.dist )
    match_rank = lib.match_rank_score( pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )
    data[horce_id][name.match_rank+".users"] = match_rank
    data[horce_id][name.match_rank+".rank"] = match_rank
