import sekitoba_library as lib
from sekitoba_data_create.race_type import RaceType
from data_manage.storage import Storage
from config import name

race_type = RaceType()

def straight_slope( horce_id, storage: Storage, data ):
    current_slope = lib.stright_slope( storage.place_num )
    data[horce_id][name.straight_slope] = \
      race_type.stright_slope( None, \
                              storage.past_data[horce_id], \
                              prod_race_rank = lib.money_class_get( storage.race_money ), \
                              prod_current_slope = current_slope )
