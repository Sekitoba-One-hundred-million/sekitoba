import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def race_money( horce_id, storage: Storage, data ):
    money_class = lib.money_class_get( storage.race_money )
    data[horce_id][name.race_money+".users"] = money_class
    data[horce_id][name.race_money+".rank"] = money_class
