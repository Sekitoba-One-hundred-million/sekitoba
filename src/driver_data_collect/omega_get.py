import time
from bs4 import BeautifulSoup

from data_manage.storage import Storage
import sekitoba_library as lib
from sekitoba_logger import logger

def data_get( url, driver ):
    result = {}
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 5 )
    
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    tbody_tag = soup.findAll( "tbody" )

    for tbody in tbody_tag:
        class_name = tbody.get( "class" )

        if not class_name == None and class_name[0] == "sortobject":
            tr_tag = tbody.findAll( "tr" )

            for tr in tr_tag:
                td_tag = tr.findAll( "td" )
                try:
                    horce_num = lib.text_replace( td_tag[1].text )
                    omega = int( lib.text_replace( td_tag[7].text ) )
                except:
                    continue
                
                result[horce_num] = omega

    return result

def data_check( storage: Storage ):
    first_name = "driver_data_collect/omega_get"

    for i in range( 1, storage.all_horce_num + 1 ):
        key_horce_num = str( i )
        if key_horce_num in storage.data["omega"].keys():
            logger.info( "{} race_id:{} horce_num:{} omega:{}".format( first_name, storage.race_id, key_horce_num, storage.data["omega"][key_horce_num] ) )
        else:
            logger.warning( "{} race_id:{} horce_num:{}".format( first_name, storage.race_id, key_horce_num ) )
            
        
def main( storage: Storage, driver ):
    base_url = "https://www.keibalab.jp/db/race/"
    year = str( int( storage.today_data.year ) )
    month = str( int( storage.today_data.month ) )
    day = str( int( storage.today_data.day ) )
    key_place_num = str( storage.place_num )
    race_num = storage.race_id[10:12]

    if len( month ) == 1:
        month = "0" + month

    if len( day ) == 1:
        day = "0" + day

    if len( key_place_num ) == 1:
        key_place_num = "0" + key_place_num

    url = base_url + year + month + day + key_place_num + race_num + "/syutsuba.html"
    storage.data["omega"] = data_get( url, driver )
    data_check( storage )
