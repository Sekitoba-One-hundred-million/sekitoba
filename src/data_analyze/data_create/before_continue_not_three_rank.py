from data_manage.storage import Storage
from config import name

def before_continue_not_three_rank( horce_id, storage: Storage, data ):
    data[horce_id][name.before_continue_not_three_rank+".users"] = storage.past_data[horce_id].before_continue_not_three_rank()
    data[horce_id][name.before_continue_not_three_rank+".rank"] = storage.past_data[horce_id].before_continue_not_three_rank()
