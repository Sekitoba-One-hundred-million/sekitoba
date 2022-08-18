from data_manage.storage import Storage
from config import name

def weather( horce_id, storage: Storage, data ):
    data[horce_id][name.weather] = storage.weather
