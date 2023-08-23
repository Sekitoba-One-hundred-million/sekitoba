import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def father_rank( horce_id, storage: Storage, data ):
    father_id = storage.data[horce_id]["parent_id"]["father"]
    father_pd = storage.past_data[father_id]
    place_num = storage.place_num
    baba_status = storage.baba
    dist_kind = lib.dist_check( storage.dist )
    data[horce_id][name.father_rank+".users"] = lib.match_rank_score( father_pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )
    data[horce_id][name.father_rank+".rank"] = lib.match_rank_score( father_pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )
