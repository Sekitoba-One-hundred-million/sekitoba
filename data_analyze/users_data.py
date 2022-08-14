import sekitoba_library as lib
from sekitoba_data_create.race_type import RaceType

from data_manage.storage import Storage
from config import name
from data_analyze.high_level import HighLevel

high_level = HighLevel()
race_type = RaceType()

class UsersData:
    def __init__( self ):
        self.data = {}

    def division( self, score, d ):
        if score < 0:
            score *= -1
            score /= d
            score *= -1
        else:
            score /= d
            
        return int( score )

    def after_users_data_analyze( self, storage: Storage ):
        def weight( horce_id ):
            try:
                self.data[horce_id][name.weight] = int( storage.data[horce_id]["weight"] / 10 )
            except:
                self.data[horce_id][name.weight] = 0

        def popular( horce_id ):
            try:
                self.data[horce_id][name.popular] = storage.data[horce_id]["popular"]
            except:
                self.data[horce_id][name.popular] = -1

        for horce_id in storage.horce_id_list:
            weight( horce_id )
            popular( horce_id )
    
    def before_users_data_analyze( self, storage: Storage ):
        def before_rank( horce_id ):
            self.data[horce_id][name.before_rank] = 0
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                self.data[horce_id][name.before_rank] = int( before_cd.rank() )

        def race_level_check( horce_id ):
            self.data[horce_id][name.race_level_check] = high_level.score_get( storage, horce_id )

        def straight_slope( horce_id ):
            current_slope = lib.stright_slope( storage.place_num )
            self.data[horce_id][name.straight_slope] = \
            race_type.stright_slope( None, \
                                    storage.past_data[horce_id], \
                                    prod_race_rank = lib.money_class_get( storage.race_money ), \
                                    prod_current_slope = current_slope )

        def limb( horce_id ):
            self.data[horce_id][name.limb] = lib.limb_search( storage.past_data[horce_id] )

        def age( horce_id ):
            current_year = int( storage.race_id[0:4] )
            horce_birth_day = int( horce_id[0:4] )
            self.data[horce_id][name.age] = current_year - horce_birth_day

        def speed_index( horce_id ):
            my_speed_index = 0
            speed_index_list = []

            for diff_horce_id in storage.horce_id_list:
                speed, up_speed, pace_speed = storage.past_data[diff_horce_id].speed_index( storage.data[horce_id]["baba_index"] )
                speed_inedx = lib.max_check( speed ) + lib.max_check( up_speed ) + lib.max_check( pace_speed ) + lib.max_check( storage.data[horce_id]["time_index"] )
                speed_index_list.append( speed_inedx )

                if diff_horce_id == horce_id:
                    my_speed_index = speed_inedx

            speed_index_list = sorted( speed_index_list, reverse = True )
            self.data[horce_id][name.speed_index] = speed_index_list.index( my_speed_index )

        def race_interval( horce_id ):
            ymd = [ storage.today_data.year, storage.today_data.month, storage.today_data.day ]
        
            try:
                self.data[horce_id][name.race_interval] = min( max( storage.past_data[horce_id].race_interval( ymd = ymd ), 0 ), 20 )
            except:
                self.data[horce_id][name.race_interval] = -1

        def before_id_weight( horce_id ):
            self.data[horce_id][name.before_id_weight] = -100
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                self.data[horce_id][name.before_id_weight] = self.division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )

        def omega( horce_id ):
            horce_num = storage.data[horce_id]["horce_num"]
            key_horce_num = str( int( horce_num ) )
            try:
                self.data[horce_id][name.omega] = storage.data["omega"][key_horce_num]
            except:
                self.data[horce_id][name.omega] = -1

        def before_speed( horce_id ):
            self.data[horce_id][name.before_speed] = -1
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                self.data[horce_id][name.before_speed] = int( before_cd.speed() )

        def trainer_rank( horce_id ):
            self.data[horce_id][name.trainer_rank] = -1
            dist = lib.dist_check( storage.dist )
            kind = storage.race_kind
            baba = storage.baba
        
            try:
                trainer_data = storage.data[horce_id]["trainer"]
            except:
                return

            if trainer_data == None:
                return

            rank_data = 0
            count = 0
        
            for day in trainer_data.keys():
                for race_num in trainer_data[day].keys():
                    check_dist, check_kind = lib.dist( trainer_data[day][race_num]["dist"] )
                    check_baba = lib.baba( trainer_data[day][race_num]["baba"] )

                    try:
                        rank = int( trainer_data[day][race_num]["rank"] )
                    except:
                        continue
                
                    if dist == check_dist:
                        rank_data += rank
                        count += 1

                    if baba == check_baba:
                        rank_data += rank
                        count += 1
                    
                    if kind == check_kind:
                        rank_data += rank
                        count += 1

            if not count == 0:
                rank_data /= count

            self.data[horce_id][name.trainer_rank] = rank_data

        def jockey_rank( horce_id ):
            self.data[horce_id][name.jockey_rank] = -1
            dist = lib.dist_check( storage.dist )
            kind = storage.race_kind
            baba = storage.baba
        
            try:
                jockey_data = storage.data[horce_id]["jockey"]
            except:
                return

            rank_data = 0
            count = 0

            if jockey_data == None:
                return

            for day in jockey_data.keys():
                for race_num in jockey_data[day].keys():
                    check_dist, check_kind = lib.dist( jockey_data[day][race_num]["dist"] )
                    check_baba = lib.baba( jockey_data[day][race_num]["baba"] )

                    try:
                        rank = int( jockey_data[day][race_num]["rank"] )
                    except:
                        continue
                
                    if dist == check_dist:
                        rank_data += rank
                        count += 1

                    if baba == check_baba:
                        rank_data += rank
                        count += 1
                    
                    if kind == check_kind:
                        rank_data += rank
                        count += 1

            if not count == 0:
                rank_data /= count

            self.data[horce_id][name.jockey_rank] = rank_data

        def before_diff( horce_id ):
            self.data[horce_id][name.before_diff] = -100
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                self.data[horce_id][name.before_diff] = max( int( before_cd.diff() * 10 ), 0 )

        def limb_horce_number( horce_id ):
            limb_math = lib.limb_search( storage.past_data[horce_id] )
            horce_num = storage.data[horce_id]["horce_num"]
            self.data[horce_id][name.limb_horce_number] = int( limb_math * 100 + int( horce_num / 2 ) )

        def mother_rank( horce_id ):
            mother_id = storage.data[horce_id]["parent_id"]["mother"]
            mother_pd = storage.past_data[mother_id]
            place_num = storage.place_num
            baba_status = storage.baba
            dist_kind = lib.dist_check( storage.dist )
            self.data[horce_id][name.mother_rank] = lib.match_rank_score( mother_pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )

        def match_rank( horce_id ):
            pd = storage.past_data[horce_id]
            place_num = storage.place_num
            baba_status = storage.baba
            dist_kind = lib.dist_check( storage.dist )
            self.data[horce_id][name.match_rank] = lib.match_rank_score( pd, None, place = place_num, baba_status = baba_status, dist_kind = dist_kind )

        def weather( horce_id ):
            self.data[horce_id][name.weather] = storage.weather

        def burden_weight( horce_id ):
            self.data[horce_id][name.burden_weight] = storage.data[horce_id]["burden_weight"]

        def before_continue_not_three_rank( horce_id ):
            self.data[horce_id][name.before_continue_not_three_rank] = storage.past_data[horce_id].before_continue_not_three_rank()

        def horce_sex( horce_id ):
            self.data[horce_id][name.horce_sex] = storage.data[horce_id]["sex"]

        def horce_sex_month( horce_id ):
            month = int( storage.today_data.month )
            horce_sex = storage.data[horce_id]["sex"]
            self.data[horce_id][name.horce_sex_month] = int( month * 10 + horce_sex )

        def dist_kind_count( horce_id ):
            dist_kind = lib.dist_check( storage.dist )
            self.data[horce_id][name.dist_kind_count] = storage.past_data[horce_id].dist_kind_count( dist_kind = dist_kind )

        def before_popular( horce_id ):
            self.data[horce_id][name.before_popular] = -100
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                self.data[horce_id][name.before_popular] = int( before_cd.popular() )

        def before_last_passing_rank( horce_id ):
            self.data[horce_id][name.before_last_passing_rank] = -100
            before_cd = storage.past_data[horce_id].before_cd()

            if not before_cd == None and before_cd.race_check():
                try:
                    self.data[horce_id][name.before_last_passing_rank] = int( before_cd.passing_rank().split( "-" )[-1] )
                except:
                    self.data[horce_id][name.before_last_passing_rank] = 0

        def before_first_passing_rank( horce_id ):
            self.data[horce_id][name.before_first_passing_rank] = -100
            before_cd = storage.past_data[horce_id].before_cd()
            
            if not before_cd == None and before_cd.race_check():
                try:
                    self.data[horce_id][name.before_first_passing_rank] = int( before_cd.passing_rank().split( "-" )[0] )
                except:
                    self.data[horce_id][name.before_first_passing_rank] = 0

        def jockey_year_rank( horce_id ):
            year = int( storage.today_data.year )        
            key_before_year = str( int( year - 1 ) )
        
            try:
                self.data[horce_id][name.jockey_year_rank] = int( storage.data[horce_id]["jockey_year_rank"][key_before_year] / 10 )
            except:
                self.data[horce_id][name.jockey_year_rank] = -1

        def age_dist( horce_id ):
            dist_kind = lib.dist_check( storage.dist )
            age = storage.data[horce_id]["age"]
            self.data[horce_id][name.age_dist] = int( age * 10 + dist_kind )


        for horce_id in storage.horce_id_list:
            lib.dic_append( self.data, horce_id, {} )
            before_rank( horce_id )
            race_level_check( horce_id )
            straight_slope( horce_id )
            #self.foot_used( horce_id )
            limb( horce_id )
            age( horce_id )
            speed_index( horce_id )
            race_interval( horce_id )
            #self.weight( horce_id ) # この段階ではまだ取得できていないので0が代入
            before_id_weight( horce_id )
            omega( horce_id )
            before_speed( horce_id )
            #self.popular( horce_id ) # 後で変更が加えられる数値
            trainer_rank( horce_id )
            jockey_rank( horce_id )
            before_diff( horce_id )
            limb_horce_number( horce_id )
            mother_rank( horce_id )
            match_rank( horce_id )
            weather( horce_id )
            burden_weight( horce_id )
            before_continue_not_three_rank( horce_id )
            horce_sex( horce_id )
            horce_sex_month( horce_id )
            dist_kind_count( horce_id )
            before_popular( horce_id )
            before_last_passing_rank( horce_id )
            before_first_passing_rank( horce_id )
            jockey_year_rank( horce_id )
            age_dist( horce_id )
