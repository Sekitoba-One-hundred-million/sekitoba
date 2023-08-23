import time
from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
from data_manage.storage import Storage

def horce_id_get( td_tag ):
    horce_id = ""
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "HorseInfo":
            horce_url = td.find( "a" ).get( "href" )
            horce_id = horce_url.split( "/" )[-1]
            break
            
    return horce_id

def odds_get( td_tag ):
    odds = 0
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Txt_R" and td_class_name[1] == "Popular":
            str_odds = lib.text_replace( td.text )
            odds = int( lib.math_check( str_odds ) )
            break

    return odds

def popular_get( td_tag ):
    popular = 0
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Popular" and td_class_name[1] == "Popular_Ninki":
            str_popular = lib.text_replace( td.text )
            popular = int( lib.math_check( str_popular ) )
            break

    return popular

def data_check( storage: Storage, horce_id ):
    first_name = "driver_data_collect/race_data_get"
    check_data_name = [ "odds", "popular" ]
    horce_num = storage.data[horce_id]["horce_num"]
    
    for data_key in check_data_name:
        if not storage.data[horce_id][data_key] == 0:
            logger.info( "{} race_id:{} horce_num:{} {}:{}".format( first_name, storage.race_id, horce_num, data_key, storage.data[horce_id][data_key] ) )
        else:
            logger.warning( "{} fail race_id:{} horce_num:{} {}".format( first_name, storage.race_id, horce_num, data_key ) )

def main( storage: Storage, driver ):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.race_id
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 5 )

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )

    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        tr_class_name = tr.get( "class" )

        if not tr_class_name == None and tr_class_name[0] == "HorseList":
            td_tag = tr.findAll( "td" )
            horce_id = horce_id_get( td_tag )
            storage.data[horce_id]["odds"] = odds_get( td_tag )
            storage.data[horce_id]["popular"] = popular_get( td_tag )
