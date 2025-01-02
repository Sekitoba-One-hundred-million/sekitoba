import time
import datetime
from bs4 import BeautifulSoup

from SekitobaLogger import logger
import SekitobaLibrary as lib
import copy

from data_manage import Storage
from data_manage import TrainData

def parent_id_collect( url ):
    father_id = ""
    mother_id = ""
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td_tag = soup.findAll( "td" )

    for td in td_tag:
        rowspan = td.get( "rowspan" )

        if not rowspan == None \
          and rowspan == "2":
            a = td.find( "a" )
            p_id = a.get( "href" ).split( "/" )[3]
            
            if len( father_id ) == 0:
                father_id = p_id
            else:
                mother_id = p_id

    return father_id, mother_id

def horce_data_collect( storage: Storage ):
    base_url = "https://db.netkeiba.com/horse/{}"

    for horce_id in storage.horce_id_list:
        storage.current_horce_data[horce_id].father_id, storage.current_horce_data[horce_id].mother_id = \
          parent_id_collect( base_url.format( horce_id ) )
