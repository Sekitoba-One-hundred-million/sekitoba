from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_data_create.before_data import BeforeData
from data_manage.storage import Storage
from config import name

before_data = BeforeData()

def before_pace( horce_id, storage: Storage, data, past_race_data ):
    storage.data[horce_id][name.before_pace] = -100
    before_cd = storage.past_data[horce_id].before_cd()

    if before_cd == None or not before_cd.race_check():
        return

    try:
        before_wrap = past_race_data[before_cd.race_id()]
    except:
        before_wrap = {}
        
    storage.data[horce_id][name.before_pace] = before_data.pace( None, prod_before_wrap = before_wrap )
