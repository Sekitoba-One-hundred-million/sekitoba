from sekitoba_data_create.train_index_get import TrainIndexGet
from data_manage.storage import Storage
from config import name

train_index_get = TrainIndexGet()

def train_score( horce_id, storage: Storage, data ):
    train_index = train_index_get.score_get( None, storage.data[horce_id]["horce_num"], prod_train_data = storage.data["train"] )
    data[horce_id][name.train_score+".users"] = train_index
    data[horce_id][name.train_score+".rank"] = train_index
