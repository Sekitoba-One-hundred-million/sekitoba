import sekitoba_library as lib
import sekitoba_data_manage as dm

from config import data_name
from config import pickle_name
from data_manage import Storage

dm.dl.file_set( pickle_name.horce_data_storage )

class DataCreate:
    def __init__( self, storage: Storage ):
        self.storage: Storage = storage
        self.analyze_data = {}

        self.horce_data_storage = dm.dl.data_get( pickle_name.horce_data_storage )

    def current_race_data_create( self, horce_id ):
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
        current_race_data[12] = str( int( self.storage.current_horce_data[horce_id].burden_weight ) )
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
        
    def create( self ):
        str_year = str( self.storage.today_data.year )
        str_day = str( self.storage.today_data.day )
        str_num = str( self.storage.today_data.num )
        str_place_num = str( self.storage.today_data.place_num )
        
        for horce_id in self.storage.horce_id_list:
            if not horce_id in self.horce_data_storage:
                continue
            
            a, past_data = lib.race_check( self.horce_data_storage[horce_id], \
                                          str_year, str_day, str_num, str_place_num )
            print( a )
            print( self.current_race_data_create( horce_id ) )
            print( "" )
