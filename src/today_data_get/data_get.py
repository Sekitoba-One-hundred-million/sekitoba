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
        self.timestamp = 0

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
    
    return time_data, bed_race    

def race_base_id_get( soup ):
    race_id_list = []
    p_tag = soup.findAll( "p" )

    for p in p_tag:
        class_name = p.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceList_DataTitle":

            try:
                split_data = p.text.split( " " )
                str_count = split_data[0].replace( "回", "" )
                place_num = str( int( lib.place_num( split_data[1] ) ) )
                str_day = split_data[2].replace( "日目", "" )
            except:
                continue

            base_id = lib.padding_str_math( place_num ) + lib.padding_str_math( str_count ) + lib.padding_str_math( str_day )

            for i in range( 1, 13 ):
                race_id_list.append( base_id + lib.padding_str_math( str( i ) ) )

    return race_id_list

def predict_race_id_get( today: datetime.datetime ):
    race_id_list = []
    driver = lib.driver_start()
    base_url = "https://race.netkeiba.com/top/?kaisai_date="
    days = 0

    if today.hour > 16:
        days = 1

    while 1:
        check_day = today + datetime.timedelta( days = days )
        data_id = str( check_day.year ) + \
          lib.padding_str_math( str( check_day.month ) ) + \
          lib.padding_str_math( str( check_day.day ) )

        url = base_url + data_id
        driver, _ = lib.driver_request( driver, url )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        race_id_list = race_base_id_get( soup )

        if not len( race_id_list ) == 0:
            break
        
        days += 1

        if days == 10:
            print( "not found race_id" )
            sys.exit( 1 )

    str_year = str( today.year )

    for i in range( 0, len( race_id_list ) ):
        race_id_list[i] = str_year + race_id_list[i]

    return race_id_list

