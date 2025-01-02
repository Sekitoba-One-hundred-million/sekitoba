import copy
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
from SekitobaLogger import logger
from data_manage import Storage
from data_manage import CurrentHorceData

def horce_idGet( td_tag ):
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
            str_horce_num = lib.textReplace( td.text )
            horce_num = int( lib.mathCheck( str_horce_num ) )
            break

    return horce_num

def waku_number_get( td_tag ):
    waku_num = None

    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and "Waku" in td_class_name[0]:
            str_waku_num = lib.textReplace( td.text )
            waku_num = int( lib.mathCheck( str_waku_num ) )
            break

    return waku_num

def age_get( td_tag ):
    age = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Barei":
            str_age = lib.strMathPull( lib.textReplace( td.text ) )
            age = int( lib.mathCheck( str_age ) )
            break

    return age

def sex_get( td_tag ):
    sex = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Barei":
            str_sex = lib.textReplace( td.text )[0]
            sex = lib.sexNum( str_sex )
            break

    return sex

def burden_weight_get( td_tag ):
    burden_weight = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Txt_C":
            str_burden_weight = lib.textReplace( td.text )
            burden_weight = lib.mathCheck( str_burden_weight )
            break

    return burden_weight

def joceky_idGet( td_tag ):
    jockey_id = None
    
    for td in td_tag:
        td_class_name = td.get( "class" )

        if not td_class_name == None and td_class_name[0] == "Jockey":
            jockey_url = td.find( "a" ).get( "href" )
            jockey_id = jockey_url.split( "/" )[-2]
            break
            
    return jockey_id

def trainer_idGet( td_tag ):
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
                weight = lib.textReplace( td.text )
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
                dist_data = lib.textReplace( span_tag[0].text ).replace( "m", "" )
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
                str_weather = lib.textReplace( div.text ).split( "/" )[2][-1]
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

def predict_netkeiba_pace( soup ):
    dl_tag = soup.findAll( 'dl' )

    for dl in dl_tag:
        class_name = dl.get( 'class' )

        if not class_name == None and \
          class_name[0] == 'RacePace':
            try:
                dd = dl.find( 'dd' )
                result = lib.textReplace( dd.text )
                break
            except:
                continue

    return lib.netkeibaPace( result )

def predict_netkeiba_deployment( soup ):
    result = []
    div_tag = soup.findAll( 'div' )

    for div in div_tag:
        class_name = div.get( 'class' )
        data_slick_index_name = div.get( 'data-slick-index' )
        
        if not class_name == None and \
          class_name[0] == 'DeployRace_SlideBoxItem':
            li_tag = div.findAll( "li" )
            count = 0
            key = ''
            instance_list = []

            for li in li_tag:
                dt = li.find( "dt" )

                if not dt == None:
                    if not len( key ) == 0:
                        result.append( copy.deepcopy( instance_list ) )
                        instance_list = []

                    key = lib.textReplace( dt.text )
                    continue

                try:
                    instance_list.append( int( lib.textReplace( li.find( "span" ).text ) ) )
                except:
                    continue
                
            break

    try:
        result.append( copy.deepcopy( instance_list ) )
    except:
        pass
        
    return result
