from config import name as data_name

class UsersScoreFunction:
    def __init__( self ):
        self.function = {}

    def set_function( self ):
        self.function[data_name.before_rank] = self.before_rank
        self.function[data_name.race_level_check] = self.race_level_check
        self.function[data_name.straight_slope] = self.straight_slope
        #self.function[data_name.foot_used] = self.foot_used
        self.function[data_name.limb] = self.limb
        self.function[data_name.age] = self.age
        self.function[data_name.speed_index] = self.speed_index
        self.function[data_name.race_interval] = self.race_interval
        self.function[data_name.weight] = self.weight
        self.function[data_name.before_id_weight] = self.before_id_weight
        self.function[data_name.omega] = self.omega
        self.function[data_name.before_speed] = self.before_speed
        self.function[data_name.popular] = self.popular
        self.function[data_name.trainer_rank] = self.trainer_rank
        self.function[data_name.jockey_rank] = self.jockey_rank
        #self.function[data_name.popular_rank] = self.popular_rank
        self.function[data_name.before_diff] = self.before_diff
        self.function[data_name.limb_horce_number] = self.limb_horce_number
        #self.function[data_name.father_rank] = self.father_rank
        self.function[data_name.mother_rank] = self.mother_rank
        self.function[data_name.match_rank] = self.match_rank
        self.function[data_name.weather] = self.weather
        #self.function[data_name.money] = self.money
        self.function[data_name.burden_weight] = self.burden_weight
        #self.function[data_name.before_up3_rank] = self.before_up3_rank
        self.function[data_name.before_continue_not_three_rank] = self.before_continue_not_three_rank
        #self.function[data_name.limb_place] = self.limb_place
        self.function[data_name.horce_sex] = self.horce_sex
        self.function[data_name.horce_sex_month] = self.horce_sex_month
        self.function[data_name.dist_kind_count] = self.dist_kind_count
        self.function[data_name.before_popular] = self.before_popular
        self.function[data_name.before_last_passing_rank] = self.before_last_passing_rank
        self.function[data_name.before_first_passing_rank] = self.before_first_passing_rank
        #self.function[data_name.before_pace] = self.before_pace
        self.function[data_name.jockey_year_rank] = self.jockey_year_rank
        self.function[data_name.age_dist] = self.age_dist
        
    def before_rank( self, score ):
        score = int( score )
        
        if score == 4 or score == 7 or score == 8:
            return 5

        if 14 < score:
            return -5

        return 0

    def race_level_check( self, score ):
        score = int( score )

        if score == 3 or score == 4:
            return 10

        if 13 < score:
            return -5

        return 0

    def straight_slope( self, score ):
        score = int( score )

        if score == 2:
            return 5

        return 0

    def limb( self, score ):
        score = int( score )

        if score == 3:
            return 5

        return 0

    def age( self, score ):
        score = int( score )

        if score == 5:
            return 5

        return 0

    def speed_index( self, score ):
        score = int( score )

        if score == 1 or score == 2 or score == 3 or score == 4:
            return 5
        
        return 0

    def race_interval( self, score ):
        score = int( score )

        if score == 10:
            return 5

        if score < 3:
            return -5
        
        return 0

    def weight( self, score ):
        score = int( score )

        if score == 50:
            return 5

        if score < 45:
            return -5

        return 0
    
    def before_id_weight( self, score ):
        score = int( score )

        if score == -2:
            return 5

        return 0

    def omega( self, score ):
        score = int( score )

        if score == 17:
            return 5

        if score < 12:
            return -10

        return 0

    def before_speed( self, score ):
        score = int( score )

        if 65 < score:
            return -5

        return 0

    def popular( self, score ):
        score = int( score )

        if 1 < score and score < 8:
            return 5

        if 12 < score:
            return -5
        
        return 0

    def trainer_rank( self, score ):
        score = int( score )

        if score == 5 or score == 6:
            return 5

        if 8 < score:
            return -5

        return 0

    def jockey_rank( self, score ):
        score = int( score )

        if score == 7:
            return 5

        if 9 < score:
            return -5

        return 0

    def before_diff( self, score ):
        score = int( score )

        if score == 7 or score == 8:
            return 5

        return 0

    def limb_horce_number( self, score ):
        score = int( score )
        
        if score == 304 or score == 305 or score == 306:
            return 5

        if score == 300 or score == 600:
            return -5

        return 0

    def mother_rank( self, score ):
        score = int( score )
        
        if score == 4:
            return 5

        return 0

    def match_rank( self, score ):
        score = int( score )
        
        if score == 6:
            return 5
        
        if 10 < score:
            return -5

        return 0

    def weather( self, score ):
        score = int( score )
        
        if score == 3:
            return 5

        return 0

    def burden_weight( self, score ):
         score = int( score )

         if score == 6:
             return 5

         return 0

    def before_continue_not_three_rank( self, score ):
        score = int( score )

        if score == 6:
            return 5

        return 0

    def horce_sex( self, score ):
        score = int( score )

        if score == 0:
            return 5

        return 0

    def horce_sex_month( self, score ):
        score = int( score )

        if score == 11 or score == 31:
            return 5

        return 0

    def dist_kind_count( self, score ):
        score = int( score )

        if score == 20:
            return -5

        return 0

    def before_popular( self, score ):
        score = int( score )

        if score == 5 or score == 6:
            return 5

        return 0

    def before_last_passing_rank( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        #if score == 17 or score == 18:
        #    return -5

        return 0

    def before_first_passing_rank( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        return 0

    def jockey_year_rank( self, score ):
        score = int( score )

        if score == 2:
            return 5

        return 0

    def age_dist( self, score ):
        score = int( score )

        if score == 54:
            return 0

        return 0
