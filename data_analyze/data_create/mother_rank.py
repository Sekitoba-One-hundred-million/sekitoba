from data_manage.storage import Storage
from config import name

def mother_rank( horce_id, storage: Storage, data ):
    mother_id = storage.data[horce_id]["parent_id"]["mother"]
    mother_pd = storage.past_data[mother_id]
    place_num = storage.place_num
    baba_status = storage.baba
    dist_kind = lib.dist_check( storage.dist )
    data[horce_id][name.mother_rank] = lib.match_rank_score( mother_pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )

