import copy
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_logger import logger

from data_manage.storage import Storage
from config import name
import http_data_collect

dm.dl.file_set( name.race_day )
dm.dl.file_set( name.race_data )
dm.dl.file_set( name.race_money_data )

class HighLevel:
    def __init__( self ):
        self.race_day = dm.dl.data_get( name.race_day )
        self.race_data = dm.dl.data_get( name.race_data )
        self.race_money_data = dm.dl.data_get( name.race_money_data )

    def day_check( self, ymd, past_ymd ):
        if past_ymd["y"] < ymd["y"]:
            return True
        elif ymd["y"] < past_ymd["y"]:
            return False

        if past_ymd["m"] < ymd["m"]:
            return True
        elif ymd["m"] < past_ymd["m"]:
            return False

        if past_ymd["d"] < ymd["d"]:
            return True
        elif ymd["d"] < past_ymd["d"]:
            return False

        return False

    def race_horce_id_get( self, race_id ):
        result = {}
        url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
        r, _ = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if not tr_class_name == None and tr_class_name[0] == "HorseList":
                td_tag = tr.findAll( "td" )
                horce_id = http_data_collect.base_race_collect.horce_id_get( td_tag )
                result[horce_id] = horce_id

        return result

    def race_day_get( self, race_id ):
        result = {}
        result["year"] = int( race_id[0:4] )
        result["month"] = 0
        result["day"] = 0

        r, _ = lib.request( "https://race.netkeiba.com/race/result.html?race_id=" + race_id + "&rf=race_list" )
        soup = BeautifulSoup( r.content, "html.parser" )
        dd_tag = soup.findAll( "dd" )

        for dd in dd_tag:
            class_name = dd.get( "class" )

            if not class_name == None and class_name[0] == "Active":
                try:
                    text = dd.find( "a" ).get( "title" )
                    m_split = text.split( "月" )
                    d_split = m_split[1].split( "日" )
                    result["month"] = int( m_split[0] )
                    result["day"] = int( d_split[0] )
                except:
                    break
            
                break

        return result
    
    def race_money_get( self, race_id ):
        money = 0
        r, _ = lib.request( "https://race.netkeiba.com/race/result.html?race_id=" + race_id )
        soup = BeautifulSoup( r.content, "html.parser" )
        money = http_data_collect.base_race_collect.race_money_get( soup )
        return money

    def past_race_data_get( self, past_race_id_list ):
        past_race_data = {}

        for past_race_id in past_race_id_list:
            year = past_race_id[0:4]
            past_race_data[past_race_id] = {}

            if not past_race_id in self.race_day.keys():
                self.race_day[past_race_id] = self.race_day_get( past_race_id )

            if not past_race_id in self.race_data.keys():
                self.race_data[past_race_id] = self.race_horce_id_get( past_race_id )

            if not past_race_id in self.race_money_data.keys():
                self.race_money_data[past_race_id] = self.race_money_get( past_race_id )
                
            past_race_data[past_race_id]["horce_id"] = copy.deepcopy( self.race_data[past_race_id] )
            past_race_data[past_race_id]["ymd"] = { "y": int( year ), "m": self.race_day[past_race_id]["month"], "d": self.race_day[past_race_id]["day"] }
            past_race_data[past_race_id]["race_money"] = copy.deepcopy( self.race_money_data[past_race_id] )

        #dm.pickle_upload( name.race_day, self.race_day, prod = True )
        #dm.pickle_upload( name.race_data, self.race_data, prod = True )
        #dm.pickle_upload( name.race_money_data, self.race_money_data, prod = True )
        return past_race_data

    def horce_data_get( self, past_race_data ):
        result = {}
        base_url = "https://db.netkeiba.com/horse/"
        
        for race_id in past_race_data.keys():
            for horce_id in past_race_data[race_id]["horce_id"].keys():
                url = base_url + horce_id
                r, _ = lib.request( url )
                soup = BeautifulSoup( r.content, "html.parser" )
                result[horce_id] = http_data_collect.horce_data_get.past_horce_data_get( soup )

        return result

    def score_get( self, storage: Storage, horce_id ):
        result = 1000
        pd = storage.past_data[horce_id]
        past_race_data = self.past_race_data_get( pd.race_id_get() )
        horce_data = self.horce_data_get( past_race_data )
        next_race_data: dict[ str, dict[ str, lib.current_data ] ] = {}
        current_race_rank = lib.money_class_get( storage.race_money )

        for race_id in past_race_data.keys():
            next_race_data[race_id] = {}
            
            for horce_id in past_race_data[race_id]["horce_id"].keys():
                next_race_data[race_id][horce_id] = lib.next_race( horce_data[horce_id], past_race_data[race_id]["ymd"] )
                #print( next_race_data[race_id][horce_id] )
        
        for past_cd in pd.past_cd_list():
            past_race_id = past_cd.race_id()
            past_day = past_cd.birthday()
            past_rank = past_cd.rank()
            ymd = past_race_data[past_race_id]["ymd"]
            high_level = False
            past_race_rank = lib.money_class_get( past_race_data[past_race_id]["race_money"] )

            if past_race_rank < current_race_rank:
                continue
            
            for horce_id in next_race_data[race_id].keys():
                next_cd = next_race_data[race_id][horce_id]

                if next_cd == None:
                    continue
                
                birthday = next_cd.ymd()
                past_ymd = { "y": int( birthday[0] ), "m": int( birthday[1] ), "d": int( birthday[2] ) }

                if not self.day_check( ymd, past_ymd ):
                    continue

                if next_cd.rank() == 1:
                    high_level = True
                    break

            if high_level:
                result = min( result, past_rank )

        return result
