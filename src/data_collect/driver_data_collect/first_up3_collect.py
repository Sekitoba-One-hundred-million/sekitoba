import time
from bs4 import BeautifulSoup
from data_manage import Storage

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def first_time_get( soup, storage: Storage ):
    race_id = storage.today_data.race_id
    div_tag = soup.find( "body" ).findAll( "div" )

    for div in div_tag:
        div_class_name = div.get( "class" )

        if div_class_name == None or len( div_class_name ) == 0 or not div_class_name[0] == "HorseList_Wrapper":
            continue
        
        dl_tag = div.findAll( "dl" )

        for dl in dl_tag:
            dl_class_name = dl.get( "class" )

            if dl_class_name == None or len( dl_class_name ) == 0 or not dl_class_name[0] == "HorseList":
                continue

            dt_tag = dl.findAll( "dt" )

            try:
                horce_num = str( int( dt_tag[1].text ) )
            except:
                continue

            lib.dicAppend( storage.first_up3, horce_num, {} )
            ul_tag = dl.findAll( "ul" )

            for ul in ul_tag:
                ul_class_name = ul.get( "class" )

                if ul_class_name == None or len( ul_class_name ) == 0 or not ul_class_name[0] == "Past_Direction":
                    continue

                li_tag = ul.findAll( "li" )

                for li in li_tag:
                    past_div_tag = li.findAll( "div" )

                    try:
                        past_race_id = past_div_tag[2].find( "a" ).get( "href" ).split( "/" )[-2]
                        first_up3 = float( past_div_tag[6].text.split( " " )[1].replace( "前", "" ) )
                    except:
                        continue

                    storage.first_up3[horce_num][past_race_id] = first_up3

def first_up3_collect( storage: Storage, driver ):
    url = "https://race.netkeiba.com/race/newspaper.html?race_id={}".format( storage.today_data.race_id )
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 10 )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )        
    first_time_get( soup, storage )
