import time
from bs4 import BeautifulSoup
from data_manage import Storage

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( soup ):
    base_num = 1
    table_tag = soup.findAll( "table" )
    odds_data = {}

    for table in table_tag:
        class_name = table.get( "class" )
        
        if class_name == None or len( class_name ) == 0 or not class_name[0] == "Odds_Table":
            continue

        instance_odds_data = {}
        td_tag = table.findAll( "td" )
        before_num = -1

        for td in td_tag:
            class_name = td.get( "class" )

            if class_name == None:
                continue

            if len( class_name ) == 1 and class_name[0] == "Waku_Normal":
                try:
                    before_num = int( lib.text_replace( td.text ) )
                except:
                    continue

            if len( class_name ) == 2 and class_name[0] == "Odds" and class_name[1] == "Popular":
                try:
                    odds_text = lib.text_replace( td.text )
                    odds = float( odds_text )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = odds
                    before_num = -1

        if len( instance_odds_data ) == 0:
            base_num += 1
            continue

        odds_data[base_num] = instance_odds_data
        base_num += 1

    return odds_data

def quinella_odds_collect( storage: Storage, driver ):
    url = "https://race.netkeiba.com/odds/index.html?type=b4&race_id={}&housiki=c0".format( storage.today_data.race_id )
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 1 )
    base_num = 1
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    storage.quinella_odds_data = data_get( soup )
