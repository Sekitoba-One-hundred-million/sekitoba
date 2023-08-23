from data_manage.storage import Storage
from data_analyze.high_level import HighLevel
from config import name

high_level = HighLevel()

def race_level_check( horce_id, storage: Storage, data ):
    high_level_score = high_level.score_get( storage, horce_id )
    data[horce_id][name.race_level_check+".users"] = high_level_score
    data[horce_id][name.race_level_check+".rank"] = high_level_score
