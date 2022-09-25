import sekitoba_library as lib

from data_manage.storage import Storage
from config import name

def father_blood_type( horce_id, storage: Storage, data ):
    dist_kind = lib.dist_check( storage.dist )
    
    if horce_id in storage.data["father_blood_type"]:
        score = int( dist_kind * 10 + storage.data["father_blood_type"][horce_id] )
        data[horce_id][name.father_blood_type+".users"] = score
        data[horce_id][name.father_blood_type+".rank"] = score
    else:
        data[horce_id][name.father_blood_type+".users"] = -1
        data[horce_id][name.father_blood_type+".rank"] = -1
