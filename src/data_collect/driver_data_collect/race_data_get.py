import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import SekitobaLibrary as lib
from SekitobaLogger import logger
from data_manage import Storage
from data_manage import CurrentHorceData
from data_collect.http_data_collect import baba_get
from data_collect.http_data_collect import weather_get

def horce_idGet( td_tag ):
    horce_id = ""
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "HorseInfo":
            horce_url = td.find( "a" ).get( "href" )
            horce_id = horce_url.split( "/" )[-1]
            break
            
    return horce_id

def weight_get( td_tag ):
    weight = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Weight":
            try:
                weight = lib.textReplace( td.text )
            except:
                continue

            break
   
    return weight

def odds_get( td_tag ):
    odds = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Txt_R" and td_class_name[1] == "Popular":
            str_odds = lib.textReplace( td.text )
            odds = float( lib.mathCheck( str_odds ) )
            break

    return odds

def popular_get( td_tag ):
    popular = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Popular" and td_class_name[1] == "Popular_Ninki":
            str_popular = lib.textReplace( td.text )
            popular = int( lib.mathCheck( str_popular ) )
            break

    return popular

def main( storage: Storage, driver ):
    best_check_count = 0
    best_data_dict = {}
    odd_update_xpath = "/html/body/div[1]/div[3]/div[2]/table/thead/tr[1]/th[10]/div/div/button"
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.today_data.race_id
    
    for i in range( 0, 10 ):
        if best_check_count == storage.all_horce_num:
            break
        
        instance_dict = {}
        driver, _ = lib.driverRequest( driver, url )
        time.sleep( 2 )

        try:
            driver.find_element( By.XPATH, odd_update_xpath ).click()
        except:
            pass
        
        time.sleep( 2 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        storage.baba = baba_get( soup )
        storage.weather = weather_get( soup )
        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if not tr_class_name == None and tr_class_name[0] == "HorseList":                    
                td_tag = tr.findAll( "td" )
                horce_id = horce_idGet( td_tag )
                instance_current_horce_data = CurrentHorceData()
                instance_current_horce_data.odds = odds_get( td_tag )
                instance_current_horce_data.popular = popular_get( td_tag )
                instance_current_horce_data.weight = weight_get( td_tag )
                instance_dict[horce_id] = instance_current_horce_data

                if len( tr_class_name ) == 2 and \
                  tr_class_name[1] == "Cancel" and \
                  not horce_id in storage.cansel_horce_id_list:
                    storage.cansel_horce_id_list.append( horce_id )

        check_count = 0
        
        for horce_id in instance_dict.keys():
            if horce_id in storage.cansel_horce_id_list:
                continue
            
            if instance_dict[horce_id].just_before_data_check():
                check_count += 1

        if best_check_count < check_count:
            best_check_count = check_count

            for horce_id in instance_dict.keys():
                storage.current_horce_data[horce_id].odds = instance_dict[horce_id].odds
                storage.current_horce_data[horce_id].popular = instance_dict[horce_id].popular
                storage.current_horce_data[horce_id].weight = instance_dict[horce_id].weight
