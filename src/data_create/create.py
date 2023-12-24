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
from sekitoba_data_create.stride_ablity import StrideAblity

dm.dl.file_set( pickle_name.horce_data_storage )
dm.dl.file_set( pickle_name.corner_horce_body )
dm.dl.file_set( pickle_name.baba_index_data )
dm.dl.file_set( pickle_name.parent_id_data )
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
dm.dl.file_set( pickle_name.trainer_judgment_prod_data )
dm.dl.file_set( pickle_name.trainer_judgment_up3_prod_data )
dm.dl.file_set( pickle_name.waku_three_rate_data )
dm.dl.file_set( pickle_name.up3_ave_data )
dm.dl.file_set( pickle_name.flame_evaluation_data )

STR_AVE = "ave_"
STR_MAX = "max_"
STR_MIN = "min_"
STR_STD = "std_"
STR_INDEX = "index_"
STAND_INDEX = "stand_"

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
        self.stride_ablity = StrideAblity()
        self.train_index.train_time_data.update( { self.storage.today_data.race_id: self.train_data_create() } )
        self.race_type.race_rank_data.update( { self.storage.today_data.race_id: int( lib.money_class_get( self.storage.race_money ) ) } )
        
        self.horce_data_storage = dm.dl.data_get( pickle_name.horce_data_storage )
        self.corner_horce_body = dm.dl.data_get( pickle_name.corner_horce_body )
        self.baba_index_data = dm.dl.data_get( pickle_name.baba_index_data )
        self.parent_id_data = dm.dl.data_get( pickle_name.parent_id_data )
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
        #self.race_cource_info = dm.dl.data_get( pickle_name.race_cource_info )
        self.trainer_judgment_prod_data = dm.dl.data_get( pickle_name.trainer_judgment_prod_data )
        self.trainer_judgment_up3_prod_data = dm.dl.data_get( pickle_name.trainer_judgment_up3_prod_data )
        self.waku_three_rate_data = dm.dl.data_get( pickle_name.waku_three_rate_data )
        self.up3_ave_data = dm.dl.data_get( pickle_name.up3_ave_data )
        self.flame_evaluation_data = dm.dl.data_get( pickle_name.flame_evaluation_data )

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
        three_popular_odds = 0
        escape_limb1_count = 0
        escape_limb2_count = 0
        escape_limb_count = 0
        insert_limb_count = 0
        female_count = 0
        male_count = 0
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

            _, past_data = lib.race_check( self.horce_data_storage[horce_id], \
                                          str_year, str_day, str_num, str_place_num )
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
            
            before_cd = pd.before_cd()
            jockey_id = self.storage.current_horce_data[horce_id].jockey_id
            trainer_id = self.storage.current_horce_data[horce_id].trainer_id
            horce_num = cd.horce_number()
            popular = cd.popular()
            odds = cd.odds()
            limb_math = lib.limb_search( pd )
            escape_within_rank = -1
            
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
            
            if not before_cd == None:
                before_diff = before_cd.diff()
                before_first_last_diff = before_cd.first_last_diff()
                before_id_weight = before_cd.id_weight()
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
                    pass

                try:
                    before_last_passing_rank = int( before_passing_list[-1] )
                except:
                    pass

            if horce_id in self.horce_sex_data:
                if self.horce_sex_data[horce_id] == 0:
                    male_count += 1
                elif self.horce_sex_data[horce_id] == 1:
                    female_count += 1
            
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
                three_popular_odds = odds
            
            past_min_first_horce_body = -1000
            past_min_last_horce_body = -1000
            past_max_first_horce_body = -1000
            past_max_last_horce_body = -1000
            past_ave_first_horce_body = -1000
            past_ave_last_horce_body = -1000
            past_std_first_horce_body = -1000
            past_std_last_horce_body = -1000
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
            trainer_last_passing_true_skill = 25
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

            if trainer_id in self.last_passing_true_skill_prod_data["trainer"]:
                trainer_last_passing_true_skill = self.last_passing_true_skill_prod_data["trainer"][trainer_id]

            if horce_id in self.up3_true_skill_prod_data["horce"]:
                up3_horce_true_skill = self.up3_true_skill_prod_data["horce"][horce_id]

            if jockey_id in self.up3_true_skill_prod_data["jockey"]:
                up3_jockey_true_skill = self.up3_true_skill_prod_data["jockey"][jockey_id]
                
            if trainer_id in self.up3_true_skill_prod_data["trainer"]:
                up3_trainer_true_skill = self.up3_true_skill_prod_data["trainer"][trainer_id]

            if horce_id in self.corner_true_skill_prod_data["horce"]:
                corner_true_skill = self.corner_true_skill_prod_data["horce"][horce_id]

            speed = []
            up_speed = []
            current_time_index = self.time_index.main( horce_id, pd.past_day_list() )

            if horce_id in self.baba_index_data:
                speed, up_speed, _ = pd.speed_index( self.baba_index_data[horce_id] )

            stride_ablity_data = self.stride_ablity.ablity_create( cd, pd )
            
            for stride_data_key in stride_ablity_data.keys():
                for math_key in stride_ablity_data[stride_data_key].keys():
                    current_race_data[stride_data_key+"_"+math_key].append( stride_ablity_data[stride_data_key][math_key] )

            condition_devi = -1000

            if horce_id in self.storage.condition_devi:
                condition_devi = self.storage.condition_devi[horce_id]
            
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

            current_race_data[data_name.before_diff].append( before_diff )
            current_race_data[data_name.before_first_passing_rank].append( before_first_passing_rank )
            current_race_data[data_name.before_id_weight].append( before_id_weight )
            current_race_data[data_name.before_last_passing_rank].append( before_last_passing_rank )
            current_race_data[data_name.before_popular].append( before_popular )
            current_race_data[data_name.before_race_score].append( before_race_score )
            current_race_data[data_name.before_rank].append( before_rank )
            current_race_data[data_name.before_speed].append( before_speed )
            current_race_data[data_name.before_first_last_diff].append( before_first_last_diff )
            current_race_data[data_name.best_first_passing_rank].append( pd.best_first_passing_rank() )
            current_race_data[data_name.best_second_passing_rank].append( pd.best_second_passing_rank() )
            current_race_data[data_name.condition_devi].append( condition_devi )
            current_race_data[data_name.diff_pace_first_passing].append( pd.diff_pace_first_passing() )
            current_race_data[data_name.diff_pace_time].append( pd.diff_pace_time() )
            current_race_data[data_name.first_result_rank_diff].append( pd.first_result_rank_diff() )
            current_race_data[data_name.last_result_rank_diff].append( pd.last_result_rank_diff() )
            current_race_data[data_name.burden_weight].append( cd.burden_weight() )
            current_race_data[data_name.diff_load_weight].append( diff_load_weight )
            current_race_data[data_name.escape_within_rank].append( escape_within_rank )
            current_race_data[data_name.past_ave_first_horce_body].append( past_ave_first_horce_body )
            current_race_data[data_name.past_ave_last_horce_body].append( past_ave_last_horce_body )
            current_race_data[data_name.past_max_first_horce_body].append( past_max_first_horce_body )
            current_race_data[data_name.past_max_last_horce_body].append( past_max_last_horce_body )
            current_race_data[data_name.past_min_first_horce_body].append( past_min_first_horce_body )
            current_race_data[data_name.past_min_last_horce_body].append( past_min_last_horce_body )
            current_race_data[data_name.past_std_first_horce_body].append( past_std_first_horce_body )
            current_race_data[data_name.past_std_last_horce_body].append( past_std_last_horce_body )
            current_race_data[data_name.passing_regression].append( pd.passing_regression() )
            current_race_data[data_name.horce_first_passing_true_skill].append( horce_first_passing_true_skill )
            current_race_data[data_name.jockey_first_passing_true_skill].append( jockey_first_passing_true_skill )
            current_race_data[data_name.trainer_first_passing_true_skill].append( trainer_first_passing_true_skill )
            current_race_data[data_name.horce_true_skill].append( horce_true_skill )
            current_race_data[data_name.jockey_true_skill].append( jockey_true_skill )
            current_race_data[data_name.trainer_true_skill].append( trainer_true_skill )
            current_race_data[data_name.jockey_last_passing_true_skill].append( jockey_last_passing_true_skill )
            current_race_data[data_name.horce_last_passing_true_skill].append( horce_last_passing_true_skill )
            current_race_data[data_name.trainer_last_passing_true_skill].append( trainer_last_passing_true_skill )
            current_race_data[data_name.popular_rank].append( popular_rank )
            current_race_data[data_name.up3_horce_true_skill].append( up3_horce_true_skill )
            current_race_data[data_name.up3_jockey_true_skill].append( up3_jockey_true_skill )
            current_race_data[data_name.up3_trainer_true_skill].append( up3_trainer_true_skill )
            current_race_data[data_name.up3_standard_value].append( up3_standard_value )
            current_race_data[data_name.speed_index].append( lib.max_check( speed ) + current_time_index["max"] )
            current_race_data[data_name.up_rate].append( pd.up_rate( key_money_class ) )
            current_race_data[data_name.corner_diff_rank_ave].append( pd.corner_diff_rank() )
            current_race_data[data_name.corner_true_skill].append( corner_true_skill )
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
            current_race_data[data_name.min_up3].append( pd.min_up3() )
            current_race_data[data_name.up_index].append( lib.max_check( up_speed ) )
            current_race_data[data_name.match_rank].append( pd.match_rank() )
            current_race_data[data_name.match_up3].append( pd.match_up3() )
            current_race_data[data_name.max_time_point].append( pd.max_time_point() )
            current_race_data[data_name.max_up3].append( pd.max_up3() )
            current_race_data[data_name.max_up3_time_point].append( pd.max_up3_time_point( str( int( limb_math ) ) ) )
            current_race_data[data_name.level_up3].append( pd.level_up3() )
            horce_id_list.append( horce_id )

        N = len( horce_id_list )
        
        if N == 0:
            return False

        current_key_list = []

        for data_key in current_race_data.keys():
            if not type( current_race_data[data_key] ) is list or \
              len( current_race_data[data_key] ) == 0:
                continue

            current_key_list.append( data_key )

        for data_key in current_key_list:
            current_race_data[data_key+"_index"] = sorted( current_race_data[data_key], reverse = True )
            current_race_data[data_key+"_stand"] = lib.standardization( current_race_data[data_key] )
            current_race_data[data_key+"_devi"] = lib.deviation_value( current_race_data[data_key] )
            current_race_data["ave_"+data_key] = sum( current_race_data[data_key] ) / N
            current_race_data["max_"+data_key] = max( current_race_data[data_key] )
            current_race_data["min_"+data_key] = min( current_race_data[data_key] )
            current_race_data["std_"+data_key] = stdev( current_race_data[data_key] )
            current_race_data["ave_race_"+data_key] = sum( current_race_data[data_key] ) / N
            current_race_data["max_race_"+data_key] = max( current_race_data[data_key] )
            current_race_data["min_race_"+data_key] = min( current_race_data[data_key] )
            current_race_data["std_race_"+data_key] = stdev( current_race_data[data_key] )
            current_race_data["max_stand_race_"+data_key] = max( lib.standardization( current_race_data[data_key] ) )

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

            _, past_data = lib.race_check( self.horce_data_storage[horce_id], \
                                          str_year, str_day, str_num, str_place_num )
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
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
            #father_blood_type = 0
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

            escape_within_rank = -1

            if limb_math == 1 or limb_math == 2:
                escape_within_rank = escape_within_rank_index.index( int( cd.horce_number() ) )

            predict_netkeiba_deployment = -1

            for t in range( 0, len( self.storage.predict_netkeiba_deployment ) ):
                if int( horce_num ) in self.storage.predict_netkeiba_deployment[t]:
                    predict_netkeiba_deployment = t
                    break

            flame_evaluation_one = -1
            flame_evaluation_two = -1
            flame_evaluation_three = -1

            try:
                flame_evaluation_one = self.flame_evaluation_data[int(cd.place())][int(str_day)][int(cd.flame_number())]["one"]
                flame_evaluation_two = self.flame_evaluation_data[int(cd.place())][int(str_day)][int(cd.flame_number())]["two"]
                flame_evaluation_three = self.flame_evaluation_data[int(cd.place())][int(str_day)][int(cd.flame_number())]["three"]
            except:
                pass                

            self.analyze_data[horce_id] = {}
            self.analyze_data[horce_id][data_name.insert_limb_count] = insert_limb_count
            self.analyze_data[horce_id][data_name.age] = int( str_year ) - int( horce_id[0:4] )
            self.analyze_data[horce_id][data_name.all_horce_num] = cd.all_horce_num()
            self.analyze_data[horce_id][data_name.ave_burden_weight_diff] = \
              current_race_data[STR_AVE+"race_"+data_name.burden_weight] - current_race_data[data_name.burden_weight][i]
            self.analyze_data[horce_id][data_name.burden_weight] = current_race_data[data_name.burden_weight][i]
            self.analyze_data[horce_id][data_name.ave_first_last_diff] = pd.ave_first_last_diff()
            self.analyze_data[horce_id][data_name.ave_first_passing_rank] = pd.first_passing_rank()
            self.analyze_data[horce_id][data_name.ave_past_ave_first_horce_body] = \
              current_race_data[STR_AVE+data_name.past_ave_first_horce_body] - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_ave_last_horce_body] = \
              current_race_data[STR_AVE+data_name.past_ave_last_horce_body] - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_max_first_horce_body] = \
              current_race_data[STR_AVE+data_name.past_max_first_horce_body] - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_max_last_horce_body] = \
              current_race_data[STR_AVE+data_name.past_max_last_horce_body] - current_race_data[data_name.past_max_last_horce_body][i]            
            self.analyze_data[horce_id][data_name.ave_past_min_first_horce_body] = \
              current_race_data[STR_AVE+data_name.past_min_first_horce_body] - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_past_min_last_horce_body] = \
              current_race_data[STR_AVE+data_name.past_min_last_horce_body] - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.ave_speed_index] = \
              current_race_data[STR_AVE+data_name.speed_index] - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.std_speed_index] = current_race_data[data_name.std_speed_index]
            self.analyze_data[horce_id][data_name.std_race_speed_index] = current_race_data[data_name.std_race_speed_index]
            self.analyze_data[horce_id][data_name.max_stand_race_speed_index] = current_race_data[data_name.max_stand_race_speed_index]
            self.analyze_data[horce_id][data_name.ave_up_rate] = \
              current_race_data[STR_AVE+data_name.up_rate] - current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.average_speed] = pd.average_speed()
            self.analyze_data[horce_id][data_name.baba] = cd.baba_status()
            self.analyze_data[horce_id][data_name.before_continue_not_three_rank] = pd.before_continue_not_three_rank()
            self.analyze_data[horce_id][data_name.best_first_passing_rank] = pd.best_first_passing_rank()
            self.analyze_data[horce_id][data_name.best_second_passing_rank] = pd.best_second_passing_rank()
            self.analyze_data[horce_id][data_name.best_weight] = pd.best_weight()
            self.analyze_data[horce_id][data_name.diff_pace_first_passing] = pd.diff_pace_first_passing()
            self.analyze_data[horce_id][data_name.diff_pace_time] = pd.diff_pace_time()
            self.analyze_data[horce_id][data_name.dist] = cd.dist() * 1000
            self.analyze_data[horce_id][data_name.dist_kind] = cd.dist_kind()
            self.analyze_data[horce_id][data_name.dist_kind_count] = pd.dist_kind_count()
            self.analyze_data[horce_id][data_name.escape_limb_count] = escape_limb_count
            self.analyze_data[horce_id][data_name.escape_limb1_count] = escape_limb1_count
            self.analyze_data[horce_id][data_name.escape_limb2_count] = escape_limb2_count
            self.analyze_data[horce_id][data_name.escape_within_rank] = escape_within_rank
            self.analyze_data[horce_id][data_name.father_rank] = father_rank
            self.analyze_data[horce_id][data_name.flame_evaluation_one] = flame_evaluation_one
            self.analyze_data[horce_id][data_name.flame_evaluation_two] = flame_evaluation_two
            self.analyze_data[horce_id][data_name.flame_evaluation_three] = flame_evaluation_three
            self.analyze_data[horce_id][data_name.foot_used_best] = self.race_type.best_foot_used( cd, pd )
            self.analyze_data[horce_id][data_name.high_level_score] = self.race_high_level.data_get( cd, pd, ymd )
            self.analyze_data[horce_id][data_name.horce_num] = horce_num
            self.analyze_data[horce_id][data_name.horce_sex] = horce_sex
            self.analyze_data[horce_id][data_name.horce_sex_month] = horce_sex_month
            self.analyze_data[horce_id][data_name.jockey_rank] = self.jockey_data.rank( race_id, horce_id )
            self.analyze_data[horce_id][data_name.jockey_year_rank] = \
              self.jockey_data.year_rank( race_id, horce_id, key_before_year )
            self.analyze_data[horce_id][data_name.kind] = cd.race_kind()
            self.analyze_data[horce_id][data_name.limb] = limb_math
            self.analyze_data[horce_id][data_name.limb_horce_number] = int( limb_math * 100 + int( cd.horce_number() / 2 ) )
            self.analyze_data[horce_id][data_name.max_past_ave_first_horce_body] = \
              current_race_data[STR_MAX+data_name.past_ave_first_horce_body] - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_ave_last_horce_body] = \
              current_race_data[STR_MAX+data_name.past_ave_last_horce_body] - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_max_first_horce_body] = \
              current_race_data[STR_MAX+data_name.past_max_first_horce_body] - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_max_last_horce_body] = \
              current_race_data[STR_MAX+data_name.past_max_last_horce_body] - current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_min_first_horce_body] = \
              current_race_data[STR_MAX+data_name.past_min_first_horce_body] - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.max_past_min_last_horce_body] = \
              current_race_data[STR_MAX+data_name.past_min_last_horce_body] - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.max_speed_index] = \
              current_race_data[STR_MAX+data_name.speed_index] - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.max_up_rate] = \
              current_race_data[STR_MAX+data_name.up_rate] - current_race_data[data_name.up_rate][i]
            self.analyze_data[horce_id][data_name.min_past_ave_first_horce_body] = \
              current_race_data[STR_MIN+data_name.past_ave_first_horce_body] - current_race_data[data_name.past_ave_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_ave_last_horce_body] = \
              current_race_data[STR_MIN+data_name.past_ave_last_horce_body] - current_race_data[data_name.past_ave_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_max_first_horce_body] = \
              current_race_data[STR_MIN+data_name.past_max_first_horce_body] - current_race_data[data_name.past_max_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_max_last_horce_body] = \
              current_race_data[STR_MIN+data_name.past_max_last_horce_body] - current_race_data[data_name.past_max_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_min_first_horce_body] = \
              current_race_data[STR_MIN+data_name.past_min_first_horce_body] - current_race_data[data_name.past_min_first_horce_body][i]
            self.analyze_data[horce_id][data_name.min_past_min_last_horce_body] = \
              current_race_data[STR_MIN+data_name.past_min_last_horce_body] - current_race_data[data_name.past_min_last_horce_body][i]
            self.analyze_data[horce_id][data_name.min_race_horce_first_passing_true_skill] = \
              current_race_data[STR_MIN+data_name.horce_first_passing_true_skill] - current_race_data[data_name.horce_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_horce_true_skill] = \
              current_race_data[STR_MIN+data_name.horce_true_skill] - current_race_data[data_name.horce_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_jockey_first_passing_true_skill] = \
              current_race_data[STR_MIN+data_name.jockey_first_passing_true_skill] - current_race_data[data_name.jockey_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_jockey_true_skill] = \
              current_race_data[STR_MIN+data_name.jockey_true_skill] - current_race_data[data_name.jockey_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_trainer_first_passing_true_skill] = \
              current_race_data[STR_MIN+data_name.trainer_first_passing_true_skill] - current_race_data[data_name.trainer_first_passing_true_skill][i]
            self.analyze_data[horce_id][data_name.min_race_trainer_true_skill] = \
              current_race_data[STR_MIN+data_name.trainer_true_skill] - current_race_data[data_name.trainer_true_skill][i]
            self.analyze_data[horce_id][data_name.min_speed_index] = \
              current_race_data[STR_MIN+data_name.speed_index] - current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.min_up3] = pd.min_up3()
            self.analyze_data[horce_id][data_name.min_up_rate] = \
              current_race_data[STR_MIN+data_name.up_rate] - current_race_data[data_name.up_rate][i]
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
            self.analyze_data[horce_id][data_name.place] = cd.place()
            self.analyze_data[horce_id][data_name.popular] = cd.popular()
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
            self.analyze_data[horce_id][data_name.predict_up3_stand] = None
            self.analyze_data[horce_id][data_name.predict_rough_rate] = None
            self.analyze_data[horce_id][data_name.race_interval] = min( max( pd.race_interval(), 0 ), 20 )
            self.analyze_data[horce_id][data_name.race_num] = cd.race_num()
            self.analyze_data[horce_id][data_name.ave_race_speed_index] = current_race_data[data_name.ave_race_speed_index]
            self.analyze_data[horce_id][data_name.min_race_speed_index] = current_race_data[data_name.min_race_speed_index]
            self.analyze_data[horce_id][data_name.max_race_speed_index] = current_race_data[data_name.max_race_speed_index]
            self.analyze_data[horce_id][data_name.speed_index] = current_race_data[data_name.speed_index][i]
            self.analyze_data[horce_id][data_name.speed_index_index] = \
              current_race_data[data_name.speed_index_index].index( current_race_data[data_name.speed_index][i] )
            self.analyze_data[horce_id][data_name.speed_index_stand] = current_race_data[data_name.speed_index_stand][i]
            self.analyze_data[horce_id][data_name.up_index] = current_race_data[data_name.up_index][i]
            self.analyze_data[horce_id][data_name.up_index_index] = \
              current_race_data[data_name.up_index_index].index( current_race_data[data_name.up_index][i] )
            self.analyze_data[horce_id][data_name.up_index_stand] = current_race_data[data_name.up_index_stand][i]
            self.analyze_data[horce_id][data_name.std_speed_index] = current_race_data[data_name.std_speed_index]
            self.analyze_data[horce_id][data_name.straight_slope] = self.race_type.stright_slope( cd, pd )
            self.analyze_data[horce_id][data_name.three_average] = pd.three_average()
            self.analyze_data[horce_id][data_name.three_difference] = pd.three_difference()
            self.analyze_data[horce_id][data_name.three_popular_limb] = three_popular_limb
            self.analyze_data[horce_id][data_name.three_popular_odds] = three_popular_odds
            self.analyze_data[horce_id][data_name.three_rate] = pd.three_rate()
            self.analyze_data[horce_id][data_name.trainer_rank] = \
              self.trainer_data.rank( race_id, \
                                     horce_id, \
                                     race_info = race_info, \
                                     trainer_id = self.storage.current_horce_data[horce_id].trainer_id )
            self.analyze_data[horce_id][data_name.two_popular_limb] = two_popular_limb
            self.analyze_data[horce_id][data_name.two_popular_odds] = two_popular_odds
            self.analyze_data[horce_id][data_name.two_rate] = pd.two_rate()
            self.analyze_data[horce_id][data_name.waku_three_rate] = \
              lib.kind_score_get( self.waku_three_rate_data, self.waku_three_key_list, kind_key_data, str( int( waku ) ) )
            self.analyze_data[horce_id][data_name.weather] = cd.weather()
            self.analyze_data[horce_id][data_name.weight] = cd.weight() / 10
            self.analyze_data[horce_id][data_name.predict_netkeiba_pace] = self.storage.predict_netkeiba_pace
            self.analyze_data[horce_id][data_name.predict_netkeiba_deployment] = predict_netkeiba_deployment
            self.analyze_data[horce_id][data_name.male_count] = male_count
            self.analyze_data[horce_id][data_name.female_count] = female_count

            str_index = "_index"

            for data_key in current_race_data.keys():
                if data_key in self.analyze_data[horce_id]:
                    continue

                for math_name in [ STR_AVE, STR_MAX, STR_MIN ]:
                    if ( math_name in data_key ) and not "race_" in data_key:
                        name = data_key.replace( math_name, "" )
                        
                        try:
                            current_race_data[data_key] = \
                              current_race_data[math_name+"race_"+name] - current_race_data[name][i]
                            break
                        except:
                            pass

                if data_key in self.analyze_data[horce_id]:
                    continue
                        
                if str_index in data_key:
                    name = data_key.replace( str_index, "" )

                    if name in current_race_data and not len( current_race_data[name] ) == 0:
                        self.analyze_data[horce_id][data_key] = \
                          current_race_data[data_key].index( current_race_data[name][i] )
                else:
                    if not type( current_race_data[data_key] ) is list:
                        self.analyze_data[horce_id][data_key] = current_race_data[data_key]
                    elif not len( current_race_data[data_key] ) == 0:
                        self.analyze_data[horce_id][data_key] = current_race_data[data_key][i]
