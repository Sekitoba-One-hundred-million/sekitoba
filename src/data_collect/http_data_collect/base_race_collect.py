from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
from data_manage import Storage
from data_manage import CurrentHorceData

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
                weight = lib.text_replace( td.text )
            except:
                continue

            break
   
    return weight

def dist_race_kind_get( soup ):
    dist_data = None
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )
        
        if not class_name == None and class_name[0] == "RaceData01":
            span_tag = div.findAll( "span" )

            try:
                dist_data = lib.text_replace( span_tag[0].text ).replace( "m", "" )
                #dist = int( lib.str_math_pull( str_dist ) )
                #_, race_kind = lib.dist( str_dist )
            except:
                continue

    return dist_data

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
            
            weather = str_weather
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
            
            baba = str_baba
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