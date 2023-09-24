from statistics import stdev

import sekitoba_library as lib
import sekitoba_data_manage as dm

from config import data_name
from config import pickle_name
from config import sekitoba_dir

from data_manage import Storage
from sekitoba_data_create.time_index_get import TimeIndexGet
from sekitoba_data_create.before_race_score_get import BeforeRaceScore
from sekitoba_data_create.train_index_get import TrainIndexGet
from sekitoba_data_create.race_type import RaceType
from sekitoba_data_create.high_level_data_get import RaceHighLevel
from sekitoba_data_create.jockey_data_get import JockeyData
from sekitoba_data_create.trainer_data_get import TrainerData

dm.dl.file_set( pickle_name.horce_data_storage )
dm.dl.file_set( pickle_name.corner_horce_body )
dm.dl.file_set( pickle_name.baba_index_data )
dm.dl.file_set( pickle_name.horce_blood_type_data )
dm.dl.file_set( pickle_name.parent_id_data )
dm.dl.file_set( pickle_name.first_up3_halon )
dm.dl.file_set( pickle_name.corner_true_skill_prod_data )
dm.dl.file_set( pickle_name.true_skill_prod_data )
dm.dl.file_set( pickle_name.first_passing_true_skill_prod_data )
dm.dl.file_set( pickle_name.last_passing_true_skill_prod_data )
dm.dl.file_set( pickle_name.up3_true_skill_prod_data )
dm.dl.file_set( pickle_name.horce_sex_data )
dm.dl.file_set( pickle_name.jockey_judgment_prod_data )
dm.dl.file_set( pickle_name.jockey_judgment_rate_prod_data )
dm.dl.file_set( pickle_name.jockey_judgment_up3_prod_data )
dm.dl.file_set( pickle_name.jockey_judgment_up3_rate_prod_data )
dm.dl.file_set( pickle_name.race_cource_info )
dm.dl.file_set( pickle_name.trainer_judgment_prod_data )
dm.dl.file_set( pickle_name.trainer_judgment_up3_prod_data )
dm.dl.file_set( pickle_name.waku_three_rate_data )
dm.dl.file_set( pickle_name.up3_ave_data )

class DataCreate:
    def __init__( self, storage: Storage ):
        self.storage: Storage = storage
        self.analyze_data = {}
        self.pace_name = "pace"

        self.time_index = TimeIndexGet()
        self.before_race_score = BeforeRaceScore()
        self.train_index = TrainIndexGet()
        self.race_type = RaceType()
        self.race_high_level = RaceHighLevel()
        self.jockey_data = JockeyData()
        self.trainer_data = TrainerData()
        self.train_index.train_time_data.update( { self.storage.today_data.race_id: self.train_data_create() } )
        self.race_type.race_rank_data.update( { self.storage.today_data.race_id: int( lib.money_class_get( self.storage.race_money ) ) } )
        
        self.horce_data_storage = dm.dl.data_get( pickle_name.horce_data_storage )
        self.corner_horce_body = dm.dl.data_get( pickle_name.corner_horce_body )
        self.baba_index_data = dm.dl.data_get( pickle_name.baba_index_data )
        self.horce_blood_type_data = dm.dl.data_get( pickle_name.horce_blood_type_data )
        self.parent_id_data = dm.dl.data_get( pickle_name.parent_id_data )
        self.first_up3_halon = dm.dl.data_get( pickle_name.first_up3_halon )
        self.corner_true_skill_prod_data = dm.dl.data_get( pickle_name.corner_true_skill_prod_data )
        self.true_skill_prod_data = dm.dl.data_get( pickle_name.true_skill_prod_data )
        self.first_passing_true_skill_prod_data = dm.dl.data_get( pickle_name.first_passing_true_skill_prod_data )
        self.last_passing_true_skill_prod_data = dm.dl.data_get( pickle_name.last_passing_true_skill_prod_data )
        self.up3_true_skill_prod_data = dm.dl.data_get( pickle_name.up3_true_skill_prod_data )
        self.horce_sex_data = dm.dl.data_get( pickle_name.horce_sex_data )
        self.jockey_judgment_prod_data = dm.dl.data_get( pickle_name.jockey_judgment_prod_data )
        self.jockey_judgment_rate_prod_data = dm.dl.data_get( pickle_name.jockey_judgment_rate_prod_data )
        self.jockey_judgment_up3_prod_data = dm.dl.data_get( pickle_name.jockey_judgment_up3_prod_data )
        self.jockey_judgment_up3_rate_prod_data = dm.dl.data_get( pickle_name.jockey_judgment_up3_rate_prod_data )
        self.race_cource_info = dm.dl.data_get( pickle_name.race_cource_info )
        self.trainer_judgment_prod_data = dm.dl.data_get( pickle_name.trainer_judgment_prod_data )
        self.trainer_judgment_up3_prod_data = dm.dl.data_get( pickle_name.trainer_judgment_up3_prod_data )
        self.waku_three_rate_data = dm.dl.data_get( pickle_name.waku_three_rate_data )
        self.up3_ave_data = dm.dl.data_get( pickle_name.up3_ave_data )

        self.waku_three_key_list = [ "place", "dist", "limb", "baba", "kind" ]
        self.score_key_list = []
        self.score_key_get()

    def score_key_get( self ):
        f = open( sekitoba_dir + "/data/score_data_name.txt" )
        all_data = f.readlines()

        for str_data in all_data:
            self.score_key_list.append( lib.text_replace( str_data ) )

    def train_data_create( self ):
        result = {}

        for key_horce_num in self.storage.train_data.keys():
            result[key_horce_num] = {}
            result[key_horce_num]["load"] = self.storage.train_data[key_horce_num].load
            result[key_horce_num]["cource"] = self.storage.train_data[key_horce_num].cource
            result[key_horce_num]["time"] = self.storage.train_data[key_horce_num].time
            result[key_horce_num]["wrap"] = self.storage.train_data[key_horce_num].wrap

        return result

    def current_data_create( self, horce_id ):
        current_race_data = [ None ] * 22
        current_race_data[0] = lib.padding_str_math( str( self.storage.today_data.year ) ) + "/" + \
          lib.padding_str_math( str( self.storage.today_data.race_date.month ) ) + "/" + \
          lib.padding_str_math( str( self.storage.today_data.race_date.day ) )
        current_race_data[1] = str( self.storage.today_data.num ) + \
          self.storage.today_data.place + \
          str( self.storage.today_data.day )
        current_race_data[2] = self.storage.weather
        current_race_data[3] = str( self.storage.today_data.race_num )
        current_race_data[4] = ""
        current_race_data[5] = str( self.storage.all_horce_num )
        current_race_data[6] = str( self.storage.current_horce_data[horce_id].waku_num )
        current_race_data[7] = str( self.storage.current_horce_data[horce_id].horce_num )
        current_race_data[8] = str( self.storage.current_horce_data[horce_id].odds )
        current_race_data[9] = str( self.storage.current_horce_data[horce_id].popular )
        current_race_data[10] = ''
        current_race_data[11] = ''
        current_race_data[12] = str( int( lib.math_check( self.storage.current_horce_data[horce_id].burden_weight ) ) )
        current_race_data[13] = self.storage.dist
        current_race_data[14] = self.storage.baba
        current_race_data[15] = ''
        current_race_data[16] = ''
        current_race_data[17] = ''
        current_race_data[18] = ''
        current_race_data[19] = ''
        current_race_data[20] = self.storage.current_horce_data[horce_id].weight
        current_race_data[21] = ''
        
        return current_race_data

    def match_rank_score( self, cd: lib.current_data, target_id ):
        target_data = []

        if target_id in self.horce_data_storage:
            target_data = self.horce_data_storage[target_id]
                
        target_pd = lib.past_data( target_data, [] )
        count = 0
        score = 0
            
        for target_cd in target_pd.past_cd_list():
            c = 0
                
            if target_cd.place() == cd.place():
                c += 1
                
            if target_cd.baba_status() == cd.baba_status():
                c += 1

            if lib.dist_check( target_cd.dist() * 1000 ) == lib.dist_check( cd.dist() * 1000 ):
                c += 1

            count += c
            score += target_cd.rank() * c

        if not count == 0:
            score /= count
                
        return int( score )

    def division( self, score, d ):
        if score < 0:
            score *= -1
            score /= d
            score *= -1
        else:
            score /= d

        return int( score )
    
    def create( self ):
        race_id = self.storage.today_data.race_id
        str_year = str( self.storage.today_data.year )
        str_day = str( self.storage.today_data.day )
        str_num = str( self.storage.today_data.num )
        str_place_num = str( self.storage.today_data.place_num )
        key_money_class = str( int( lib.money_class_get( self.storage.race_money ) ) )
        ymd = { "y": self.storage.today_data.year, \
               "m": self.storage.today_data.race_date.month, \
               "d": self.storage.today_data.race_date.day }

        current_race_data = {}
        for score_key in self.score_key_list:
            current_race_data[score_key] = []

        my_limb_count = {}
        one_popular_limb = 0
        one_popular_odds = 0
        two_popular_odds = 0
        two_popular_limb = 0
        three_popular_limb = 0
        escape_limb1_count = 0
        escape_limb2_count = 0
        escape_limb_count = 0
        insert_limb_count = 0
        horce_id_list = []
        
        for horce_id in self.storage.horce_id_list:
            if horce_id in self.storage.cansel_horce_id_list:
                continue
            
            if not horce_id in self.horce_data_storage:
                continue
            
            past_data = self.horce_data_storage[horce_id]

            try:
                current_data = self.current_data_create( horce_id )
            except:
                continue
            
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
            jockey_id = self.storage.current_horce_data[horce_id].jockey_id
            trainer_id = self.storage.current_horce_data[horce_id].trainer_id
            horce_num = cd.horce_number()
            popular = cd.popular()
            odds = cd.odds()
            limb_math = lib.limb_search( pd )
            escape_within_rank = -1
            
            if limb_math == 1:
                escape_limb1_count += 1
            elif limb_math == 2:
                escape_limb2_count += 1
            
            if limb_math == 1 or limb_math == 2:
                escape_limb_count += 1
                escape_within_rank = horce_num
            elif limb_math == 3 or limb_math == 4:
                insert_limb_count += 1

            lib.dic_append( my_limb_count, limb_math, 0 )
            my_limb_count[limb_math] += 1

            if popular == 1:
                one_popular_odds = odds
                one_popular_limb = limb_math
            elif popular == 2:
                two_popular_odds = odds
                two_popular_limb = limb_math
            elif popular == 3:
                three_popular_limb = limb_math
            
            past_min_first_horce_body = 1000
            past_min_last_horce_body = 1000
            past_max_first_horce_body = 1000
            past_max_last_horce_body = 1000
            past_ave_first_horce_body = 1000
            past_ave_last_horce_body = 1000
            past_std_first_horce_body = 1000
            past_std_last_horce_body = 1000
            past_first_horce_body_list = []
            past_last_horce_body_list = []

            for past_cd in  pd.past_cd_list():
                past_race_id = past_cd.race_id()
                past_key_horce_num = str( int( past_cd.horce_number() ) )

                if past_race_id in self.corner_horce_body:
                    past_min_corner_key = min( self.corner_horce_body[past_race_id] )
                    past_max_corner_key = max( self.corner_horce_body[past_race_id] )
                    
                    if past_key_horce_num in self.corner_horce_body[past_race_id][past_min_corner_key]:
                        past_first_horce_body_list.append( self.corner_horce_body[past_race_id][past_min_corner_key][past_key_horce_num] )
                        past_last_horce_body_list.append( self.corner_horce_body[past_race_id][past_max_corner_key][past_key_horce_num] )

            if not len( past_first_horce_body_list ) == 0:
                past_min_first_horce_body = min( past_first_horce_body_list )
                past_min_last_horce_body = min( past_last_horce_body_list )
                past_max_first_horce_body = max( past_first_horce_body_list )
                past_max_last_horce_body = max( past_last_horce_body_list )
                past_ave_first_horce_body = sum( past_first_horce_body_list ) / len( past_first_horce_body_list )
                past_ave_last_horce_body = sum( past_last_horce_body_list ) / len( past_last_horce_body_list )

                if len( past_first_horce_body_list ) > 1:
                    past_std_first_horce_body = stdev( past_first_horce_body_list )
                    past_std_last_horce_body = stdev( past_last_horce_body_list )

            horce_true_skill = 25
            jockey_true_skill = 25
            trainer_true_skill = 25
            horce_first_passing_true_skill = 25
            jockey_first_passing_true_skill = 25
            trainer_first_passing_true_skill = 25
            horce_last_passing_true_skill = 25
            jockey_last_passing_true_skill = 25
            corner_true_skill = 25
            up3_horce_true_skill = 25
            up3_jockey_true_skill = 25
            up3_trainer_true_skill = 25

            if horce_id in self.first_passing_true_skill_prod_data["horce"]:
                horce_first_passing_true_skill = self.first_passing_true_skill_prod_data["horce"][horce_id]

            if jockey_id in self.first_passing_true_skill_prod_data["jockey"]:
                jockey_first_passing_true_skill = self.first_passing_true_skill_prod_data["jockey"][jockey_id]
                
            if trainer_id in self.first_passing_true_skill_prod_data["trainer"]:
                trainer_first_passing_true_skill = self.first_passing_true_skill_prod_data["trainer"][trainer_id]

            if horce_id in self.true_skill_prod_data["horce"]:
                horce_true_skill = self.true_skill_prod_data["horce"][horce_id]

            if jockey_id in self.true_skill_prod_data["jockey"]:
                jockey_true_skill = self.true_skill_prod_data["jockey"][jockey_id]
                
            if trainer_id in self.true_skill_prod_data["trainer"]:
                trainer_true_skill = self.true_skill_prod_data["trainer"][trainer_id]

            if horce_id in self.last_passing_true_skill_prod_data["horce"]:
                horce_last_passing_true_skill = self.last_passing_true_skill_prod_data["horce"][horce_id]

            if jockey_id in self.last_passing_true_skill_prod_data["jockey"]:
                jockey_last_passing_true_skill = self.last_passing_true_skill_prod_data["jockey"][jockey_id]

            if horce_id in self.up3_true_skill_prod_data["horce"]:
                up3_horce_true_skill = self.up3_true_skill_prod_data["horce"][horce_id]

            if jockey_id in self.up3_true_skill_prod_data["jockey"]:
                up3_jockey_true_skill = self.up3_true_skill_prod_data["jockey"][jockey_id]
                
            if trainer_id in self.up3_true_skill_prod_data["trainer"]:
                up3_trainer_true_skill = self.up3_true_skill_prod_data["trainer"][trainer_id]

            if horce_id in self.corner_true_skill_prod_data["horce"]:
                corner_true_skill = self.corner_true_skill_prod_data["horce"][horce_id]

            speed = []
            current_time_index = self.time_index.main( horce_id, pd.past_day_list() )

            if horce_id in self.baba_index_data:
                speed, _, _ = pd.speed_index( self.baba_index_data[horce_id] )

            first_up3_halon_ave = -1
            first_up3_halon_min = -1

            if race_id in self.first_up3_halon and \
              horce_num in self.first_up3_halon[race_id] and \
              not len( self.first_up3_halon[race_id][horce_num] ) == 0:
                first_up3_halon_ave = sum( self.first_up3_halon[race_id][horce_num] ) / len( self.first_up3_halon[race_id][horce_num] )
                first_up3_halon_min = min( self.first_up3_halon[race_id][horce_num] )

            first_wrap = self.train_index.first_wrap( race_id, horce_num )
            final_wrap = self.train_index.final_wrap( race_id, cd.horce_number() )
            train_time_slope, train_time_slice = self.train_index.train_time_slope_slice( race_id, horce_num )
            wrap_slope, wrap_slice = self.train_index.wrap_slope_slice( race_id, horce_num )
            wrap_diff = first_wrap - final_wrap

            judgement_key_data = {}
            judgement_key_data["limb"] = str( int( limb_math ) )
            judgement_key_data["popular"] = str( int( cd.popular() ) )
            judgement_key_data["flame_num"] = str( int( cd.flame_number() ) )
            judgement_key_data["dist"] = str( int( cd.dist_kind() ) )
            judgement_key_data["kind"] = str( int( cd.race_kind() ) )
            judgement_key_data["baba"] = str( int( cd.baba_status() ) )
            judgement_key_data["place"] = str( int( cd.place()) )
            judgement_rate_key_list = [ "0", "1", "2" ]

            for judgement_key in judgement_key_data:
                try:
                    current_race_data["jockey_judgment_{}".format( judgement_key )].append( \
                        self.jockey_judgment_prod_data[jockey_id][judgement_key][judgement_key_data[judgement_key]] )
                except:
                    current_race_data["jockey_judgment_{}".format( judgement_key )].append( self.storage.all_horce_num / 2 )

                try:
                    current_race_data["jockey_judgment_up3_{}".format( judgement_key )].append( \
                        self.jockey_judgment_up3_prod_data[jockey_id][judgement_key][judgement_key_data[judgement_key]] )
                except:
                    current_race_data["jockey_judgment_up3_{}".format( judgement_key )].append( 0 )

                try:
                    current_race_data["trainer_judgment_{}".format( judgement_key )].append( \
                        self.trainer_judgment_prod_data[trainer_id][judgement_key][judgement_key_data[judgement_key]] )
                except:
                    current_race_data["trainer_judgment_{}".format( judgement_key )].append( self.storage.all_horce_num / 2 )

                try:
                    current_race_data["trainer_judgment_up3_{}".format( judgement_key )].append( \
                        self.trainer_judgment_up3_prod_data[trainer_id][judgement_key][judgement_key_data[judgement_key]] )
                except:
                    current_race_data["trainer_judgment_up3_{}".format( judgement_key )].append( 0 )

            for judgement_key in judgement_key_data:
                for rk in judgement_rate_key_list:
                    try:
                        current_race_data["jockey_judgment_rate_{}_{}".format( judgement_key, rk  )].append( \
                            self.jockey_judgment_rate_prod_data[jockey_id][judgement_key][judgement_key_data[judgement_key]][rk] )
                    except:
                        current_race_data["jockey_judgment_rate_{}_{}".format( judgement_key,rk )].append( 0 )

                    try:
                        current_race_data["jockey_judgment_up3_rate_{}_{}".format( judgement_key, rk  )].append( \
                            self.jockey_judgment_up3_rate_prod_data[jockey_id][judgement_key][judgement_key_data[judgement_key]][rk] )
                    except:
                        current_race_data["jockey_judgment_up3_rate_{}_{}".format( judgement_key,rk )].append( 0 )

            current_race_data[data_name.burden_weight].append( cd.burden_weight() )
            current_race_data[data_name.escape_within_rank].append( escape_within_rank )
            current_race_data[data_name.past_ave_first_horce_body].append( past_ave_first_horce_body )
            current_race_data[data_name.past_ave_last_horce_body].append( past_ave_last_horce_body )
            current_race_data[data_name.past_max_first_horce_body].append( past_max_first_horce_body )
            current_race_data[data_name.past_max_last_horce_body].append( past_max_last_horce_body )
            current_race_data[data_name.past_min_first_horce_body].append( past_min_first_horce_body )
            current_race_data[data_name.past_min_last_horce_body].append( past_min_last_horce_body )
            current_race_data[data_name.past_std_first_horce_body].append( past_std_first_horce_body )
            current_race_data[data_name.past_std_last_horce_body].append( past_std_last_horce_body )
            current_race_data[data_name.horce_first_passing_true_skill].append( horce_first_passing_true_skill )
            current_race_data[data_name.jockey_first_passing_true_skill].append( jockey_first_passing_true_skill )
            current_race_data[data_name.trainer_first_passing_true_skill].append( trainer_first_passing_true_skill )
            current_race_data[data_name.horce_true_skill].append( horce_true_skill )
            current_race_data[data_name.jockey_true_skill].append( jockey_true_skill )
            current_race_data[data_name.trainer_true_skill].append( trainer_true_skill )
            current_race_data[data_name.jockey_last_passing_true_skill].append( jockey_last_passing_true_skill )
            current_race_data[data_name.horce_last_passing_true_skill].append( horce_last_passing_true_skill )
            current_race_data[data_name.up3_horce_true_skill].append( up3_horce_true_skill )
            current_race_data[data_name.up3_jockey_true_skill].append( up3_jockey_true_skill )
            current_race_data[data_name.up3_trainer_true_skill].append( up3_trainer_true_skill )
            current_race_data[data_name.speed_index].append( lib.max_check( speed ) + current_time_index["max"] )
            current_race_data[data_name.up_rate].append( pd.up_rate( key_money_class ) )
            current_race_data[data_name.corner_diff_rank_ave].append( pd.corner_diff_rank() )
            current_race_data[data_name.corner_true_skill].append( corner_true_skill )
            current_race_data[data_name.first_up3_halon_ave].append( first_up3_halon_ave )
            current_race_data[data_name.first_up3_halon_min].append( first_up3_halon_min )
            current_race_data[data_name.final_wrap].append( final_wrap )
            current_race_data[data_name.first_wrap].append( first_wrap )
            current_race_data[data_name.train_time_rate].append( self.train_index.train_time_rate( race_id, horce_num ) )
            current_race_data[data_name.train_time_slope].append( train_time_slope )
            current_race_data[data_name.train_time_slice].append( train_time_slice )
            current_race_data[data_name.wrap_diff].append( wrap_diff )
            current_race_data[data_name.wrap_rate].append( self.train_index.wrap_rate( race_id, horce_num ) )
            current_race_data[data_name.wrap_slice].append( wrap_slice )
            current_race_data[data_name.wrap_slope].append( wrap_slope )
            current_race_data[data_name.wrap_std].append( self.train_index.wrap_std( race_id, horce_num ) )
            current_race_data[data_name.foot_used].append( self.race_type.foot_used_score_get( cd, pd ) )
            current_race_data[data_name.level_score].append( pd.level_score() )
            current_race_data[data_name.match_rank].append( pd.match_rank() )
            current_race_data[data_name.match_up3].append( pd.match_up3() )
            horce_id_list.append( horce_id )

        N = len( horce_id_list )

        if N == 0:
            return False

        ave_burden_weight = sum( current_race_data[data_name.burden_weight] ) / N
        ave_past_ave_first_horce_body = sum( current_race_data[data_name.past_ave_first_horce_body] ) / N
        ave_past_ave_last_horce_body = sum( current_race_data[data_name.past_ave_last_horce_body] ) / N
        ave_past_max_first_horce_body = sum( current_race_data[data_name.past_max_first_horce_body] ) / N
        ave_past_max_last_horce_body = sum( current_race_data[data_name.past_max_last_horce_body] ) / N
        ave_past_min_first_horce_body = sum( current_race_data[data_name.past_min_first_horce_body] ) / N
        ave_past_min_last_horce_body = sum( current_race_data[data_name.past_min_last_horce_body] ) / N
        ave_race_horce_first_passing_true_skill = sum( current_race_data[data_name.horce_first_passing_true_skill] ) / N
        ave_race_jockey_first_passing_true_skill = sum( current_race_data[data_name.jockey_first_passing_true_skill] ) / N
        ave_race_trainer_first_passing_true_skill = sum( current_race_data[data_name.trainer_first_passing_true_skill] ) / N
        ave_race_horce_true_skill = sum( current_race_data[data_name.horce_true_skill] ) / N
        ave_race_jockey_true_skill = sum( current_race_data[data_name.jockey_true_skill] ) / N
        ave_race_trainer_true_skill = sum( current_race_data[data_name.trainer_true_skill] ) / N
        ave_up_rate = sum( current_race_data[data_name.up_rate] ) / N        
        ave_speed_index = sum( current_race_data[data_name.speed_index] ) / N
        corner_diff_rank_ave_index = sorted( current_race_data[data_name.corner_diff_rank_ave], reverse = True )
        corner_true_skill_index = sorted( current_race_data[data_name.corner_true_skill], reverse = True )
        escape_within_rank_index = sorted( current_race_data[data_name.escape_within_rank], reverse = True )
        foot_used_index = sorted( current_race_data[data_name.foot_used], reverse = True )
        horce_first_passing_true_skill_index = sorted( current_race_data[data_name.horce_first_passing_true_skill], reverse = True )
        horce_last_passing_true_skill_index = sorted( current_race_data[data_name.horce_last_passing_true_skill], reverse = True )
        jockey_last_passing_true_skill_index = sorted( current_race_data[data_name.jockey_last_passing_true_skill], reverse = True )
        horce_true_skill_index = sorted( current_race_data[data_name.horce_true_skill], reverse = True )
        jockey_first_passing_true_skill_index = sorted( current_race_data[data_name.jockey_first_passing_true_skill], reverse = True )
        jockey_true_skill_index = sorted( current_race_data[data_name.jockey_true_skill], reverse = True )
        jockey_judgment_baba_index = sorted( current_race_data[data_name.jockey_judgment_baba], reverse = True )
        jockey_judgment_dist_index = sorted( current_race_data[data_name.jockey_judgment_dist], reverse = True )
        jockey_judgment_flame_num_index = sorted( current_race_data[data_name.jockey_judgment_flame_num], reverse = True )
        jockey_judgment_kind_index = sorted( current_race_data[data_name.jockey_judgment_kind], reverse = True )
        jockey_judgment_limb_index = sorted( current_race_data[data_name.jockey_judgment_limb], reverse = True )
        jockey_judgment_place_index = sorted( current_race_data[data_name.jockey_judgment_place], reverse = True )
        jockey_judgment_popular_index = sorted( current_race_data[data_name.jockey_judgment_popular], reverse = True )
        level_score_index = sorted( current_race_data[data_name.level_score], reverse = True )
        match_rank_index = sorted( current_race_data[data_name.match_rank], reverse = True )
        match_up3_index = sorted( current_race_data[data_name.match_up3], reverse = True )
        past_ave_first_horce_body_index = sorted( current_race_data[data_name.past_ave_first_horce_body], reverse = True )
        past_ave_last_horce_body_index = sorted( current_race_data[data_name.past_ave_last_horce_body], reverse = True )
        past_min_first_horce_body_index = sorted( current_race_data[data_name.past_min_first_horce_body], reverse = True )
        past_min_last_horce_body_index = sorted( current_race_data[data_name.past_min_last_horce_body], reverse = True )
        speed_index_index = sorted( current_race_data[data_name.speed_index], reverse = True )
        trainer_first_passing_true_skill_index = sorted( current_race_data[data_name.trainer_first_passing_true_skill], reverse =  True )
        trainer_true_skill_index = sorted( current_race_data[data_name.trainer_true_skill], reverse = True )
        up3_horce_true_skill_index = sorted( current_race_data[data_name.up3_horce_true_skill], reverse = True )
        up3_jockey_true_skill_index = sorted( current_race_data[data_name.up3_jockey_true_skill], reverse = True )
        up3_trainer_true_skill_index = sorted( current_race_data[data_name.up3_trainer_true_skill], reverse = True )
        up_rate_index = sorted( current_race_data[data_name.up_rate], reverse = True )
        
        corner_diff_rank_ave_stand = lib.standardization( current_race_data[data_name.corner_diff_rank_ave] )
        corner_true_skill_stand = lib.standardization( current_race_data[data_name.corner_true_skill] )
        first_up3_halon_ave_stand = lib.standardization( current_race_data[data_name.first_up3_halon_ave] )
        first_up3_halon_min_stand = lib.standardization( current_race_data[data_name.first_up3_halon_min] )
        first_wrap_stand = lib.standardization( current_race_data[data_name.first_wrap] )
        final_wrap_stand = lib.standardization( current_race_data[data_name.final_wrap] )
        train_time_rate_stand = lib.standardization( current_race_data[data_name.train_time_rate] )
        train_time_slice_stand = lib.standardization( current_race_data[data_name.train_time_slice] )
        train_time_slope_stand = lib.standardization( current_race_data[data_name.train_time_slope] )
        wrap_diff_stand = lib.standardization( current_race_data[data_name.wrap_diff] )
        wrap_rate_stand = lib.standardization( current_race_data[data_name.wrap_rate] )
        wrap_slice_stand = lib.standardization( current_race_data[data_name.wrap_slice] )
        wrap_slope_stand = lib.standardization( current_race_data[data_name.wrap_slope] )
        wrap_std_stand = lib.standardization( current_race_data[data_name.wrap_std] )
        foot_used_stand = lib.standardization( current_race_data[data_name.foot_used] )
        horce_first_passing_true_skill_stand = lib.standardization( current_race_data[data_name.horce_first_passing_true_skill] )
        horce_true_skill_stand = lib.standardization( current_race_data[data_name.horce_true_skill] )
        jockey_first_passing_true_skill_stand = lib.standardization( current_race_data[data_name.jockey_first_passing_true_skill] )
        jockey_true_skill_stand = lib.standardization( current_race_data[data_name.jockey_true_skill] )
        jockey_judgment_baba_stand = lib.standardization( current_race_data[data_name.jockey_judgment_baba] )
        jockey_judgment_dist_stand = lib.standardization( current_race_data[data_name.jockey_judgment_dist] )
        jockey_judgment_flame_num_stand = lib.standardization( current_race_data[data_name.jockey_judgment_flame_num] )
        jockey_judgment_kind_stand = lib.standardization( current_race_data[data_name.jockey_judgment_kind] )
        jockey_judgment_limb_stand = lib.standardization( current_race_data[data_name.jockey_judgment_limb] )
        jockey_judgment_place_stand = lib.standardization( current_race_data[data_name.jockey_judgment_place] )
        jockey_judgment_popular_stand = lib.standardization( current_race_data[data_name.jockey_judgment_popular] )
        jockey_judgment_up3_baba_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_baba] )
        jockey_judgment_up3_dist_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_dist] )
        jockey_judgment_up3_flame_num_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_flame_num] )
        jockey_judgment_up3_kind_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_kind] )
        jockey_judgment_up3_limb_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_limb] )
        jockey_judgment_up3_place_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_place] )
        jockey_judgment_up3_popular_stand = lib.standardization( current_race_data[data_name.jockey_judgment_up3_popular] )
        level_score_stand = lib.standardization( current_race_data[data_name.level_score] )
        match_rank_stand = lib.standardization( current_race_data[data_name.match_rank] )
        match_up3_stand = lib.standardization( current_race_data[data_name.match_up3] )
        past_ave_first_horce_body_stand = lib.standardization( current_race_data[data_name.past_ave_first_horce_body] )
        past_ave_last_horce_body_stand = lib.standardization( current_race_data[data_name.past_ave_last_horce_body] )
        past_max_first_horce_body_stand = lib.standardization( current_race_data[data_name.past_max_first_horce_body] )
        past_max_last_horce_body_stand = lib.standardization( current_race_data[data_name.past_max_last_horce_body] )
        past_min_first_horce_body_stand = lib.standardization( current_race_data[data_name.past_min_first_horce_body] )
        past_min_last_horce_body_stand = lib.standardization( current_race_data[data_name.past_min_last_horce_body] )
        speed_index_stand = lib.standardization( current_race_data[data_name.speed_index] )
        trainer_first_passing_true_skill_stand = lib.standardization( current_race_data[data_name.trainer_first_passing_true_skill] )
        trainer_true_skill_stand = lib.standardization( current_race_data[data_name.trainer_true_skill] )
        up3_horce_true_skill_stand = lib.standardization( current_race_data[data_name.up3_horce_true_skill] )
        up3_jockey_true_skill_stand = lib.standardization( current_race_data[data_name.up3_jockey_true_skill] )
        up3_trainer_true_skill_stand = lib.standardization( current_race_data[data_name.up3_trainer_true_skill] )
        up_rate_stand = lib.standardization( current_race_data[data_name.up_rate] )

        max_past_ave_first_horce_body = max( current_race_data[data_name.past_ave_first_horce_body] )
        max_past_ave_last_horce_body = max( current_race_data[data_name.past_ave_last_horce_body] )
        max_past_max_first_horce_body = max( current_race_data[data_name.past_max_first_horce_body] )
        max_past_max_last_horce_body = max( current_race_data[data_name.past_max_last_horce_body] )
        max_past_min_first_horce_body = max( current_race_data[data_name.past_min_first_horce_body] )
        max_past_min_last_horce_body = max( current_race_data[data_name.past_min_last_horce_body] )
        max_race_horce_true_skill = max( current_race_data[data_name.horce_true_skill] )
        max_race_jockey_true_skill = max( current_race_data[data_name.jockey_true_skill] )
        max_race_trainer_true_skill = max( current_race_data[data_name.trainer_true_skill] )
        max_race_horce_first_passing_true_skill = max( current_race_data[data_name.horce_first_passing_true_skill] )
        max_race_jockey_first_passing_true_skill = max( current_race_data[data_name.jockey_first_passing_true_skill] )
        max_race_trainer_first_passing_true_skill = max( current_race_data[data_name.trainer_first_passing_true_skill] )
        max_speed_index = max( current_race_data[data_name.speed_index] )
        max_up_rate = max( current_race_data[data_name.up_rate] )

        min_past_ave_first_horce_body = min( current_race_data[data_name.past_ave_first_horce_body] )
        min_past_ave_last_horce_body = min( current_race_data[data_name.past_ave_last_horce_body] )
        min_past_max_first_horce_body = min( current_race_data[data_name.past_max_first_horce_body] )
        min_past_max_last_horce_body = min( current_race_data[data_name.past_max_last_horce_body] )
        min_past_min_first_horce_body = min( current_race_data[data_name.past_min_first_horce_body] )
        min_past_min_last_horce_body = min( current_race_data[data_name.past_min_last_horce_body] )
        min_race_horce_true_skill = min( current_race_data[data_name.horce_true_skill] )
        min_race_jockey_true_skill = min( current_race_data[data_name.jockey_true_skill] )
        min_race_trainer_true_skill = min( current_race_data[data_name.trainer_true_skill] )
        min_race_horce_first_passing_true_skill = min( current_race_data[data_name.horce_first_passing_true_skill] )
        min_race_jockey_first_passing_true_skill = min( current_race_data[data_name.jockey_first_passing_true_skill] )
        min_race_trainer_first_passing_true_skill = min( current_race_data[data_name.trainer_first_passing_true_skill] )
        min_speed_index = min( current_race_data[data_name.speed_index] )
        min_up_rate = min( current_race_data[data_name.up_rate] )

        std_past_ave_first_horce_body = stdev( current_race_data[data_name.past_ave_first_horce_body] )
        std_past_ave_last_horce_body = stdev( current_race_data[data_name.past_ave_last_horce_body] )
        std_past_max_first_horce_body = stdev( current_race_data[data_name.past_max_first_horce_body] )
        std_past_max_last_horce_body = stdev( current_race_data[data_name.past_max_last_horce_body] )
        std_past_min_first_horce_body = stdev( current_race_data[data_name.past_min_first_horce_body] )
        std_past_min_last_horce_body = stdev( current_race_data[data_name.past_min_last_horce_body] )
        std_race_horce_true_skill = stdev( current_race_data[data_name.horce_true_skill] )
        std_race_jockey_true_skill = stdev( current_race_data[data_name.jockey_true_skill] )
        std_race_trainer_true_skill = stdev( current_race_data[data_name.trainer_true_skill] )
        std_race_horce_first_passing_true_skill = stdev( current_race_data[data_name.horce_first_passing_true_skill] )
        std_race_jockey_first_passing_true_skill = stdev( current_race_data[data_name.jockey_first_passing_true_skill] )
        std_race_trainer_first_passing_true_skill = stdev( current_race_data[data_name.trainer_first_passing_true_skill] )        
        std_speed_index = stdev( current_race_data[data_name.speed_index] )
        std_up_rate = stdev( current_race_data[data_name.up_rate] )

        self.analyze_data[self.pace_name] = {}
        self.analyze_data[self.pace_name][data_name.ave_burden_weight_diff] = ave_burden_weight
        self.analyze_data[self.pace_name][data_name.ave_race_horce_true_skill] = ave_race_horce_true_skill
        self.analyze_data[self.pace_name][data_name.ave_race_jockey_true_skill] = ave_race_jockey_true_skill
        self.analyze_data[self.pace_name][data_name.ave_race_trainer_true_skill] = ave_race_trainer_true_skill
        self.analyze_data[self.pace_name][data_name.ave_race_horce_first_passing_true_skill] = \
          ave_race_horce_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.ave_race_jockey_first_passing_true_skill] = \
          ave_race_jockey_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.ave_race_trainer_first_passing_true_skill] = \
          ave_race_trainer_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.ave_up_rate] = ave_up_rate
        self.analyze_data[self.pace_name][data_name.ave_speed_index] = ave_speed_index
        self.analyze_data[self.pace_name][data_name.max_race_horce_true_skill] = max_race_horce_true_skill
        self.analyze_data[self.pace_name][data_name.max_race_jockey_true_skill] = max_race_jockey_true_skill
        self.analyze_data[self.pace_name][data_name.max_race_trainer_true_skill] = max_race_trainer_true_skill
        self.analyze_data[self.pace_name][data_name.max_race_horce_first_passing_true_skill] = \
          max_race_horce_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.max_race_jockey_first_passing_true_skill] = \
          max_race_jockey_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.max_race_trainer_first_passing_true_skill] = \
          max_race_trainer_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.max_up_rate] = max_up_rate
        self.analyze_data[self.pace_name][data_name.max_speed_index] = max_speed_index
        self.analyze_data[self.pace_name][data_name.min_race_horce_true_skill] = min_race_horce_true_skill
        self.analyze_data[self.pace_name][data_name.min_race_jockey_true_skill] = min_race_jockey_true_skill
        self.analyze_data[self.pace_name][data_name.min_race_trainer_true_skill] = min_race_trainer_true_skill
        self.analyze_data[self.pace_name][data_name.min_race_horce_first_passing_true_skill] = \
          min_race_horce_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.min_race_jockey_first_passing_true_skill] = \
          min_race_jockey_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.min_race_trainer_first_passing_true_skill] = \
          min_race_trainer_first_passing_true_skill
        self.analyze_data[self.pace_name][data_name.min_up_rate] = min_up_rate
        self.analyze_data[self.pace_name][data_name.min_speed_index] = min_speed_index

        for i, horce_id in enumerate( horce_id_list ):
            if horce_id in self.storage.cansel_horce_id_list:
                continue

            if not horce_id in self.horce_data_storage:
                continue

            past_data = self.horce_data_storage[horce_id]

            try:
                current_data = self.current_data_create( horce_id )
            except:
                continue
            
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
            before_cd = pd.before_cd()

            if before_cd == None:
                before_diff = -1000
                before_first_last_diff = -1000
                before_id_weight = -1000
                before_popular = -1000
                before_race_score = -1000
                before_rank = -1000
                before_speed = -1000
                popular_rank = -1000
                diff_load_weight = -1000
                before_first_passing_rank = -1000
                before_last_passing_rank = -1000
                up3_standard_value = -1000
                self.storage.skip_horce_id_list.append( horce_id )
            else:
                before_diff = max( before_cd.diff(), 0 ) * 10
                before_first_last_diff = before_cd.first_last_diff()
                before_id_weight = self.division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )
                before_popular = before_cd.popular()
                before_race_score = self.before_race_score.score_get( before_cd, limb_math, horce_id )
                before_rank = before_cd.rank()
                before_speed = before_cd.speed()
                popular_rank = abs( before_cd.rank() - before_cd.popular() )
                diff_load_weight = cd.burden_weight() - before_cd.burden_weight()
                p1, p2 = before_cd.pace()
                up3 = before_cd.up_time()
                up3_standard_value = max( min( ( up3 - p2 ) * 5, 15 ), -10 )
                before_passing_list = before_cd.passing_rank().split( "-" )

                try:
                    before_first_passing_rank = int( before_passing_list[0] )
                except:
                    before_first_passing_rank = 0

                try:
                    before_last_passing_rank = int( before_passing_list[-1] )
                except:
                    before_last_passing_rank = 0


            limb_math = lib.limb_search( pd )
            horce_num = cd.horce_number()
            key_horce_num = str( int( horce_num ) )
            key_before_year = str( int( int( str_year ) - 1 ) )
            key_place = str( int( cd.place()) )
            key_dist = str( int( cd.dist() * 1000 ) )
            key_dist_kind = str( int( cd.dist_kind() ) )
            key_kind = str( int( cd.race_kind() ) )
            key_baba = str( int( cd.baba_status() ) )
            key_limb = str( int( limb_math ) )

            father_blood_type = 0
            father_id = ""
            mother_id = ""
            horce_sex = -1
            horce_sex_month = -1
            race_info = { "dist": int( cd.dist() * 1000 ), "baba": int( cd.baba_status()), "kind": int( cd.race_kind() ) }
            kind_key_data = {}
            kind_key_data["place"] = key_place
            kind_key_data["dist"] = key_dist
            kind_key_data["baba"] = key_baba
            kind_key_data["kind"] = key_kind
            kind_key_data["limb"] = key_limb

            waku = -1

            if cd.horce_number() < cd.all_horce_num() / 2:
                waku = 1
            else:
                waku = 2

            if horce_id in self.horce_sex_data:
                horce_sex = self.horce_sex_data[horce_id]
                horce_sex_month = int( self.storage.today_data.race_date.month * 10 + horce_sex )

            if horce_id in self.parent_id_data:
                father_id = self.parent_id_data[horce_id]["father"]
                mother_id = self.parent_id_data[horce_id]["mother"]

            father_rank = self.match_rank_score( cd, father_id )
            mother_rank = self.match_rank_score( cd, mother_id )

            if race_id in self.horce_blood_type_data and \
              key_horce_num in self.horce_blood_type_data[race_id]:
                father_blood_type = self.horce_blood_type_data[race_id][key_horce_num]["father"]

            straight_dist = -1
            straight_flame = 0
            
            try:
                straight_dist = int( self.race_cource_info[key_place][key_kind][key_dist]["dist"][0] / 100 )
            except:
                pass

            if cd.horce_number() < cd.all_horce_num() / 3:
                straight_flame = int( 100 + straight_dist )
            elif ( cd.all_horce_num() / 3 ) * 2 <= cd.horce_number():
                straight_flame = int( 200 + straight_dist )

            ave_up3 = 36
            
            try:
                ave_up3 = self.up3_ave_data[key_place][key_kind][key_dist_kind]
            except:
                pass

            escape_within_rank = -1

            if limb_math == 1 or limb_math == 2:
                escape_within_rank = escape_within_rank_index.index( int( cd.horce_number() ) )

            self.analyze_data[horce_id] = {}
            self.analyze_data[horce_id]["ave_up3"] = ave_up3
            self.analyze_data[horce_id][data_name.age] = int( str_year ) - int( horce_id[0:4] )
            self.analyze_data[horce_id][data_name.all_horce_num] = cd.all_horce_num()
            self.analyze_data[horce_id][data_name.ave_burden_weight_diff] = \
              ave_burden_weight - current_race_data[data_name.burden_weight][i]
            self.analyze_data[horce_id][data_name.ave_first_last_diff] = pd.ave_first_last_diff()
            self.analyze_data[horce_id][data_name.ave_first_passing_rank] = pd.first_passing_rank()
            self.analyze_data[horce_id][data_name.ave_past_ave_first_horce_body] = \
              ave_past_ave_first_horce_body - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_ave_last_horce_body] = \
              ave_past_ave_last_horce_body - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_max_first_horce_body] = \
              ave_past_max_first_horce_body - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_max_last_horce_body] = \
              ave_past_max_last_horce_body - current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_min_first_horce_body] = \
              ave_past_min_first_horce_body - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_min_last_horce_body] = \
              ave_past_min_last_horce_body - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_race_horce_first_passing_true_skill] = \
              ave_race_horce_first_passing_true_skill - current_race_data[data_name.horce_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_race_horce_true_skill] = \
              ave_race_horce_true_skill - current_race_data[data_name.horce_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_race_jockey_first_passing_true_skill] = \
              ave_race_jockey_first_passing_true_skill - current_race_data[data_name.jockey_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_race_jockey_true_skill] = \
              ave_race_jockey_true_skill - current_race_data[data_name.jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_race_trainer_first_passing_true_skill] = \
              ave_race_trainer_first_passing_true_skill - current_race_data[data_name.trainer_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_race_trainer_true_skill] = \
              ave_race_trainer_true_skill - current_race_data[data_name.trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.ave_speed_index] = ave_speed_index - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.ave_up_rate] = ave_up_rate - current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.average_speed] = pd.average_speed()
            self.analyze_data[horce_id][data_name.baba] = cd.baba_status()
            self.analyze_data[horce_id][data_name.before_continue_not_three_rank] = pd.before_continue_not_three_rank()
            self.analyze_data[horce_id][data_name.before_diff] = before_diff
            self.analyze_data[horce_id][data_name.before_first_last_diff] = before_first_last_diff
            self.analyze_data[horce_id][data_name.before_first_passing_rank] = before_first_passing_rank
            self.analyze_data[horce_id][data_name.before_id_weight] = before_id_weight
            self.analyze_data[horce_id][data_name.before_last_passing_rank] = before_last_passing_rank
            self.analyze_data[horce_id][data_name.before_popular] = before_popular
            self.analyze_data[horce_id][data_name.before_race_score] = before_race_score
            self.analyze_data[horce_id][data_name.before_rank] = before_rank
            self.analyze_data[horce_id][data_name.before_speed] = before_speed
            self.analyze_data[horce_id][data_name.best_first_passing_rank] = pd.best_first_passing_rank()
            self.analyze_data[horce_id][data_name.best_second_passing_rank] = pd.best_second_passing_rank()
            self.analyze_data[horce_id][data_name.best_weight] = pd.best_weight()
            self.analyze_data[horce_id][data_name.burden_weight] = cd.burden_weight()
            self.analyze_data[horce_id][data_name.corner_diff_rank_ave] = current_race_data[data_name.corner_diff_rank_ave][i]
            self.analyze_data[horce_id][data_name.corner_diff_rank_ave_index] = \
              corner_diff_rank_ave_index.index( current_race_data[data_name.corner_diff_rank_ave][i] )
            self.analyze_data[horce_id][data_name.corner_diff_rank_ave_stand] = corner_diff_rank_ave_stand[i]
            self.analyze_data[horce_id][data_name.corner_true_skill] = current_race_data[data_name.corner_true_skill][i]
            self.analyze_data[horce_id][data_name.corner_true_skill_index] = \
              corner_true_skill_index.index( current_race_data[data_name.corner_true_skill][i] )
            self.analyze_data[horce_id][data_name.corner_true_skill_stand] = corner_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.diff_load_weight] = diff_load_weight
            self.analyze_data[horce_id][data_name.diff_pace_first_passing] = pd.diff_pace_first_passing()
            self.analyze_data[horce_id][data_name.diff_pace_time] = pd.diff_pace_time()
            self.analyze_data[horce_id][data_name.dist] = cd.dist() * 1000
            self.analyze_data[horce_id][data_name.dist_kind] = cd.dist_kind()
            self.analyze_data[horce_id][data_name.dist_kind_count] = pd.dist_kind_count()
            self.analyze_data[horce_id][data_name.escape_limb_count] = escape_limb_count
            self.analyze_data[horce_id][data_name.escape_limb1_count] = escape_limb1_count
            self.analyze_data[horce_id][data_name.escape_limb2_count] = escape_limb2_count
            self.analyze_data[horce_id][data_name.escape_within_rank] = escape_within_rank
            self.analyze_data[horce_id][data_name.father_blood_type] = int( cd.dist_kind() * 10 + father_blood_type )
            self.analyze_data[horce_id][data_name.father_rank] = father_rank
            self.analyze_data[horce_id][data_name.final_wrap] = current_race_data[data_name.final_wrap][i]
            self.analyze_data[horce_id][data_name.first_up3_halon_ave] = current_race_data[data_name.first_up3_halon_ave][i]
            self.analyze_data[horce_id][data_name.first_up3_halon_ave_stand] = first_up3_halon_ave_stand[i]
            self.analyze_data[horce_id][data_name.first_up3_halon_min] = current_race_data[data_name.first_up3_halon_min][i]
            self.analyze_data[horce_id][data_name.first_up3_halon_min_stand] = first_up3_halon_min_stand[i]
            self.analyze_data[horce_id][data_name.first_wrap] = current_race_data[data_name.first_wrap][i]
            self.analyze_data[horce_id][data_name.foot_used] = current_race_data[data_name.foot_used][i]
            self.analyze_data[horce_id][data_name.foot_used_best] = self.race_type.best_foot_used( cd, pd )
            self.analyze_data[horce_id][data_name.foot_used_index] = \
              foot_used_index.index( current_race_data[data_name.foot_used][i] )
            self.analyze_data[horce_id][data_name.foot_used_stand] = foot_used_stand[i]
            self.analyze_data[horce_id][data_name.high_level_score] = self.race_high_level.data_get( cd, pd, ymd )
            self.analyze_data[horce_id][data_name.horce_first_passing_true_skill] = \
              current_race_data[data_name.horce_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.horce_first_passing_true_skill_index] = \
              horce_first_passing_true_skill_index.index( current_race_data[data_name.horce_first_passing_true_skill][i] )
            self.analyze_data[horce_id][data_name.horce_first_passing_true_skill_stand] = horce_first_passing_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.horce_last_passing_true_skill] = \
              current_race_data[data_name.horce_last_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.horce_last_passing_true_skill_index] = \
              horce_last_passing_true_skill_index.index( current_race_data[data_name.horce_last_passing_true_skill][i] )
            self.analyze_data[horce_id][data_name.horce_num] = horce_num
            self.analyze_data[horce_id][data_name.horce_sex] = horce_sex
            self.analyze_data[horce_id][data_name.horce_sex_month] = horce_sex_month
            self.analyze_data[horce_id][data_name.horce_true_skill] = current_race_data[data_name.horce_true_skill][i]
            self.analyze_data[horce_id][data_name.horce_true_skill_index] = \
              horce_true_skill_index.index( current_race_data[data_name.horce_true_skill][i] )
            self.analyze_data[horce_id][data_name.horce_true_skill_stand] = horce_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.insert_limb_count] = insert_limb_count
            self.analyze_data[horce_id][data_name.jockey_first_passing_true_skill] = \
              current_race_data[data_name.jockey_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.jockey_first_passing_true_skill_index] = \
              jockey_first_passing_true_skill_index.index( current_race_data[data_name.jockey_first_passing_true_skill][i] )
            self.analyze_data[horce_id][data_name.jockey_first_passing_true_skill_stand] = \
              jockey_first_passing_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_baba] = current_race_data[data_name.jockey_judgment_baba][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_baba_index] = \
              jockey_judgment_baba_index.index( current_race_data[data_name.jockey_judgment_baba][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_baba_stand] = jockey_judgment_baba_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_dist] = current_race_data[data_name.jockey_judgment_dist][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_dist_index] = \
              jockey_judgment_dist_index.index( current_race_data[data_name.jockey_judgment_dist][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_dist_stand] = jockey_judgment_dist_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_flame_num] = \
              current_race_data[data_name.jockey_judgment_flame_num][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_flame_num_index] = \
              jockey_judgment_flame_num_index.index( current_race_data[data_name.jockey_judgment_flame_num][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_flame_num_stand] = jockey_judgment_flame_num_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_kind] = current_race_data[data_name.jockey_judgment_kind][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_kind_index] = \
              jockey_judgment_kind_index.index( current_race_data[data_name.jockey_judgment_kind][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_kind_stand] = jockey_judgment_kind_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_limb] = current_race_data[data_name.jockey_judgment_limb][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_limb_index] = \
              jockey_judgment_limb_index.index( current_race_data[data_name.jockey_judgment_limb][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_limb_stand] = jockey_judgment_limb_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_place] = current_race_data[data_name.jockey_judgment_place][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_place_index] = \
              jockey_judgment_place_index.index( current_race_data[data_name.jockey_judgment_place][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_place_stand] = jockey_judgment_place_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_popular] = \
              current_race_data[data_name.jockey_judgment_popular][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_popular_index] = \
              jockey_judgment_popular_index.index( current_race_data[data_name.jockey_judgment_popular][i] )
            self.analyze_data[horce_id][data_name.jockey_judgment_popular_stand] = jockey_judgment_popular_stand[i]            
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_baba_0] = \
              current_race_data[data_name.jockey_judgment_rate_baba_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_baba_1] = \
              current_race_data[data_name.jockey_judgment_rate_baba_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_baba_2] = \
              current_race_data[data_name.jockey_judgment_rate_baba_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_dist_0] = \
              current_race_data[data_name.jockey_judgment_rate_dist_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_dist_1] = \
              current_race_data[data_name.jockey_judgment_rate_dist_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_dist_2] = \
              current_race_data[data_name.jockey_judgment_rate_dist_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_flame_num_0] = \
              current_race_data[data_name.jockey_judgment_rate_flame_num_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_flame_num_1] = \
              current_race_data[data_name.jockey_judgment_rate_flame_num_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_flame_num_2] = \
              current_race_data[data_name.jockey_judgment_rate_flame_num_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_kind_0] = \
              current_race_data[data_name.jockey_judgment_rate_kind_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_kind_1] = \
              current_race_data[data_name.jockey_judgment_rate_kind_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_kind_2] = \
              current_race_data[data_name.jockey_judgment_rate_kind_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_limb_0] = \
              current_race_data[data_name.jockey_judgment_rate_limb_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_limb_1] = \
              current_race_data[data_name.jockey_judgment_rate_limb_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_limb_2] = \
              current_race_data[data_name.jockey_judgment_rate_limb_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_place_0] = \
              current_race_data[data_name.jockey_judgment_rate_place_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_place_1] = \
              current_race_data[data_name.jockey_judgment_rate_place_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_place_2] = \
              current_race_data[data_name.jockey_judgment_rate_place_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_popular_0] = \
              current_race_data[data_name.jockey_judgment_rate_popular_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_popular_1] = \
              current_race_data[data_name.jockey_judgment_rate_popular_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_rate_popular_2] = \
              current_race_data[data_name.jockey_judgment_rate_popular_2][i]            
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_baba] = \
              current_race_data[data_name.jockey_judgment_up3_baba][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_baba_stand] = jockey_judgment_up3_baba_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_dist] = \
              current_race_data[data_name.jockey_judgment_up3_dist][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_dist_stand] = jockey_judgment_up3_dist_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_flame_num] = \
              current_race_data[data_name.jockey_judgment_up3_flame_num][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_flame_num_stand] = jockey_judgment_up3_flame_num_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_kind] = \
              current_race_data[data_name.jockey_judgment_up3_kind][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_kind_stand] = jockey_judgment_up3_kind_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_limb] = \
              current_race_data[data_name.jockey_judgment_up3_limb][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_limb_stand] = jockey_judgment_up3_limb_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_place] = \
              current_race_data[data_name.jockey_judgment_up3_place][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_place_stand] = jockey_judgment_up3_place_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_popular] = \
              current_race_data[data_name.jockey_judgment_up3_popular][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_popular_stand] = jockey_judgment_up3_popular_stand[i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_baba_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_baba_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_baba_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_baba_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_baba_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_baba_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_dist_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_dist_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_dist_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_dist_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_dist_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_dist_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_flame_num_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_flame_num_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_flame_num_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_flame_num_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_flame_num_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_flame_num_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_kind_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_kind_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_kind_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_kind_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_kind_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_kind_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_limb_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_limb_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_limb_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_limb_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_limb_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_limb_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_place_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_place_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_place_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_place_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_place_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_place_2][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_popular_0] = \
              current_race_data[data_name.jockey_judgment_up3_rate_popular_0][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_popular_1] = \
              current_race_data[data_name.jockey_judgment_up3_rate_popular_1][i]
            self.analyze_data[horce_id][data_name.jockey_judgment_up3_rate_popular_2] = \
              current_race_data[data_name.jockey_judgment_up3_rate_popular_2][i]
            self.analyze_data[horce_id][data_name.jockey_last_passing_true_skill] = \
              current_race_data[data_name.jockey_last_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.jockey_last_passing_true_skill_index] = \
              jockey_last_passing_true_skill_index.index( current_race_data[data_name.jockey_last_passing_true_skill][i] )
            self.analyze_data[horce_id][data_name.jockey_rank] = self.jockey_data.rank( race_id, horce_id )
            self.analyze_data[horce_id][data_name.jockey_true_skill] = current_race_data[data_name.jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.jockey_true_skill_index] = \
              jockey_true_skill_index.index( current_race_data[data_name.jockey_true_skill][i] )
            self.analyze_data[horce_id][data_name.jockey_true_skill_stand] = jockey_true_skill_stand[i] 
            self.analyze_data[horce_id][data_name.jockey_year_rank] = \
              self.jockey_data.year_rank( race_id, horce_id, key_before_year )
            self.analyze_data[horce_id][data_name.kind] = cd.race_kind()
            self.analyze_data[horce_id][data_name.level_score] = current_race_data[data_name.level_score][i]
            self.analyze_data[horce_id][data_name.level_score_index] = \
              level_score_index.index( current_race_data[data_name.level_score][i] )
            self.analyze_data[horce_id][data_name.level_score_stand] = level_score_stand[i]
            self.analyze_data[horce_id][data_name.limb] = limb_math
            self.analyze_data[horce_id][data_name.limb_horce_number] = int( limb_math * 100 + int( cd.horce_number() / 2 ) )
            self.analyze_data[horce_id][data_name.match_rank] = current_race_data[data_name.match_rank][i]
            self.analyze_data[horce_id][data_name.match_rank_index] = \
              match_rank_index.index( current_race_data[data_name.match_rank][i] )
            self.analyze_data[horce_id][data_name.match_rank_stand] = match_rank_stand[i]
            self.analyze_data[horce_id][data_name.match_up3] = current_race_data[data_name.match_up3][i] / ave_up3 - 1
            self.analyze_data[horce_id][data_name.match_up3_index] = \
              match_up3_index.index( current_race_data[data_name.match_up3][i] )
            self.analyze_data[horce_id][data_name.match_up3_stand] = match_up3_stand[i]            
            self.analyze_data[horce_id][data_name.max_past_ave_first_horce_body] = \
              max_past_ave_first_horce_body - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_ave_last_horce_body] = \
              max_past_ave_last_horce_body - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_max_first_horce_body] = \
              max_past_max_first_horce_body - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_max_last_horce_body] = \
              max_past_max_last_horce_body - current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_min_first_horce_body] = \
              max_past_min_first_horce_body - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_min_last_horce_body] = \
              max_past_min_last_horce_body - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_race_horce_first_passing_true_skill] = \
              max_race_horce_first_passing_true_skill - current_race_data[data_name.horce_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.max_race_horce_true_skill] = \
              max_race_horce_true_skill - current_race_data[data_name.horce_true_skill][i]
            self.analyze_data[horce_id][data_name.max_race_jockey_first_passing_true_skill] = \
              max_race_jockey_first_passing_true_skill - current_race_data[data_name.jockey_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.max_race_jockey_true_skill] = \
              max_race_jockey_true_skill - current_race_data[data_name.jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.max_race_trainer_first_passing_true_skill] = \
              max_race_trainer_first_passing_true_skill - current_race_data[data_name.trainer_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.max_race_trainer_true_skill] = \
              max_race_trainer_true_skill - current_race_data[data_name.trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.max_speed_index] = \
              max_speed_index - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.max_up_rate] = \
              max_up_rate - current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.min_past_ave_first_horce_body] = \
              min_past_ave_first_horce_body - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_ave_last_horce_body] = \
              min_past_ave_last_horce_body - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_max_first_horce_body] = \
              min_past_max_first_horce_body - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_max_last_horce_body] = \
              min_past_max_last_horce_body - current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_min_first_horce_body] = \
              min_past_min_first_horce_body - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_min_last_horce_body] = \
              min_past_min_last_horce_body - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_race_horce_first_passing_true_skill] = \
              min_race_horce_first_passing_true_skill - current_race_data[data_name.horce_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_horce_true_skill] = \
              min_race_horce_true_skill - current_race_data[data_name.horce_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_jockey_first_passing_true_skill] = \
              min_race_jockey_first_passing_true_skill - current_race_data[data_name.jockey_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_jockey_true_skill] = \
              min_race_jockey_true_skill - current_race_data[data_name.jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_trainer_first_passing_true_skill] = \
              min_race_trainer_first_passing_true_skill - current_race_data[data_name.trainer_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_trainer_true_skill] = \
              min_race_trainer_true_skill - current_race_data[data_name.trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.min_speed_index] = \
              min_speed_index - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.min_up3] = pd.min_up3() / ave_up3 - 1
            self.analyze_data[horce_id][data_name.min_up_rate] = \
              min_up_rate - current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.money] = pd.get_money()
            self.analyze_data[horce_id][data_name.money_class] = lib.money_class_get( self.storage.race_money )
            self.analyze_data[horce_id][data_name.mother_rank] = mother_rank
            self.analyze_data[horce_id][data_name.my_limb_count] = my_limb_count[limb_math]
            self.analyze_data[horce_id][data_name.odds] = cd.odds()
            self.analyze_data[horce_id][data_name.one_popular_odds] = one_popular_odds
            self.analyze_data[horce_id][data_name.one_popular_limb] = one_popular_limb
            self.analyze_data[horce_id][data_name.one_rate] = pd.one_rate()
            self.analyze_data[horce_id][data_name.pace_up] = pd.pace_up_check()
            self.analyze_data[horce_id][data_name.passing_regression] = pd.passing_regression()
            self.analyze_data[horce_id][data_name.past_ave_first_horce_body] = \
              current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.past_ave_last_horce_body] = \
              current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.past_ave_first_horce_body_index] = \
              past_ave_first_horce_body_index.index( current_race_data[data_name.past_ave_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.past_ave_last_horce_body_index] = \
              past_ave_last_horce_body_index.index( current_race_data[data_name.past_ave_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.past_ave_first_horce_body_stand] = past_ave_first_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_ave_last_horce_body_stand] = past_ave_last_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_max_first_horce_body] = \
              current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.past_max_last_horce_body] = \
              current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.past_max_first_horce_body_stand] = past_max_first_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_max_last_horce_body_stand] = past_max_last_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_min_first_horce_body] = \
              current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.past_min_last_horce_body] = \
              current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.past_min_first_horce_body_index] = \
              past_min_first_horce_body_index.index( current_race_data[data_name.past_min_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.past_min_last_horce_body_index] = \
              past_min_last_horce_body_index.index( current_race_data[data_name.past_min_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.past_min_first_horce_body_stand] = past_min_first_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_min_last_horce_body_stand] = past_min_last_horce_body_stand[i]
            self.analyze_data[horce_id][data_name.past_std_first_horce_body] = current_race_data[data_name.past_std_first_horce_body][i]
            self.analyze_data[horce_id][data_name.past_std_last_horce_body] = current_race_data[data_name.past_std_last_horce_body][i]
            self.analyze_data[horce_id][data_name.place] = cd.place()
            self.analyze_data[horce_id][data_name.popular] = cd.popular()
            self.analyze_data[horce_id][data_name.popular_rank] = popular_rank
            self.analyze_data[horce_id][data_name.predict_first_passing_rank] = None
            self.analyze_data[horce_id][data_name.predict_first_passing_rank_index] = None
            self.analyze_data[horce_id][data_name.predict_first_passing_rank_stand] = None
            self.analyze_data[horce_id][data_name.predict_last_passing_rank] = None
            self.analyze_data[horce_id][data_name.predict_last_passing_rank_index] = None
            self.analyze_data[horce_id][data_name.predict_last_passing_rank_stand] = None
            self.analyze_data[horce_id][data_name.predict_pace] = None
            self.analyze_data[horce_id][data_name.predict_train_score] = None
            self.analyze_data[horce_id][data_name.predict_train_score_index] = None
            self.analyze_data[horce_id][data_name.predict_train_score_stand] = None
            self.analyze_data[horce_id][data_name.predict_up3] = None
            self.analyze_data[horce_id][data_name.predict_up3_index] = None
            self.analyze_data[horce_id][data_name.predict_up3_stand] = None
            self.analyze_data[horce_id][data_name.race_interval] = min( max( pd.race_interval(), 0 ), 20 )
            self.analyze_data[horce_id][data_name.race_num] = cd.race_num()
            self.analyze_data[horce_id][data_name.speed_index] = current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.speed_index_index] = \
              speed_index_index.index( current_race_data[data_name.speed_index][i] )
            #print( horce_id, cd.horce_number(), speed_index_index, current_race_data[data_name.speed_index][i] )
            self.analyze_data[horce_id][data_name.speed_index_stand] = speed_index_stand[i]
            self.analyze_data[horce_id][data_name.stand_final_wrap] = final_wrap_stand[i]
            self.analyze_data[horce_id][data_name.stand_first_wrap] = first_wrap_stand[i]
            self.analyze_data[horce_id][data_name.stand_train_time_rate] = train_time_rate_stand[i]
            self.analyze_data[horce_id][data_name.stand_train_time_slice] = train_time_slice_stand[i]
            self.analyze_data[horce_id][data_name.stand_train_time_slope] = train_time_slope_stand[i]
            self.analyze_data[horce_id][data_name.stand_wrap_diff] = wrap_diff_stand[i]
            self.analyze_data[horce_id][data_name.stand_wrap_rate] = wrap_rate_stand[i]
            self.analyze_data[horce_id][data_name.stand_wrap_slice] = wrap_slice_stand[i]
            self.analyze_data[horce_id][data_name.stand_wrap_slope] = wrap_slope_stand[i]
            self.analyze_data[horce_id][data_name.stand_wrap_std] = wrap_std_stand[i]
            self.analyze_data[horce_id][data_name.std_past_ave_first_horce_body] = std_past_ave_first_horce_body
            self.analyze_data[horce_id][data_name.std_past_ave_last_horce_body] = std_past_ave_last_horce_body
            self.analyze_data[horce_id][data_name.std_past_max_first_horce_body] = std_past_max_first_horce_body
            self.analyze_data[horce_id][data_name.std_past_max_last_horce_body] = std_past_max_last_horce_body
            self.analyze_data[horce_id][data_name.std_past_min_first_horce_body] = std_past_min_first_horce_body
            self.analyze_data[horce_id][data_name.std_past_min_last_horce_body] = std_past_min_last_horce_body
            self.analyze_data[horce_id][data_name.std_race_horce_first_passing_true_skill] = \
              std_race_horce_first_passing_true_skill
            self.analyze_data[horce_id][data_name.std_race_horce_true_skill] = std_race_horce_true_skill
            self.analyze_data[horce_id][data_name.std_race_jockey_first_passing_true_skill] = \
              std_race_jockey_first_passing_true_skill
            self.analyze_data[horce_id][data_name.std_race_jockey_true_skill] = std_race_jockey_true_skill
            self.analyze_data[horce_id][data_name.std_race_trainer_first_passing_true_skill] = \
              std_race_trainer_first_passing_true_skill
            self.analyze_data[horce_id][data_name.std_race_trainer_true_skill] = std_race_trainer_true_skill
            self.analyze_data[horce_id][data_name.std_speed_index] = std_speed_index
            self.analyze_data[horce_id][data_name.std_up_rate] = std_up_rate
            self.analyze_data[horce_id][data_name.straight_flame] = straight_flame
            self.analyze_data[horce_id][data_name.straight_slope] = self.race_type.stright_slope( cd, pd )
            self.analyze_data[horce_id][data_name.three_average] = pd.three_average()
            self.analyze_data[horce_id][data_name.three_difference] = pd.three_difference()
            self.analyze_data[horce_id][data_name.three_popular_limb] = three_popular_limb
            self.analyze_data[horce_id][data_name.three_rate] = pd.three_rate()
            self.analyze_data[horce_id][data_name.train_time_rate] = current_race_data[data_name.train_time_rate][i]
            self.analyze_data[horce_id][data_name.train_time_slice] = current_race_data[data_name.train_time_slice][i]
            self.analyze_data[horce_id][data_name.train_time_slope] = current_race_data[data_name.train_time_slope][i]
            self.analyze_data[horce_id][data_name.trainer_first_passing_true_skill] = \
              current_race_data[data_name.trainer_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.trainer_first_passing_true_skill_index] = \
              trainer_first_passing_true_skill_index.index( current_race_data[data_name.trainer_first_passing_true_skill][i] )
            self.analyze_data[horce_id][data_name.trainer_first_passing_true_skill_stand] = \
              trainer_first_passing_true_skill_stand[i]            
            self.analyze_data[horce_id][data_name.trainer_judgment_baba] = current_race_data[data_name.trainer_judgment_baba][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_dist] = current_race_data[data_name.trainer_judgment_dist][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_flame_num] = \
              current_race_data[data_name.trainer_judgment_flame_num][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_kind] = current_race_data[data_name.trainer_judgment_kind][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_limb] = current_race_data[data_name.trainer_judgment_limb][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_place] = current_race_data[data_name.trainer_judgment_place][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_popular] = \
              current_race_data[data_name.trainer_judgment_popular][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_baba] = \
              current_race_data[data_name.trainer_judgment_up3_baba][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_dist] = \
              current_race_data[data_name.trainer_judgment_up3_dist][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_flame_num] = \
              current_race_data[data_name.trainer_judgment_up3_flame_num][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_kind] = \
              current_race_data[data_name.trainer_judgment_up3_kind][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_limb] = \
              current_race_data[data_name.trainer_judgment_up3_limb][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_place] = \
              current_race_data[data_name.trainer_judgment_up3_place][i]
            self.analyze_data[horce_id][data_name.trainer_judgment_up3_popular] = \
              current_race_data[data_name.trainer_judgment_up3_popular][i]
            self.analyze_data[horce_id][data_name.trainer_rank] = \
              self.trainer_data.rank( race_id, \
                                     horce_id, \
                                     race_info = race_info, \
                                     trainer_id = self.storage.current_horce_data[horce_id].trainer_id )
            self.analyze_data[horce_id][data_name.trainer_true_skill] = current_race_data[data_name.trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.trainer_true_skill_index] = \
              trainer_true_skill_index.index( current_race_data[data_name.trainer_true_skill][i] )
            self.analyze_data[horce_id][data_name.trainer_true_skill_stand] = trainer_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.two_popular_limb] = two_popular_limb
            self.analyze_data[horce_id][data_name.two_popular_odds] = two_popular_odds
            self.analyze_data[horce_id][data_name.two_rate] = pd.two_rate()
            self.analyze_data[horce_id][data_name.up3_horce_true_skill] = current_race_data[data_name.up3_horce_true_skill][i]
            self.analyze_data[horce_id][data_name.up3_horce_true_skill_index] = \
              up3_horce_true_skill_index.index( current_race_data[data_name.up3_horce_true_skill][i] )
            self.analyze_data[horce_id][data_name.up3_horce_true_skill_stand] = up3_horce_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.up3_jockey_true_skill] = current_race_data[data_name.up3_jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.up3_jockey_true_skill_index] = \
              up3_jockey_true_skill_index.index( current_race_data[data_name.up3_jockey_true_skill][i] )
            self.analyze_data[horce_id][data_name.up3_jockey_true_skill_stand] = up3_jockey_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.up3_standard_value] = up3_standard_value
            self.analyze_data[horce_id][data_name.up3_trainer_true_skill] = current_race_data[data_name.up3_trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.up3_trainer_true_skill_index] = \
              up3_trainer_true_skill_index.index( current_race_data[data_name.up3_trainer_true_skill][i] )
            self.analyze_data[horce_id][data_name.up3_trainer_true_skill_stand] = up3_trainer_true_skill_stand[i]
            self.analyze_data[horce_id][data_name.up_rate] = current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.up_rate_index] = up_rate_index.index( current_race_data[data_name.up_rate][i] )
            self.analyze_data[horce_id][data_name.up_rate_stand] = up_rate_stand[i]
            self.analyze_data[horce_id][data_name.waku_three_rate] = \
              lib.kind_score_get( self.waku_three_rate_data, self.waku_three_key_list, kind_key_data, str( int( waku ) ) )
            self.analyze_data[horce_id][data_name.weather] = cd.weather()
            self.analyze_data[horce_id][data_name.weight] = cd.weight() / 10
            self.analyze_data[horce_id][data_name.wrap_diff] = current_race_data[data_name.wrap_diff][i]
            self.analyze_data[horce_id][data_name.wrap_rate] = current_race_data[data_name.wrap_rate][i]
            self.analyze_data[horce_id][data_name.wrap_slice] = current_race_data[data_name.wrap_slice][i]
            self.analyze_data[horce_id][data_name.wrap_slope] = current_race_data[data_name.wrap_slope][i]
            self.analyze_data[horce_id][data_name.wrap_std] = current_race_data[data_name.wrap_std][i]
