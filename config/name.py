import datetime

class Name:
    def __init__( self ):
        self.before_rank = "before_rank"
        self.race_level_check = "race_level_check"
        self.straight_slope = "straight_slope"
        self.limb = "limb"
        self.age = "age"
        self.speed_index = "speed_index"
        self.race_interval = "race_interval"
        self.weight = "weight"
        self.before_id_weight = "before_id_weight"
        self.omega = "omega"
        self.before_speed = "before_speed"
        self.popular = "popular"
        self.trainer_rank = "trainer_rank"
        self.jockey_rank = "jockey_rank"
        self.before_diff = "before_diff"
        self.limb_horce_number = "limb_horce_number"
        self.mother_rank = "mother_rank"
        self.match_rank = "match_rank"
        self.weather = "weather"
        self.burden_weight = "burden_weight"
        self.before_continue_not_three_rank = "before_continue_not_three_rank"
        self.horce_sex = "horce_sex"
        self.horce_sex_month = "horce_sex_month"
        self.dist_kind_count = "dist_kind_count"
        self.before_popular = "before_popular"
        self.before_last_passing_rank = "before_last_passing_rank"
        self.before_first_passing_rank = "before_first_passing_rank"
        self.jockey_year_rank = "jockey_year_rank"
        self.age_dist = "age_dist"
        self.users_score_rate = "users_score_rate.pickle.v1"
        self.standard_time = "standard_time.pickle"
        self.up_pace_regressin = "up_pace_regressin.pickle"
        self.up_average = "up_average.pickle"
        self.race_day = "race_day.pickle"
        self.race_data = "race_data.pickle"
        self.horce_data_storage = "horce_data_storage.pickle"
        self.race_money_data = "race_money_data.pickle"
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
