import datetime
from bs4 import BeautifulSoup

from sekitoba_logger import logger
import sekitoba_library as lib
from data_manage.storage import Storage

blood = { "#C4F2F9": 1, "#C6FFAA": 2, "#E0B7FF": 3, "#FFA6E2": 4,  "#FFD28E": 5, "#E8BF9B": 6, "#FFF99": 7, "#DDDDDD": 8 }

def main( storage: Storage ):
    storage.data["father_blood_type"] = {}
    cookie = lib.netkeiba_login()
    url = "https://race.netkeiba.com/race/bias.html?race_id=" + storage.race_id
    r, _ = lib.request( url, cookie = cookie )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )
            
        if not class_name == None and len( class_name ) == 2 and class_name[0] == "List" and class_name[1] == "HorseList":
            td_tag = tr.findAll( "td" )

            try:
                horce_id = td_tag[3].find( "a" ).get( "href" ).split( "/" )[-1]
                father_style = td_tag[4].get( "style" ).replace( "background:", "" ).replace( ";", "" )
                storage.data["father_blood_type"][horce_id] = blood[father_style]
            except:
                continue
