import datetime
from bs4 import BeautifulSoup

from sekitoba_logger import logger
import sekitoba_library as lib
from data_manage.storage import Storage

def main( storage: Storage ):
    storage.data["train"] = {}
    cookie = lib.netkeiba_login()
    url = "https://race.netkeiba.com/race/oikiri.html?race_id=" + storage.race_id
    r, _ = lib.request( url, cookie = cookie )
    soup = BeautifulSoup( r.content, "html.parser" )
    ul_tag = soup.findAll( "ul" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None \
          and "OikiriDataHead" in class_name[0]:
            td_tag = tr.findAll( "td" )
            
            if not len( td_tag ) == 13:
                continue

            key = lib.text_replace( td_tag[1].text )
            lib.dic_append( storage.data["train"], key, { "time": [], "wrap": [], "load": "", "critic": "", "rank": "", "cource": ""  } )
            li_tag = td_tag[8].findAll( "li" )
            storage.data["train"][key]["cource"] = td_tag[5].text
            storage.data["train"][key]["load"] = td_tag[10].text
            storage.data["train"][key]["critic"] = td_tag[11].text
            storage.data["train"][key]["rank"] = td_tag[12].text

            for li in li_tag:
                text_list = li.text.replace( ")", "" ).split( "(" )

                if not len( text_list ) == 2:
                    continue

                train_time = text_list[0]
                wrap_time = text_list[1]

                try:
                    storage.data["train"][key]["time"].append( float( train_time ) )
                    storage.data["train"][key]["wrap"].append( float( wrap_time ) )
                except:
                    continue
