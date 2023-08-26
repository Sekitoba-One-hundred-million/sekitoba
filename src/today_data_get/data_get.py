import datetime
from bs4 import BeautifulSoup

from data_manage import TodayData
from sekitoba_logger import logger
import sekitoba_library as lib

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
    race_day = None
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
            race_day = check_day
            break

        week_num = check_day.weekday()

        # 土日なのに取得できていない場合は失敗なのでもう一回
        if week_num == 5 or \
          week_num == 6:
            continue
        
        days += 1

        if days == 10:
            print( "not found race_id" )
            sys.exit( 1 )

    str_year = str( today.year )

    for i in range( 0, len( race_id_list ) ):
        race_id_list[i] = str_year + race_id_list[i]

    return race_id_list, race_day

def today_data_list_create() -> list[TodayData]:
    today_data_list = []
    #race_id_list, race_day = predict_race_id_get( datetime.datetime.now() )
    race_id_list, race_day = predict_race_id_get( datetime.datetime( 2023, 7, 9 ) )

    for race_id in race_id_list:
        today_data = TodayData( race_id, race_day )

        # htmlがきちんと取得できない可能性があるので
        for i in range( 0, 5 ):
            today_data.race_time_get()

            if today_data.race_timestamp == -1:
                continue

            if today_data.bet_race:
                today_data_list.append( today_data )
                
            break

    return sorted( today_data_list, key = lambda x: x.race_timestamp )
