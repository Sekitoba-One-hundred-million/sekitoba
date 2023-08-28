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
                    omega = None
                
                result[horce_num] = omega

    return result            
        
def main( storage: Storage, driver ):
    best_check_count = 0
    base_url = "https://www.keibalab.jp/db/race/"
    year = str( int( storage.today_data.race_date.year ) )
    month = lib.padding_str_math( str( int( storage.today_data.race_date.month ) ) )
    day = lib.padding_str_math( str( int( storage.today_data.race_date.day ) ) )
    key_place_num = lib.padding_str_math( str( storage.today_data.place_num ) )
    race_num = lib.padding_str_math( str( storage.today_data.race_num ) )
    url = base_url + year + month + day + key_place_num + race_num + "/syutsuba.html"

    for i in range( 0, 10 ):
        if best_check_count == storage.all_horce_num:
            break
        
        check_count = 0
        omega_data = data_get( url, driver )

        for horce_num in omega_data.keys():
            if not omega_data[horce_num] == None:
                check_count += 1

        if check_count < best_check_count:
            continue

        best_check_count = check_count
        
        for horce_num in omega_data.keys():
            for horce_id in storage.current_horce_data.keys():
                if storage.current_horce_data[horce_id].horce_num == horce_num:
                    storage.current_horce_data[horce_id].omega = omega_data[horce_num]
                    break
