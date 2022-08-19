import sekitoba_library as lib
from sekitoba_data_create.race_type import RaceType
from data_manage.storage import Storage
from config import name

race_type = RaceType()

def straight_slope( horce_id, storage: Storage, data, past_race_data ):
    current_slope = lib.stright_slope( storage.place_num )
    race_rank_data = {}
    foot_used_data = {}
    past_cd_list = storage.past_data[horce_id].past_cd_list()

    for past_cd in past_cd_list:
        past_race_id = past_cd.race_id()
        try:
            foot_used_data[past_race_id] = lib.foot_used_create( past_race_data["wrap"][past_race_id] )
            race_rank_data[past_race_id] = lib.money_class_get( past_race_data["race_money"][past_race_id] )
        except:
            continue

    race_type.set_data( race_rank_data, foot_used_data )
    data[horce_id][name.straight_slope] = race_type.stright_slope( None, \
                                                                  storage.past_data[horce_id], \
                                                                  prod_race_rank = lib.money_class_get( storage.race_money ), \
                                                                  prod_current_slope = current_slope )
