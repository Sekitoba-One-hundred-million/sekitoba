from data_manage.storage import Storage
from config import name

def money( horce_id, storage: Storage, data ):
    money = storage.past_data[horce_id].get_money()

    if not money == 0:
        money += 100

    users_money = money / 200
    rank_money = money
    data[horce_id][name.money+".users"] = users_money
    data[horce_id][name.money+".rank"] = rank_money
