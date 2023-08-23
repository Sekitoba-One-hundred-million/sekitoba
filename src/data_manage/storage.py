import sekitoba_library as lib
#from data_analyze.users_data import UsersData
from today_data_get.data_get import TodayData

class Storage:
    def __init__( self ):
        self.race_id = ""
        self.place_num = ""
        self.weather = 0
        self.dist = 0
        self.baba = 0
        self.race_kind = 0
        self.place = 0
        self.all_horce_num = 0
        self.race_money = 0
        self.today_data: TodayData = None
        self.outside = False
        self.horce_id_list = []
        self.data = {}
        self.past_data: dict[ str, lib.past_data ] = {}
        #self.users_data: UsersData = None
