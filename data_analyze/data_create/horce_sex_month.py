from data_manage.storage import Storage
from config import name

def horce_sex_month( horce_id, storage: Storage, data ):
    month = int( storage.today_data.month )
    horce_sex = storage.data[horce_id]["sex"]
    data[horce_id][name.horce_sex_month] = int( month * 10 + horce_sex )
