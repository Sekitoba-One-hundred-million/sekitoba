from bs4 import BeautifulSoup

import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def race_money_get( race_id ):
    money = 0
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
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
