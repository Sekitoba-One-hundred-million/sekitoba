from data_manage.storage import Storage
from config import name

def horce_sex_month( horce_id, storage: Storage, data ):
    month = int( storage.today_data.month )
    horce_sex = storage.data[horce_id]["sex"]

    try:
        data[horce_id][name.horce_sex_month+".users"] = int( month * 10 + horce_sex )
        data[horce_id][name.horce_sex_month+".rank"] = int( month * 10 + horce_sex )
    except:
        data[horce_id][name.horce_sex_month+".users"] = -1
        data[horce_id][name.horce_sex_month+".rank"] = -1
