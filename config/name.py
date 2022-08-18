import datetime

class Name:
    def __init__( self ):
        self.before_rank = "before_rank"
        self.before_rank_minus = "before_rank_minus"
        self.race_level_check = "race_level_check"
        self.race_level_check_minus = "race_level_check_minus"
        self.straight_slope = "straight_slope"
        self.foot_used = "foot_used"
        self.limb = "limb"
        self.age = "age"
        self.speed_index = "speed_index"
        self.race_interval = "race_interval"
        self.weight = "weight"
        self.weight_minus = "weight_minus"
        self.before_id_weight = "before_id_weight"
        self.omega = "omega"
        self.before_speed_minus = "before_speed_minus"
        self.popular = "popular"
        self.popular_minus = "popular_minus"
        self.trainer_rank = "trainer_rank"
        self.trainer_rank_minus = "trainer_rank_minus"
        self.jockey_rank = "jockey_rank"
        self.jockey_rank_minus = "jockey_rank_minus"
        self.before_diff = "before_diff"
        self.limb_horce_number = "limb_horce_number"
        self.limb_horce_number_minus = "limb_horce_number_minus"
        self.mother_rank = "mother_rank"
        self.match_rank = "match_rank"
        self.match_rank_minus = "match_rank_minus"
        self.weather = "weather"
        self.burden_weight = "burden_weight"
        self.before_continue_not_three_rank = "before_continue_not_three_rank"
        self.before_continue_not_three_rank_minus = "before_continue_not_three_rank_minus"
        self.horce_sex = "horce_sex"
        self.horce_sex_month = "horce_sex_month"
        self.dist_kind_count_minus = "dist_kind_count_minus"
        self.before_popular = "before_popular"
        self.before_last_passing_rank = "before_last_passing_rank"
        self.before_last_passing_rank_minus = "before_last_passing_rank_minus"
        self.before_first_passing_rank = "before_first_passing_rank"
        self.jockey_year_rank = "jockey_year_rank"
        self.money = "money"
        self.horce_num = "horce_num"
        self.baba = "baba"
        self.before_pace = "before_pace"
        self.place = "place"
        self.popular_rank = "popular_rank"
        self.train_score = "train_score"
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
