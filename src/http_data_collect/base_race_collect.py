from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
from data_manage import Storage
from data_manage import CurrentHorceData

first_name = "http_data_collect/base_race_collect"
data_name_list = [ "horce_num", "waku_num", "age", "burden_weight", "jockey_id", "trainer_id" ]

def horce_id_get( td_tag ):
    horce_id = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "HorseInfo":
            horce_url = td.find( "a" ).get( "href" )
            horce_id = horce_url.split( "/" )[-1]
            break
            
    return horce_id

def horce_number_get( td_tag ):
    horce_num = None

    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and "Umaban" in td_class_name[0]:
            str_horce_num = lib.text_replace( td.text )
            horce_num = int( lib.math_check( str_horce_num ) )
            break

    return horce_num

def waku_number_get( td_tag ):
    waku_num = None

    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and "Waku" in td_class_name[0]:
            str_waku_num = lib.text_replace( td.text )
            waku_num = int( lib.math_check( str_waku_num ) )
            break

    return waku_num

def age_get( td_tag ):
    age = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Barei":
            str_age = lib.str_math_pull( lib.text_replace( td.text ) )
            age = int( lib.math_check( str_age ) )
            break

    return age

def sex_get( td_tag ):
    sex = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Barei":
            str_sex = lib.text_replace( td.text )[0]
            sex = lib.sex_num( str_sex )
            break

    return sex

def burden_weight_get( td_tag ):
    burden_weight = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Txt_C":
            str_burden_weight = lib.text_replace( td.text )
            burden_weight = lib.math_check( str_burden_weight )
            break

    return burden_weight

def joceky_id_get( td_tag ):
    jockey_id = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Jockey":
            jockey_url = td.find( "a" ).get( "href" )
            jockey_id = jockey_url.split( "/" )[-2]
            break
            
    return jockey_id

def trainer_id_get( td_tag ):
    trainer_id = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Trainer":
            trainer_url = td.find( "a" ).get( "href" )
            trainer_id = trainer_url.split( "/" )[-2]
            break
            
    return trainer_id

def weight_get( td_tag ):
    weight = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Weight":
            try:
                text = lib.text_replace( td.text )
                str_weight = text.split( "(" )[0]
                weight = int( lib.math_check( str_weight ) )
            except:
                weight = -1
                
            break
   
    return weight

def dist_race_kind_get( soup ):
    dist = None
    race_kind = None
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "RaceData01":
            span_tag = div.findAll( "span" )

            try:
                str_dist = lib.text_replace( span_tag[0].text )
                dist = int( lib.str_math_pull( str_dist ) )
                _, race_kind = lib.dist( str_dist )
            except:
                continue

    return dist, race_kind

def outside_get( soup ):
    outside = False
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "RaceData01":
            if "外" in div.text:
                outside = True
                break

    return outside

def weather_get( soup ):
    weather = None
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "RaceData01":
            try:
                str_weather = lib.text_replace( div.text ).split( "/" )[2][-1]
            except:
                continue
            
            weather = int( lib.weather( str_weather ) )
            break

    return weather

def baba_get( soup ):
    baba = None
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "RaceData01":
            span_tag = div.findAll( "span" )
            
            try:
                str_baba = span_tag[2].text[-1]
            except:
                continue
            
            baba = int( lib.baba( str_baba ) )
            break

    return baba

def race_money_get( soup ):
    money = None
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData02":
            span_tag = div.findAll( "span" )

            for span in span_tag:
                text = span.text.replace( "\n", "" )
                split_text = text.split( "," )

                if len( split_text ) > 1 \
                   and "本賞金" in split_text[0]:
                    try:
                        money = float( split_text[0].split( ":" )[1] )
                    except:
                        money = 0
                    break
            break

    return money

def main( storage: Storage, before = False ):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.today_data.race_id

    for i in range( 0, 10 ):
        r, _ = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )

        if not storage.before_data_check():
            storage.dist, storage.race_kind = dist_race_kind_get( soup )
            storage.outside = outside_get( soup )
            storage.weather = weather_get( soup )
            storage.baba = baba_get( soup )
            storage.race_money = race_money_get( soup )

        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if not tr_class_name == None and tr_class_name[0] == "HorseList":
                td_tag = tr.findAll( "td" )
                horce_id = horce_id_get( td_tag )
                current_horce_data = CurrentHorceData()
                current_horce_data.horce_num = horce_number_get( td_tag )
                current_horce_data.waku_num = waku_number_get( td_tag )
                current_horce_data.age = age_get( td_tag )
                current_horce_data.sex = sex_get( td_tag )
                current_horce_data.burden_weight = burden_weight_get( td_tag )
                current_horce_data.jockey_id = joceky_id_get( td_tag )
                current_horce_data.trainer_id = trainer_id_get( td_tag )
                storage.current_horce_data[horce_id] = current_horce_data
                storage.horce_id_list.append( horce_id )
                
        storage.all_horce_num = len( storage.horce_id_list )
        current_horce_data_check = False

        for horce_id in storage.current_horce_data.keys():
            current_horce_data_check = storage.current_horce_data[horce_id].before_data_check()

        if storage.before_data_check() and \
          current_horce_data_check:
            break
