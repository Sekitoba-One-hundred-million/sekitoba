import SekitobaLibrary as lib
#from data_analyze.users_data import UsersData
from data_manage.today_data import TodayData
from data_manage.train_data import TrainData
from data_manage.current_horce_data import CurrentHorceData

class Storage:
    def __init__( self, today_data ):
        self.base_money = 20000
        self.weather = None
        self.dist = None
        self.baba = None
        #self.race_kind = None
        self.all_horce_num = None
        self.race_money = None
        self.outside = None
        self.predict_netkeiba_pace = None
        self.predict_netkeiba_deployment: list = []
        self.today_data: TodayData = today_data
        self.horce_id_list = []
        self.jockey_id_list = []
        self.trainer_id_list = []
        self.current_horce_data: dict[ str, CurrentHorceData ] = {}
        self.train_data: dict[ str, TrainData ] = {}
        self.past_data: dict[ str, lib.PastData ] = {}
        self.condition_devi: dict[ str, float ] = {}
        self.first_up3: dict[ str, dict[ int, dict[ str, float ] ] ] = {}
        self.wide_odds: dict[ int, dict[ int, float ] ] = {}
        self.skip_horce_id_list = []
        self.cansel_horce_id_list = []

    def before_data_check( self ):
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
