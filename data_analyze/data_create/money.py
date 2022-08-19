from data_manage.storage import Storage
from config import name

def money( horce_id, storage: Storage, data ):
    money = storage.past_data[horce_id].get_money()

    if not money == 0:
        money += 100

    money /= 200
    money = min( money, 30 )
    data[horce_id][name.money] = money
