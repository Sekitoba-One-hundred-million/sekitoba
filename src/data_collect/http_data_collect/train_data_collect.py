import time
import datetime
from bs4 import BeautifulSoup

from SekitobaLogger import logger
import SekitobaLibrary as lib
import copy

from data_manage import Storage
from data_manage import TrainData
    
def train_collect( storage: Storage ):
    best_check_count = 0
    continue_count = 0
    instance_train_data_dict = {}
    cookie = lib.netkeiba_login()
    url = "https://race.netkeiba.com/race/oikiri.html?race_id=" + storage.today_data.race_id

    for i in range( 0, 10 ):
        if best_check_count == storage.all_horce_num or \
          continue_count == 3:
            break

        r, _ = lib.request( url, cookie = cookie )
        soup = BeautifulSoup( r.content, "html.parser" )
        ul_tag = soup.findAll( "ul" )
        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            class_name = tr.get( "class" )

            if not class_name == None \
            and "OikiriDataHead" in class_name[0]:
                td_tag = tr.findAll( "td" )

                if len( td_tag ) < 13:
                    continue

                key_horce_num = lib.text_replace( td_tag[1].text )
                li_tag = td_tag[8].findAll( "li" )
                train_data = TrainData()
                train_data.cource = lib.text_replace( td_tag[5].text )
                train_data.load = td_tag[10].text
                train_data.critic = td_tag[11].text
                train_data.rank = td_tag[12].text

                for li in li_tag:
                    text_list = li.text.replace( ")", "" ).split( "(" )

                    if not len( text_list ) == 2:
                        continue

                    train_time = text_list[0]
                    wrap_time = text_list[1]

                    try:
                        train_data.time.append( float( train_time ) )
                        train_data.wrap.append( float( wrap_time ) )
                    except:
                        continue

                storage.train_data[key_horce_num] = train_data

        check_count = 0
        for horce_num_key in storage.train_data.keys():
            if storage.train_data[horce_num_key].data_check():
                check_count += 1

        if best_check_count < check_count:
            instance_train_data_dict = copy.deepcopy( storage.train_data )
            best_check_count = check_count
        elif best_check_count == check_count:
            continue_count += 1

    storage.train_data = instance_train_data_dict
