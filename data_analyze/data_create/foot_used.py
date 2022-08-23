import sekitoba_library as lib
from data_analyze.common_past_data import CommonPastData
from sekitoba_data_create.race_type import RaceType
from data_manage.storage import Storage
from config import name

race_type = RaceType()

def foot_used( horce_id, storage: Storage, data, common_past_data: CommonPastData ):
    race_rank_data = {}
    foot_used_data = {}
    past_cd_list = storage.past_data[horce_id].past_cd_list()

    for past_cd in past_cd_list:
        past_race_id = past_cd.race_id()
        try:
            foot_used_data[past_race_id] = lib.foot_used_create( common_past_data.wrap[past_race_id] )
            race_rank_data[past_race_id] = lib.money_class_get( common_past_data.race_money[past_race_id] )
        except:
            continue

    race_type.set_data( race_rank_data, foot_used_data )
    data[horce_id][name.foot_used] = race_type.foot_used_score_get( None, \
                                                                   storage.past_data[horce_id], \
                                                                   prod_race_rank = lib.money_class_get( storage.race_money ) )
