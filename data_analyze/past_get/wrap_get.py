from bs4 import BeautifulSoup

import sekitoba_library as lib
from data_manage.storage import Storage
from config import name

def wrap_get( race_id ):
    wrap_data = {}
    url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        summary = table.get( "summary" )

        if not summary == None \
           and summary == "ラップタイム":
            tr_tag = table.findAll( "tr" )
            dist_data = tr_tag[0].findAll( "th" )
            wrap_time = tr_tag[2].findAll( "td" )

            for i in range( 0, len( dist_data ) ):
                dist = dist_data[i].text.replace( "m", "" )
                wrap = float( wrap_time[i].text )
                wrap_data[dist] = wrap

    return wrap_data
