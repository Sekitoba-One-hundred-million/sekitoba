import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from sekitoba_data_create.race_type import RaceType
from data_manage.storage import Storage
from config import name

race_type = RaceType()

def race_deployment( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    race_type.set_wrap_data( common_past_data.wrap )
    dep_score = race_type.deploypent( storage.past_data[horce_id] )
    data[horce_id][name.race_deployment+".users"] = dep_score
    data[horce_id][name.race_deployment+".rank"] = dep_score
