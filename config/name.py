import datetime

class Name:
    def __init__( self ):
        self.before_rank = "before_rank"
        self.before_rank_minus = "before_rank_minus"
        self.race_level_check = "race_level_check"
        self.race_level_check_minus = "race_level_check_minus"
        self.straight_slope = "straight_slope"
        self.straight_slope_minus = "straight_slope_minus"
        self.foot_used = "foot_used"
        self.foot_used_minus = "foot_used_minus"
        self.limb = "limb"
        self.limb_minus = "limb_minus"
        self.age = "age"
        self.age_minus = "age_minus"
        self.speed_index = "speed_index"
        self.speed_index_minus = "speed_index_minus"
        self.race_interval = "race_interval"
        self.race_interval_minus = "race_interval_minus"
        self.weight = "weight"
        self.weight_minus = "weight_minus"
        self.before_id_weight = "before_id_weight"
        self.before_id_weight_minus = "before_id_weight_minus"
        self.omega = "omega"
        self.omega_minus = "omega_minus"
        self.before_speed = "before_speed"
        self.before_speed_minus = "before_speed_minus"
        self.popular = "popular"
        self.popular_minus = "popular_minus"
        self.trainer_rank = "trainer_rank"
        self.trainer_rank_minus = "trainer_rank_minus"
        self.jockey_rank = "jockey_rank"
        self.jockey_rank_minus = "jockey_rank_minus"
        self.before_diff = "before_diff"
        self.before_diff_minus = "before_diff_minus"
        self.limb_horce_number = "limb_horce_number"
        self.limb_horce_number_minus = "limb_horce_number_minus"
        self.mother_rank = "mother_rank"
        self.mother_rank_minus = "mother_rank_minus"
        self.match_rank = "match_rank"
        self.match_rank_minus = "match_rank_minus"
        self.weather = "weather"
        self.weather_minus = "weather_minus"
        self.burden_weight = "burden_weight"
        self.burden_weight_minus = "burden_weight_minus"
        self.before_continue_not_three_rank = "before_continue_not_three_rank"
        self.before_continue_not_three_rank_minus = "before_continue_not_three_rank_minus"
        self.horce_sex = "horce_sex"
        self.horce_sex_minus = "horce_sex_minus"
        self.horce_sex_month = "horce_sex_month"
        self.horce_sex_month_minus = "horce_sex_month_minus"
        self.dist_kind_count = "dist_kind_count"
        self.dist_kind_count_minus = "dist_kind_count_minus"
        self.before_popular = "before_popular"
        self.before_popular_minus = "before_popular_minus"
        self.before_last_passing_rank = "before_last_passing_rank"
        self.before_last_passing_rank_minus = "before_last_passing_rank_minus"
        self.before_first_passing_rank = "before_first_passing_rank"
        self.before_first_passing_rank_minus = "before_first_passing_rank_minus"
        self.jockey_year_rank = "jockey_year_rank"
        self.jockey_year_rank_minus = "jockey_year_rank_minus"
        self.money = "money"
        self.money_minus = "money_minus"
        self.horce_num = "horce_num"
        self.horce_num_minus = "horce_num_minus"
        self.baba = "baba"
        self.baba_minus = "baba_minus"
        self.place = "place"
        self.place_minus = "place_minus"
        self.popular_rank = "popular_rank"
        self.popular_rank_minus = "popular_rank_minus"
        self.train_score = "train_score"
        self.train_score_minus = "train_score_minus"
        self.race_deployment = "race_deployment"
        self.race_deployment_minus = "race_deployment_minus"
        self.up3_standard_value = "up3_standard_value"
        self.up3_standard_value_minus = "up3_standard_value_minus"
        self.my_limb_count = "my_limb_count"
        self.my_limb_count_minus = "my_limb_count_minus"
        self.true_skill = "true_skill"
        self.true_skill_minus = "true_skill_minus"
        self.stock_name = self.stock_name_create()

    def stock_name_create( self ):
        today = datetime.date.today()
        year = str( int( today.year ) )
        month = str( int( today.month ) )
        day = str( int( today.day ) )

        if len( month ) == 1:
            month = "0" + month

        if len( day ) == 1:
            day = "0" + day

        stock_name = year + month + day + "_stock.pickle"
        return stock_name
