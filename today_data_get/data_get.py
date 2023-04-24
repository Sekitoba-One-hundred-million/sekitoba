import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
import time

from sekitoba_logger import logger
import sekitoba_library as lib
from today_data_get import race_place_get

class TodayData:
    def __init__( self, url ):
        self.url = url
        self.place = ""
        self.year = ""
        self.month = ""
        self.day = ""
        self.race_id = ""
        self.hour = 0
        self.minutue = 0
        self.num = 0

def today_url_list_create( year, place, number, day_num ):
    result = []
    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
    base_url += year
    str_place_num = str( lib.place_num( place ) )
    
    if len( str_place_num ) == 1:
        base_url += "0"
        
    base_url += str_place_num
    base_url += "0" + number

    if len( day_num ) == 1:
        base_url += "0" + day_num
    else:
        base_url += day_num

    for i in range( 1, 13 ):
        url = base_url

        if i < 10:
            url += "0" + str( i )
        else:
            url += str( i )

        result.append( url )

    return result

def url_time( url ):
    bed_race = False
    time_data = ""
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for i in range( 0, len( div_tag ) ):
        class_name = div_tag[i].get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData01":
            text_data = div_tag[i].text.replace( "\n", "" )
            text_data = text_data.replace( " ", "" )
            split_text = text_data.split( "/" )
            time_data = split_text[0].replace( "発走", "" )

            if split_text[1][0] == "芝" \
               or split_text[1][0] == "ダ":
                bed_race = True
                
            break

    """
    for i in range( 0, len( div_tag ) ):
        class_name = div_tag[i].get( "class" )
        
        if not class_name == None \
           and class_name[0] == "RaceName":
            ct = div_tag[i].text.replace( "\n", "" )

            if "新馬" in ct:
                bed_race = False
    """
    
    return time_data, bed_race
    

def today_data_list_collect( year, month, day, place, number, day_num ) -> [ TodayData ]:
    today_data_list = []
    today_url_list = today_url_list_create( year, place, number, day_num )
    
    for today_url in today_url_list:
        t, c = url_time( today_url )

        if c:
            race_id = lib.id_get( today_url )
            
            td = TodayData( today_url )
            td.year = year
            td.month = month
            td.day = day
            td.place = place
            td.race_id = race_id
            td.hour = int( t.split( ":" )[0] )
            td.minutue = int( t.split( ":" )[1] )
            td.num = int( race_id[10:12] )
            today_data_list.append( td )
            logger.info( "today race {}:{}R".format( td.place, td.num) )
        
    return today_data_list

def wait( race_day ):
    now_time = datetime.datetime.now()
    total_seconds = ( race_day - now_time ).total_seconds()
    
    if total_seconds < 0 \
       and not now_time.day == race_day.day:
        return []
    elif 0 < total_seconds:
        print( "レース開始日時まで待ちます" )
        for i in tqdm( range( 0, int( total_seconds ) + 5 ) ):
            time.sleep( 1 )

def main() -> list[TodayData]: 
    data_set = []
    result = []

    dt_now = datetime.datetime.now()
    year = str( int( dt_now.year ) )
    month = str( int( dt_now.month ) )
    day = str( int( dt_now.day ) )
    print( year, month, day )

    #race_place = race_place_get.main()
    #for i in range( 0, len( race_place ) ):
    #        data_set.append( today_data_list_collect( year, race_place[i]["place"], \
    #                                            race_place[i]["number"], race_place[i]["day"] ) )
    #data_set.append( today_data_list_collect( year, month, day, "中山", "3", "8" ) )
    data_set.append( today_data_list_collect( year, month, day, "東京", "2", "2" ) )
    data_set.append( today_data_list_collect( year, month, day, "福島", "1", "6" ) )
    count = np.zeros( len( data_set ), dtype=np.int32 )

    while 1:
        min_h = 100
        
        for i in range( 0, len( data_set ) ):
            if count[i] < len( data_set[i] ):
                if data_set[i][count[i]].hour < min_h:
                    min_h = data_set[i][count[i]].hour

        if min_h == 100:
            break
        
        check_list = []
        
        for i in range( 0, len( data_set ) ):
            if count[i] < len( data_set[i] ):
                if data_set[i][count[i]].hour == min_h:
                    check_list.append( i )

        if len( check_list ) == 1:
            result.append( data_set[check_list[0]][count[check_list[0]]] )
            count[check_list[0]] += 1
        else:
            check = -1
            min_m = 100
            
            for i in range( 0, len( check_list ) ):
                if data_set[check_list[i]][count[check_list[i]]].minutue < min_m:
                    min_m = data_set[check_list[i]][count[check_list[i]]].minutue
                    check = i
            
            if not check == -1:
                result.append( data_set[check_list[check]][count[check_list[check]]] )
                count[check_list[check]] += 1

    return result
