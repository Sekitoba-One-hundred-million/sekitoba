import time
from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
from data_manage import Storage
from data_manage import CurrentHorceData

def horce_id_get( td_tag ):
    horce_id = ""
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "HorseInfo":
            horce_url = td.find( "a" ).get( "href" )
            horce_id = horce_url.split( "/" )[-1]
            break
            
    return horce_id

def id_weight_get( td_tag ):
    id_weight = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Weight":
            try:
                text = td.find( "small" ).text
                str_id_weight = lib.str_math_pull( lib.text_replace( text ) )
                id_weight = int( lib.math_check( str_id_weight ) )

                if "-" in text:
                    id_weight *= -1
            except:
                id_weight == -1000
            
            break
   
    return id_weight

def odds_get( td_tag ):
    odds = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Txt_R" and td_class_name[1] == "Popular":
            str_odds = lib.text_replace( td.text )
            odds = int( lib.math_check( str_odds ) )
            break

    return odds

def popular_get( td_tag ):
    popular = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Popular" and td_class_name[1] == "Popular_Ninki":
            str_popular = lib.text_replace( td.text )
            popular = int( lib.math_check( str_popular ) )
            break

    return popular

def main( storage: Storage, driver ):
    best_check_count = 0
    best_data_dict = {}
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.today_data.race_id

    for i in range( 0, 10 ):
        if best_check_count == storage.all_horce_num:
            break
        
        instance_dict = {}
        driver, _ = lib.driver_request( driver, url )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if not tr_class_name == None and tr_class_name[0] == "HorseList":
                td_tag = tr.findAll( "td" )
                horce_id = horce_id_get( td_tag )
                instance_current_horce_data = CurrentHorceData()
                instance_current_horce_data.odds = odds_get( td_tag )
                instance_current_horce_data.popular = popular_get( td_tag )
                instance_current_horce_data.id_weight = id_weight_get( td_tag )
                print( horce_id, instance_current_horce_data.odds, instance_current_horce_data.popular, instance_current_horce_data.id_weight )
                instance_dict[horce_id] = instance_current_horce_data

        check_count = 0
        
        for horce_id in instance_dict.keys():
            if instance_dict[horce_id].just_before_data_check():
                check_count += 1

        print( check_count, storage.all_horce_num )
        if best_check_count < check_count:
            best_check_count = check_count

            for horce_id in instance_dict.keys():
                storage.current_horce_data[horce_id].odds = instance_dict[horce_id].odds
                storage.current_horce_data[horce_id].popular = instance_dict[horce_id].popular
                storage.current_horce_data[horce_id].id_weight = instance_dict[horce_id].id_weight
