import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

from config import data_name
from config import pickle_name
from config import sekitoba_dir

from data_manage import Storage
from SekitobaDataCreate.win_rate import WinRate
from SekitobaDataCreate.time_index_get import TimeIndexGet
from SekitobaDataCreate.before_race_score_get import BeforeRaceScore
from SekitobaDataCreate.train_index_get import TrainIndexGet
from SekitobaDataCreate.race_type import RaceType
from SekitobaDataCreate.high_level_data_get import RaceHighLevel
from SekitobaDataCreate.jockey_data_get import JockeyAnalyze
from SekitobaDataCreate.trainer_data_get import TrainerAnalyze
from SekitobaDataCreate.stride_ablity import StrideAblity
from SekitobaDataCreate.last_wrap import LastWrap
from SekitobaDataCreate.get_horce_data import GetHorceData
from SekitobaDataCreate.odds_cluster import OddsCluster
from SekitobaDataCreate.kinetic_energy import KineticEnergy
from SekitobaDataCreate.blood_type_score import BloodTypeScore

STR_AVE = "ave_"
STR_MAX = "max_"
STR_MIN = "min_"
STR_STD = "std_"
STR_INDEX = "index_"
STAND_INDEX = "stand_"

dm.dl.file_set( "race_cource_info.pickle" )

class DataCreate:
    def __init__( self, storage: Storage ):
        self.storage: Storage = storage
        self.analyze_data = {}
        self.pace_name = "pace"
        self.waku_three_key_list = [ "place", "dist", "limb", "baba", "kind" ]
        self.score_key_list = []

        self.race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )

        self.race_data = ps.RaceData()
        self.race_horce_data = ps.RaceHorceData()
        self.horce_data = ps.HorceData()
        self.parent_data = ps.HorceData()
        self.jockey_data = ps.JockeyData()
        self.trainer_data = ps.TrainerData()
        self.prod_data = ps.ProdData()

        self.win_rate = WinRate( self.race_data, self.prod_data )
        self.time_index = TimeIndexGet( self.horce_data )
        self.before_race_score = BeforeRaceScore( self.race_data )
        self.train_index = TrainIndexGet()
        self.race_type = RaceType()
        self.race_high_level = RaceHighLevel()
        self.jockey_analyze = JockeyAnalyze( self.race_data, self.race_horce_data, self.jockey_data )
        self.trainer_analyze = TrainerAnalyze( self.race_data, self.race_horce_data, self.trainer_data )
        self.stride_ablity = StrideAblity( self.race_data )
        self.train_index.train_time_data.update( { self.storage.today_data.race_id: self.train_data_create() } )
        self.race_type.set_race_money( { self.storage.today_data.race_id: self.storage.race_money } )
        self.last_wrap = LastWrap( self.race_data, self.horce_data, self.race_horce_data )
        self.kinetic_energy = KineticEnergy( self.race_data )
        self.blood_type_score = BloodTypeScore( self.race_data, self.horce_data )

        self.readScoreFile( sekitoba_dir + "/data/score_data_name.txt" )
        self.readScoreFile( sekitoba_dir + "/data/add_score_data_name.txt" )


    def readScoreFile( self, fileName ):
        f = open( fileName )
        all_data = f.readlines()
        f.close()

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
        current_race_data = [ '' ] * 22
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

    def match_rankScore( self, cd: lib.CurrentData, target_id ):
        target_past_data = self.horce_data.get_past_data( target_id )
        target_pd = lib.PastData( target_past_data, [], self.race_data )
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

    def prod_flame_evaluation( self, data ):
        result = {}
    
        for race_place_num in data.keys():
            result[race_place_num] = {}
            for day in data[race_place_num].keys():
                result[race_place_num][day] = {}
                for flame_number in data[race_place_num][day].keys():
                    result[race_place_num][day][flame_number] = {}
                    result[race_place_num][day][flame_number]["one"] = \
                    data[race_place_num][day][flame_number]["one"] / data[race_place_num][day][flame_number]["count"]
                    result[race_place_num][day][flame_number]["two"] = \
                    data[race_place_num][day][flame_number]["two"] / data[race_place_num][day][flame_number]["count"]
                    result[race_place_num][day][flame_number]["three"] = \
                    data[race_place_num][day][flame_number]["three"] / data[race_place_num][day][flame_number]["count"]
                    
        return result
    
    def create( self ):
        race_id = self.storage.today_data.race_id
        self.prod_data.get_all_data()
        self.horce_data.get_multi_data( self.storage.horce_id_list )
        self.jockey_data.get_multi_data( self.storage.jockey_id_list )
        self.trainer_data.get_multi_data( self.storage.trainer_id_list )
        self.race_horce_data.horce_id_list = self.storage.horce_id_list

        for horce_id in self.storage.horce_id_list:
            self.race_horce_data.data[horce_id] = {}
            self.race_horce_data.data[horce_id]["jockey_id"] = self.storage.current_horce_data[horce_id].jockey_id
            self.race_horce_data.data[horce_id]["trainer_id"] = self.storage.current_horce_data[horce_id].trainer_id

        self.race_data.data["year"] = self.storage.today_data.race_date.year
        self.race_data.data["month"] = self.storage.today_data.race_date.month
        self.race_data.data["day"] = self.storage.today_data.race_date.day
        self.race_data.data["out_side"] = self.storage.outside
        self.race_data.data["first_up3_halon"] = self.storage.first_up3
        self.race_data.data["stride_ablity_analyze"] = self.prod_data.data["stride_ablity_analyze"]
        self.race_data.data["waku_three_rate"] = self.prod_data.data["waku_three_rate"]
        self.race_data.data["dist_index"] = self.prod_data.data["dist_index"]
        self.race_data.data["standard_time"] = self.prod_data.data["standard_time"]
        self.race_data.data["up3_standard_time"] = self.prod_data.data["up3_standard_time"]
        self.race_data.data["race_time_analyze"] = self.prod_data.data["race_time_analyze"]

        # Memo; 以下はsekitoba_updateで追加が必要
        self.race_data.data["before_pace"] = self.prod_data.data["before_pace"]
        self.race_data.data["up3_analyze"] = self.prod_data.data["up3_analyze"]
        self.race_data.data["waku_three_rate"] = self.prod_data.data["waku_three_rate"]
        self.race_data.data["blood_type_score"] = self.prod_data.data["blood_type_score"]
        self.race_data.data["blood_type"] = self.storage.blood_type_data
        self.race_data.data["flame_evaluation"] = self.prod_flame_evaluation( self.prod_data.data["flame_evaluation"] )
        
        today_data = { "year": self.storage.today_data.race_date.year, \
                      "month": self.storage.today_data.race_date.month, \
                      "day": self.storage.today_data.race_date.day }
        str_year = str( self.storage.today_data.year )
        str_day = str( self.storage.today_data.day )
        str_num = str( self.storage.today_data.num )
        str_place_num = str( self.storage.today_data.place_num )
        key_money_class = str( int( lib.money_class_get( self.storage.race_money ) ) )
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
        horce_odds_list = []

        for horce_id in self.storage.horce_id_list:
            if horce_id in self.storage.cansel_horce_id_list:
                continue

            current_data = self.current_data_create( horce_id )
            try:
                current_data = self.current_data_create( horce_id )
            except:
                continue

            past_data = []

            if horce_id in self.horce_data.data:
                _, past_data = lib.race_check( self.horce_data.data[horce_id]["past_data"], today_data )

            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, self.race_data )
            getHorceData = GetHorceData( cd, pd )
            pd.set_up3_analyze_data( self.prod_data.data["up3_analyze"] )
            self.race_data.data["dist"] = int( cd.dist() * 1000 )
            self.race_data.data["kind"] = cd.race_kind()
            self.race_data.data["baba"] = cd.baba_status()
            self.race_data.data["place"] = cd.place()

            before_cd = pd.before_cd()
            horce_num = cd.horce_number()
            popular = cd.popular()
            odds = cd.odds()
            limb_math = lib.limb_search( pd )
            key_limb = str( int( limb_math ) )
            jockey_id = self.storage.current_horce_data[horce_id].jockey_id
            trainer_id = self.storage.current_horce_data[horce_id].trainer_id
            escape_within_rank = -1

            before_diff = getHorceData.getBeforeDiff()
            before_first_last_diff = getHorceData.getBeforeFirstLastDiff()
            before_id_weight = getHorceData.getBeforeIdWeight()
            before_popular = getHorceData.getBeforePopular()
            before_rank = getHorceData.getBeforeRank()
            before_speed = getHorceData.getBeforeSpeed()
            popular_rank = getHorceData.getPopularRank()
            diff_load_weight = getHorceData.getDiffLoadWeight()
            before_first_passing_rank, before_last_passing_rank  = getHorceData.getBeforePassingRank()
            up3_standard_value = getHorceData.getUp3StandardValue()            
            before_race_score = self.before_race_score.score_get( horce_id, getHorceData )

            if self.storage.current_horce_data[horce_id].sex == 0:
                male_count += 1
            elif self.storage.current_horce_data[horce_id].sex == 1:
                female_count += 1

            if getHorceData.limb_math == 1:
                escape_limb1_count += 1
            elif getHorceData.limb_math == 2:
                escape_limb2_count += 1
            
            if getHorceData.limb_math == 1 or getHorceData.limb_math == 2:
                escape_limb_count += 1
                escape_within_rank = horce_num
            elif getHorceData.limb_math == 3 or getHorceData.limb_math == 4:
                insert_limb_count += 1

            lib.dic_append( my_limb_count, getHorceData.limb_math, 0 )
            my_limb_count[getHorceData.limb_math] += 1

            if popular == 1:
                one_popular_odds = odds
                one_popular_limb = getHorceData.limb_math
            elif popular == 2:
                two_popular_odds = odds
                two_popular_limb = getHorceData.limb_math
            elif popular == 3:
                three_popular_limb = getHorceData.limb_math
                three_popular_odds = odds

            past_min_first_horce_body, past_max_first_horce_body, past_ave_first_horce_body, past_std_first_horce_body = \
              getHorceData.getFirstHorceBody()
            past_min_last_horce_body, past_max_last_horce_body, past_ave_last_horce_body, past_std_last_horce_body = \
              getHorceData.getLastHorceBody()

            horce_true_skill = 25
            jockey_true_skill = 25
            trainer_true_skill = 25
            horce_first_passing_true_skill = 25
            jockey_first_passing_true_skill = 25
            trainer_first_passing_true_skill = 25
            horce_last_passing_true_skill = 25
            jockey_last_passing_true_skill = 25
            trainer_last_passing_true_skill = 25
            up3_horce_true_skill = 25
            up3_jockey_true_skill = 25
            up3_trainer_true_skill = 25
            corner_true_skill = 25
            speed = []
            up_speed = []
            pace_speed = []

            if horce_id in self.horce_data.data:
                horce_true_skill = self.horce_data.data[horce_id]["true_skill"]
                horce_first_passing_true_skill = self.horce_data.data[horce_id]["first_passing_true_skill"]
                horce_last_passing_true_skill = self.horce_data.data[horce_id]["last_passing_true_skill"]
                up3_horce_true_skill = self.horce_data.data[horce_id]["up3_true_skill"]
                corner_true_skill = self.horce_data.data[horce_id]["corner_true_skill"]
                speed, up_speed, pace_speed = pd.speed_index( self.horce_data.data[horce_id]["baba_index"] )

            if jockey_id in self.jockey_data.data:
                jockey_true_skill = self.jockey_data.data[jockey_id]["true_skill"]
                jockey_first_passing_true_skill = self.jockey_data.data[jockey_id]["first_passing_true_skill"]
                jockey_last_passing_true_skill = self.jockey_data.data[jockey_id]["last_passing_true_skill"]
                up3_jockey_true_skill = self.jockey_data.data[jockey_id]["up3_true_skill"]

            if trainer_id in self.trainer_data.data:
                trainer_true_skill = self.trainer_data.data[trainer_id]["true_skill"]
                trainer_first_passing_true_skill = self.trainer_data.data[trainer_id]["first_passing_true_skill"]
                trainer_last_passing_true_skill = self.trainer_data.data[trainer_id]["last_passing_true_skill"]
                up3_trainer_true_skill = self.trainer_data.data[trainer_id]["up3_true_skill"]
                
            current_time_index = self.time_index.main( horce_id, pd.past_day_list() )
            stride_ablity_data = self.stride_ablity.ablity_create( cd, pd )
            pace_up_rate = pd.pace_up_rate()

            for stride_data_key in stride_ablity_data.keys():
                current_race_data[stride_data_key].append( stride_ablity_data[stride_data_key] )

            first_wrap = self.train_index.first_wrap( race_id, horce_num )
            final_wrap = self.train_index.final_wrap( race_id, cd.horce_number() )
            train_time_slope, train_time_slice = self.train_index.train_time_slope_slice( race_id, horce_num )
            wrap_slope, wrap_slice = self.train_index.wrap_slope_slice( race_id, horce_num )
            wrap_diff = first_wrap - final_wrap

            horce_first_up3_halon = {}
            race_first_up3_ave = -1000
            race_first_up3_min = -1000
            race_first_up3_max = -1000

            try:
                horce_first_up3_halon = self.race_data.data["first_up3_halon"][str(int(cd.horce_number()))]
            except:
                pass
            
            if not len( horce_first_up3_halon ) == 0:
                race_first_up3_ave = 0
                race_first_up3_min = 1000
                race_first_up3_max = -1000
                
                for k in horce_first_up3_halon.keys():
                    race_first_up3_ave += horce_first_up3_halon[k]
                    race_first_up3_min = min( race_first_up3_min, horce_first_up3_halon[k] )
                    race_first_up3_max = max( race_first_up3_max, horce_first_up3_halon[k] )

                race_first_up3_ave /= len( horce_first_up3_halon )
                
            judgment_key_data = {}
            judgment_key_data["limb"] = str( int( limb_math ) )
            judgment_key_data["popular"] = str( int( cd.popular() ) )
            judgment_key_data["flame_num"] = str( int( cd.flame_number() ) )
            judgment_key_data["dist"] = str( int( cd.dist_kind() ) )
            judgment_key_data["kind"] = str( int( cd.race_kind() ) )
            judgment_key_data["baba"] = str( int( cd.baba_status() ) )
            judgment_key_data["place"] = str( int( cd.place()) )
            judgment_rate_key_list = [ "0", "1", "2" ]

            for judgment_key in judgment_key_data:
                jockey_judge_key = "jockey_judgment_{}".format( judgment_key )
                jockey_judge_up3_key = "jockey_judgment_up3_{}".format( judgment_key )
                trainer_judge_key = "trainer_judgment_{}".format( judgment_key )
                trainer_judge_up3_key = "trainer_judgment_up3_{}".format( judgment_key )
                judge_value_key = judgment_key_data[judgment_key]

                if jockey_judge_key in current_race_data:
                    try:
                        current_race_data[jockey_judge_key].append( \
                            self.jockey_data.data[jockey_id]["jockey_judgment"][judgment_key][judge_value_key] )
                    except:
                        current_race_data[jockey_judge_key].append( lib.escapeValue )

                if jockey_judge_up3_key in current_race_data:
                    try:
                        current_race_data[jockey_judge_up3_key].append( \
                            self.jockey_data.data[jockey_id]["jockey_judgment_up3"][judgment_key][judge_value_key] )
                    except:
                        current_race_data[jockey_judge_up3_key].append( lib.escapeValue )

                if trainer_judge_key in current_race_data:
                    try:
                        current_race_data[trainer_judge_key].append( \
                            self.trainer_data.data[trainer_id]["trainer_judgment"][judgment_key][judge_value_key] )
                    except:
                        current_race_data[trainer_judge_key].append( lib.escapeValue )

                if trainer_judge_up3_key in current_race_data:
                    try:
                        current_race_data[trainer_judge_up3_key].append( \
                            self.trainer_data.data[trainer_id]["trainer_judgment_up3"][judgment_key][judge_value_key] )
                    except:
                        current_race_data[trainer_judge_up3_key].append( lib.escapeValue )

            for judgment_key in judgment_key_data:
                judge_value_key = judgment_key_data[judgment_key]
                
                for rk in judgment_rate_key_list:
                    jockey_judge_rate_key = "jockey_judgment_rate_{}_{}".format( judgment_key, rk  )
                    jockey_judge_up3_rate_key = "jockey_judgment_up3_rate_{}_{}".format( judgment_key, rk  )

                    if jockey_judge_rate_key in current_race_data:
                        try:
                            current_race_data[jockey_judge_rate_key].append( \
                                self.jockey_data.data[jockey_id]["jockey_judgment_rate"][judgment_key][judge_value_key][rk] )
                        except:
                            current_race_data[jockey_judge_rate_key].append( lib.escapeValue )

                    if jockey_judge_up3_rate_key in current_race_data:
                        try:
                            current_race_data[jockey_judge_up3_rate_key].append( \
                                self.jockey_data.data[jockey_id]["jockey_judgment_up3_rate"][judgment_key][judge_value_key][rk] )
                        except:
                            current_race_data[jockey_judge_up3_rate_key].append( lib.escapeValue )

            current_race_data[data_name.age].append( int( str_year ) - int( horce_id[0:4] ) )
            current_race_data[data_name.before_diff].append( before_diff )
            current_race_data[data_name.before_first_passing_rank].append( before_first_passing_rank )
            current_race_data[data_name.before_id_weight].append( before_id_weight )
            current_race_data[data_name.before_last_passing_rank].append( before_last_passing_rank )
            current_race_data[data_name.before_popular].append( before_popular )
            current_race_data[data_name.before_race_score].append( before_race_score )
            current_race_data[data_name.before_rank].append( before_rank )
            current_race_data[data_name.before_speed].append( before_speed )
            current_race_data[data_name.before_first_last_diff].append( before_first_last_diff )
            current_race_data[data_name.best_dist].append( pd.best_dist() )
            current_race_data[data_name.best_first_passing_rank].append( pd.best_first_passing_rank() )
            current_race_data[data_name.best_second_passing_rank].append( pd.best_second_passing_rank() )
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
            current_race_data[data_name.up_rate].append( pd.up_rate( key_money_class, self.prod_data.data["up_kind_ave"] ) )
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
            current_race_data[data_name.level_score].append( pd.level_score( self.prod_data.data["money_class_true_skill"] ) )
            current_race_data[data_name.min_up3].append( pd.min_up3() )
            current_race_data[data_name.up_index].append( lib.max_check( up_speed ) )
            current_race_data[data_name.up_speed_index].append( lib.max_check( up_speed ) )
            current_race_data[data_name.pace_speed_index].append( lib.max_check( pace_speed ) )
            current_race_data[data_name.match_rank].append( pd.match_rank() )
            current_race_data[data_name.match_up3].append( pd.match_up3() )
            current_race_data[data_name.max_time_point].append( pd.max_time_point( self.prod_data.data["race_time_analyze"] ) )
            current_race_data[data_name.max_up3].append( pd.max_up3() )
            current_race_data[data_name.max_up3_time_point].append( pd.max_up3TimePoint( str( int( limb_math ) ) ) )
            current_race_data[data_name.level_up3].append( pd.level_up3( self.prod_data.data["money_class_true_skill"] ) )
            current_race_data[data_name.stamina].append( pd.stamina_create( key_limb) )
            current_race_data[data_name.first_up3_ave].append( race_first_up3_ave )
            current_race_data[data_name.first_up3_min].append( race_first_up3_min )
            current_race_data[data_name.first_up3_max].append( race_first_up3_max )
            current_race_data[data_name.kinetic_energy].append( self.kinetic_energy.create( cd, pd ) )
            current_race_data[data_name.run_circle_speed].append( pd.run_circle_speed() )
            current_race_data[data_name.blood_type_score].append(
                self.blood_type_score.score_get( horce_id, cd, pd, getHorceData, sex = self.storage.current_horce_data[horce_id].sex ) )
            horce_odds_list.append( { "horce_id": horce_id, "odds": odds } )

            #for pace_up_rate_key in pace_up_rate.keys():
            #    current_race_data["pace_up_rate_"+pace_up_rate_key].append( pace_up_rate[pace_up_rate_key] )

            horce_id_list.append( horce_id )

        N = len( horce_id_list )

        if N == 0:
            return False

        self.last_wrap.create_score()
        current_key_list = []

        for data_key in current_race_data.keys():
            if not type( current_race_data[data_key] ) is list or \
              len( current_race_data[data_key] ) == 0:
                continue

            current_key_list.append( data_key )

        for data_key in current_key_list:
            current_race_data["race_"+data_key] = current_race_data[data_key]
            current_race_data[data_key+"_index"] = sorted( current_race_data[data_key], reverse = True )
            current_race_data[data_key+"_stand"] = lib.standardization( current_race_data[data_key] )
            current_race_data[data_key+"_devi"] = lib.deviation_value( current_race_data[data_key] )
            current_race_data["ave_"+data_key] = lib.average( current_race_data[data_key] )
            current_race_data["max_"+data_key] = max( current_race_data[data_key] )
            current_race_data["min_"+data_key] = lib.minimum( current_race_data[data_key] )
            current_race_data["std_"+data_key] = lib.stdev( current_race_data[data_key] )
            current_race_data["ave_race_"+data_key] = lib.average( current_race_data[data_key] )
            current_race_data["max_race_"+data_key] = max( current_race_data[data_key] )
            current_race_data["min_race_"+data_key] = lib.minimum( current_race_data[data_key] )
            current_race_data["std_race_"+data_key] = lib.stdev( current_race_data[data_key] )
            current_race_data["max_stand_race_"+data_key] = max( lib.standardization( current_race_data[data_key] ) )

        for i, horce_id in enumerate( horce_id_list ):
            if horce_id in self.storage.cansel_horce_id_list:
                continue

            try:
                current_data = self.current_data_create( horce_id )
            except:
                continue

            past_data = []

            if horce_id in self.horce_data.data:
                _, past_data = lib.race_check( self.horce_data.data[horce_id]["past_data"], today_data )

            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, self.race_data )
            pd.set_up3_analyze_data( self.prod_data.data["up3_analyze"] )
            getHorceData = GetHorceData( cd, pd )

            limb_math = lib.limb_search( pd )
            horce_num = cd.horce_number()
            key_before_year = str( int( int( str_year ) - 1 ) )
            horce_sex = self.storage.current_horce_data[horce_id].sex
            #horce_sex_month = int( self.storage.today_data.race_date.month * 10 + horce_sex )
            escape_within_rank = -1

            if limb_math == 1 or limb_math == 2:
                escape_within_rank = current_race_data[data_name.escape_within_rank+"_index"].index( int( cd.horce_number() ) )

            predict_netkeiba_deployment = -1

            for t in range( 0, len( self.storage.predict_netkeiba_deployment ) ):
                if int( horce_num ) in self.storage.predict_netkeiba_deployment[t]:
                    predict_netkeiba_deployment = t
                    break

            flame_evaluation_one, flame_evaluation_two, flame_evaluation_three = \
              getHorceData.getFlameEvaluation( self.prod_data.data["flame_evaluation"] )

            first_straight_dist, last_straight_dist = \
              getHorceData.getStraightDist( self.race_cource_info )

            win_rate_data = self.win_rate.data_get( limb_math, cd )
            cluster_data = [0] * 4
            oddsCluster = OddsCluster( horce_odds_list )
            oddsCluster.clustering()

            for cl in oddsCluster.cluster.values():
                cluster_data[int(cl-1)] += 1

            self.analyze_data[horce_id] = {}
            self.analyze_data[horce_id][data_name.odds_cluster_1] = cluster_data[0]
            self.analyze_data[horce_id][data_name.odds_cluster_2] = cluster_data[1]
            self.analyze_data[horce_id][data_name.odds_cluster_3] = cluster_data[2]
            self.analyze_data[horce_id][data_name.odds_cluster_4] = cluster_data[3]

            self.analyze_data[horce_id][data_name.insert_limb_count] = insert_limb_count
            self.analyze_data[horce_id][data_name.all_horce_num] = cd.all_horce_num()
            self.analyze_data[horce_id][data_name.ave_burden_weight_diff] = \
              lib.minus( current_race_data[STR_AVE+"race_"+data_name.burden_weight], current_race_data[data_name.burden_weight][i] )
            self.analyze_data[horce_id][data_name.burden_weight] = current_race_data[data_name.burden_weight][i]
            self.analyze_data[horce_id][data_name.ave_first_last_diff] = pd.ave_first_last_diff()
            self.analyze_data[horce_id][data_name.ave_first_passing_rank] = pd.first_passing_rank()
            self.analyze_data[horce_id][data_name.ave_past_ave_first_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_ave_first_horce_body], current_race_data[data_name.past_ave_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_past_ave_last_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_ave_last_horce_body], current_race_data[data_name.past_ave_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_past_max_first_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_max_first_horce_body], current_race_data[data_name.past_max_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_past_max_last_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_max_last_horce_body], current_race_data[data_name.past_max_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_past_min_first_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_min_first_horce_body], current_race_data[data_name.past_min_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_past_min_last_horce_body] = \
              lib.minus( current_race_data[STR_AVE+data_name.past_min_last_horce_body], current_race_data[data_name.past_min_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.ave_speed_index] = \
              lib.minus( current_race_data[STR_AVE+data_name.speed_index], current_race_data[data_name.speed_index][i] )
            self.analyze_data[horce_id][data_name.std_speed_index] = current_race_data[data_name.std_speed_index]
            self.analyze_data[horce_id][data_name.std_race_speed_index] = current_race_data[data_name.std_race_speed_index]
            self.analyze_data[horce_id][data_name.max_stand_race_speed_index] = current_race_data[data_name.max_stand_race_speed_index]
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
            self.analyze_data[horce_id][data_name.flame_evaluation_one] = flame_evaluation_one
            self.analyze_data[horce_id][data_name.flame_evaluation_two] = flame_evaluation_two
            self.analyze_data[horce_id][data_name.flame_evaluation_three] = flame_evaluation_three
            self.analyze_data[horce_id][data_name.foot_used_best] = self.race_type.best_foot_used( cd, pd )
            self.analyze_data[horce_id][data_name.high_level_score] = self.race_high_level.data_get( cd, pd, today_data )
            self.analyze_data[horce_id][data_name.horce_num] = horce_num
            self.analyze_data[horce_id][data_name.horce_sex] = horce_sex
            #self.analyze_data[horce_id][data_name.horce_sex_month] = horce_sex_month
            self.analyze_data[horce_id][data_name.jockey_rank] = self.jockey_analyze.rank( race_id, horce_id )
            self.analyze_data[horce_id][data_name.jockey_year_rank] = self.jockey_analyze.year_rank( horce_id, key_before_year )
            self.analyze_data[horce_id][data_name.kind] = cd.race_kind()
            self.analyze_data[horce_id][data_name.limb] = limb_math
            #self.analyze_data[horce_id][data_name.limb_horce_number] = int( limb_math * 100 + int( cd.horce_number() / 2 ) )
            self.analyze_data[horce_id][data_name.max_past_ave_first_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_ave_first_horce_body], current_race_data[data_name.past_ave_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_past_ave_last_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_ave_last_horce_body], current_race_data[data_name.past_ave_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_past_max_first_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_max_first_horce_body], current_race_data[data_name.past_max_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_past_max_last_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_max_last_horce_body], current_race_data[data_name.past_max_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_past_min_first_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_min_first_horce_body], current_race_data[data_name.past_min_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_past_min_last_horce_body] = \
              lib.minus( current_race_data[STR_MAX+data_name.past_min_last_horce_body], current_race_data[data_name.past_min_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.max_speed_index] = \
              lib.minus( current_race_data[STR_MAX+data_name.speed_index], current_race_data[data_name.speed_index][i] )
            self.analyze_data[horce_id][data_name.max_up_rate] = \
              lib.minus( current_race_data[STR_MAX+data_name.up_rate], current_race_data[data_name.up_rate][i] )
            self.analyze_data[horce_id][data_name.min_past_ave_first_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_ave_first_horce_body], current_race_data[data_name.past_ave_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_past_ave_last_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_ave_last_horce_body], current_race_data[data_name.past_ave_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_past_max_first_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_max_first_horce_body], current_race_data[data_name.past_max_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_past_max_last_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_max_last_horce_body], current_race_data[data_name.past_max_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_past_min_first_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_min_first_horce_body], current_race_data[data_name.past_min_first_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_past_min_last_horce_body] = \
              lib.minus( current_race_data[STR_MIN+data_name.past_min_last_horce_body], current_race_data[data_name.past_min_last_horce_body][i] )
            self.analyze_data[horce_id][data_name.min_speed_index] = \
              lib.minus( current_race_data[STR_MIN+data_name.speed_index], current_race_data[data_name.speed_index][i] )
            self.analyze_data[horce_id][data_name.min_up3] = pd.min_up3()
            self.analyze_data[horce_id][data_name.money] = pd.get_money()
            self.analyze_data[horce_id][data_name.money_class] = lib.money_class_get( self.storage.race_money )
            self.analyze_data[horce_id][data_name.my_limb_count] = my_limb_count[limb_math]
            self.analyze_data[horce_id][data_name.odds] = cd.odds()
            self.analyze_data[horce_id][data_name.one_popular_odds] = one_popular_odds
            self.analyze_data[horce_id][data_name.one_popular_limb] = one_popular_limb
            self.analyze_data[horce_id][data_name.one_rate] = pd.one_rate()
            #self.analyze_data[horce_id][data_name.pace_up] = pd.pace_up_check( self.prod_data.data["up_pace_regressin"] )
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
            self.analyze_data[horce_id][data_name.predict_up3] = None
            self.analyze_data[horce_id][data_name.predict_up3_stand] = None
            self.analyze_data[horce_id][data_name.race_interval] = min( max( pd.race_interval(), 0 ), 20 )
            #self.analyze_data[horce_id][data_name.race_num] = cd.race_num()
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
            #self.analyze_data[horce_id][data_name.straight_slope] = self.race_type.stright_slope( cd, pd )
            self.analyze_data[horce_id][data_name.three_average] = pd.three_average()
            self.analyze_data[horce_id][data_name.three_difference] = pd.three_difference()
            self.analyze_data[horce_id][data_name.three_popular_limb] = three_popular_limb
            self.analyze_data[horce_id][data_name.three_popular_odds] = three_popular_odds
            self.analyze_data[horce_id][data_name.three_rate] = pd.three_rate()
            self.analyze_data[horce_id][data_name.trainer_rank] = self.trainer_analyze.rank( race_id, horce_id )
            self.analyze_data[horce_id][data_name.two_popular_limb] = two_popular_limb
            self.analyze_data[horce_id][data_name.two_popular_odds] = two_popular_odds
            self.analyze_data[horce_id][data_name.two_rate] = pd.two_rate()
            self.analyze_data[horce_id][data_name.waku_three_rate] = getHorceData.getKindScore( self.prod_data.data["waku_three_rate"] )
            self.analyze_data[horce_id][data_name.weather] = cd.weather()
            self.analyze_data[horce_id][data_name.weight] = cd.weight() / 10
            self.analyze_data[horce_id][data_name.predict_netkeiba_pace] = self.storage.predict_netkeiba_pace
            self.analyze_data[horce_id][data_name.predict_netkeiba_deployment] = predict_netkeiba_deployment
            self.analyze_data[horce_id][data_name.male_count] = male_count
            self.analyze_data[horce_id][data_name.female_count] = female_count
            self.analyze_data[horce_id][data_name.first_straight_dist] = first_straight_dist
            self.analyze_data[horce_id][data_name.last_straight_dist] = last_straight_dist

            for rk in win_rate_data.keys():
                self.analyze_data[horce_id][rk] = win_rate_data[rk] 

            for wrap_key in self.last_wrap.horce_wrap_score[horce_id].keys():
                self.analyze_data[horce_id][wrap_key] = self.last_wrap.horce_wrap_score[horce_id][wrap_key]

            self.analyze_data[horce_id].update( lib.pace_teacher_analyze( current_race_data, t_instance = self.analyze_data[horce_id] ) )
            self.analyze_data[horce_id].update( lib.horce_teacher_analyze( current_race_data, self.analyze_data[horce_id], i ) )

            for key in self.analyze_data[horce_id].keys():
                if not self.analyze_data[horce_id][key] == None:
                    self.analyze_data[horce_id][key] = round( self.analyze_data[horce_id][key], 3 )
