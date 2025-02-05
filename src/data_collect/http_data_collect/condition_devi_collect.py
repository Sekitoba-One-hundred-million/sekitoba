import time
import datetime
from bs4 import BeautifulSoup

from SekitobaLogger import logger
import SekitobaLibrary as lib
import copy

from data_manage import Storage
from data_manage import TrainData
    
def condition_devi_collect( storage: Storage ):
    best_check_count = 0
    continue_count = 0
    instance_train_data_dict = {}
    url = "https://race.sp.netkeiba.com/barometer/score.html?race_id=" + storage.today_data.race_id
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None and \
          len( class_name ) == 2 and \
          class_name[0] == "HorseList":
            td_tag = tr.findAll( "td" )
            try:
                a_tag = td_tag[2].find( "a" )
                horce_id = a_tag.get( "href" ).split( "&" )[0].split( "horse_id=" )[-1]
                span_tag = td_tag[3].findAll( "span" )
                condition_devi = float( lib.text_replace( span_tag[0].text ) )
                storage.condition_devi[horce_id] = condition_devi
            except:
                continue
