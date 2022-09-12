import sekitoba_library as lib
from sekitoba_data_create.race_type import RaceType
from data_analyze import data_create
from data_analyze.common_past_data import CommonPastData
from data_manage.storage import Storage
from config import name

class UsersData:
    def __init__( self ):
        self.data = {}

    def after_users_data_analyze( self, storage: Storage ):
        for horce_id in storage.horce_id_list:
            data_create.weight( horce_id, storage, self.data )
            data_create.popular( horce_id, storage, self.data )
    
    def before_users_data_analyze( self, storage: Storage, common_past_data: CommonPastData ):
        for horce_id in storage.horce_id_list:
            lib.dic_append( self.data, horce_id, {} )
            data_create.before_rank( horce_id, storage, self.data )
            data_create.race_level_check( horce_id, storage, self.data )
            data_create.straight_slope( horce_id, storage, self.data, common_past_data )
            data_create.foot_used( horce_id, storage, self.data, common_past_data )
            data_create.limb( horce_id, storage, self.data )
            data_create.age( horce_id, storage, self.data )
            data_create.speed_index( horce_id, storage, self.data )
            data_create.race_interval( horce_id, storage, self.data )
            data_create.before_id_weight( horce_id, storage, self.data )
            data_create.omega( horce_id, storage, self.data )
            data_create.before_speed( horce_id, storage, self.data )
            data_create.trainer_rank( horce_id, storage, self.data, common_past_data )
            data_create.jockey_rank( horce_id, storage, self.data, common_past_data )
            data_create.before_diff( horce_id, storage, self.data )
            data_create.limb_horce_number( horce_id, storage, self.data )
            data_create.mother_rank( horce_id, storage, self.data )
            data_create.match_rank( horce_id, storage, self.data )
            data_create.weather( horce_id, storage, self.data )
            data_create.burden_weight( horce_id, storage, self.data )
            data_create.before_continue_not_three_rank( horce_id, storage, self.data )
            data_create.horce_sex( horce_id, storage, self.data )
            data_create.horce_sex_month( horce_id, storage, self.data )
            data_create.dist_kind_count( horce_id, storage, self.data )
            data_create.before_popular( horce_id, storage, self.data )
            data_create.before_last_passing_rank( horce_id, storage, self.data )
            data_create.before_first_passing_rank( horce_id, storage, self.data )
            data_create.jockey_year_rank( horce_id, storage, self.data, common_past_data )
            data_create.money( horce_id, storage, self.data )
            data_create.horce_num( horce_id, storage, self.data )
            data_create.baba( horce_id, storage, self.data )
            data_create.place( horce_id, storage, self.data )
            data_create.before_pace( horce_id, storage, self.data, common_past_data )
            data_create.popular_rank( horce_id, storage, self.data )
            data_create.train_score( horce_id, storage, self.data )
            data_create.race_deployment( horce_id, storage, self.data, common_past_data )
            data_create.up3_standard_value( horce_id, storage, self.data )
            data_create.my_limb_count( horce_id, storage, self.data )
            data_create.true_skill( horce_id, storage, self.data, common_past_data )
