from data_manage.storage import Storage
from config import name

def up3_standard_value( horce_id, storage: Storage, data ):
    data[horce_id][name.up3_standard_value+".users"] = 100
    data[horce_id][name.up3_standard_value+".rank"] = 100
    before_cd = storage.past_data[horce_id].before_cd()

    if before_cd == None:
        return

    p1, p2 = before_cd.pace()
    up3 = before_cd.up_time()
    up3_standard_value = max( min( ( up3 - p2 ) * 5, 15 ), -10 )
    data[horce_id][name.up3_standard_value+".users"] = up3_standard_value
    data[horce_id][name.up3_standard_value+".rank"] = up3_standard_value
