import datetime
from bs4 import BeautifulSoup

from data_manage import TodayData
from SekitobaLogger import logger
import SekitobaLibrary as lib

def raceBaseIdGet( soup ):
    race_idList = []
    pTag = soup.findAll( "p" )

    for p in pTag:
        className = p.get( "class" )

        if not className == None \
          and 0 < len( className ) \
          and className[0] == "RaceList_DataTitle":

            splitData = p.text.split( " " )

            if len( splitData ) < 2:
                continue
            
            strCount = splitData[0].replace( "回", "" )
            strPlaceNum = str( int( lib.place_num( splitData[1] ) ) )
            strDay = splitData[2].replace( "日目", "" )

            baseId = lib.paddingStrMath( strPlaceNum ) + lib.paddingStrMath( strCount ) + lib.paddingStrMath( strDay )

            for i in range( 1, 13 ):
                race_idList.append( baseId + lib.paddingStrMath( str( i ) ) )

    return race_idList

def predictRaceIdGet( today: datetime.datetime ):
    race_idList = []
    driver = lib.driver_start()
    baseUrl = "https://race.netkeiba.com/top/?kaisai_date="
    raceDay = ""
    days = 0

    if today.hour > 16:
        days = 1

    while 1:
        checkDay = today + datetime.timedelta( days = days )
        dataId = str( checkDay.year ) + \
          lib.paddingStrMath( str( checkDay.month ) ) + \
          lib.paddingStrMath( str( checkDay.day ) )

        url = baseUrl + dataId
        driver, _ = lib.driver_request( driver, url )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        race_idList = raceBaseIdGet( soup )

        if not len( race_idList ) == 0:
            raceDay = checkDay
            break

        weekNum = check_day.weekday()

        # 土日なのに取得できていない場合は失敗なのでもう一回
        if weekNum == 5 or \
          weekNum == 6:
            continue
        
        days += 1

        if days == 10:
            print( "not found race_id" )
            sys.exit( 1 )

    str_year = str( today.year )

    for i in range( 0, len( race_idList ) ):
        race_idList[i] = str_year + race_idList[i]

    return race_idList, raceDay

def today_data_listCreate() -> list[TodayData]:
    today_data_list = []
    race_idList, raceDay = predictRaceIdGet( datetime.datetime.now() )

    for race_id in race_idList:
        todayData = TodayData( race_id, raceDay )

        # htmlがきちんと取得できない可能性があるので
        for i in range( 0, 5 ):
            todayData.race_time_get()

            if todayData.race_timestamp == -1:
                continue

            if todayData.bet_race:
                today_data_list.append( todayData )
                
            break

    return sorted( today_data_list, key = lambda x: x.race_timestamp )
