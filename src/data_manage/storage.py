import sekitoba_library as lib
#from data_analyze.users_data import UsersData
from data_manage.today_data import TodayData
from data_manage.train_data import TrainData
from data_manage.current_horce_data import CurrentHorceData

class Storage:
    def __init__( self, today_data ):
        self.weather = None
        self.dist = None
        self.baba = None
        #self.race_kind = None
        self.all_horce_num = None
        self.race_money = None
        self.outside = None
        self.today_data: TodayData = today_data
        self.horce_id_list = []
        self.current_horce_data: dict[ str, CurrentHorceData ] = {}
        self.train_data: dict[ str, TrainData ] = {}
        self.past_data: dict[ str, lib.past_data ] = {}
        #self.users_data: UsersData = None

    def before_data_check( self ):
        #print( self.weather, self.dist )
        if self.weather == None:
            return False
        elif self.dist == None:
            return False
        elif self.baba == None:
            return False
        elif self.all_horce_num == None or self.all_horce_num == 0:
            return False
        elif self.race_money == None:
            return False
        elif self.outside == None:
            return False

        return True
