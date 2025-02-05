import SekitobaLibrary as lib
from data_manage import Storage
from data_collect.http_data_collect import *
from data_collect.driver_data_collect import *

def base_collect( storage: Storage ):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.today_data.race_id

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        tr_class_name = tr.get( "class" )

        if not tr_class_name == None \
          and 0 < len( tr_class_name ) \
          and tr_class_name[0] == "HorseList":
            td_tag = tr.findAll( "td" )
            horce_id = horce_id_get( td_tag )

            if horce_id in storage.current_horce_data:
                storage.current_horce_data[horce_id].weight = weight_get( td_tag )

def main( storage: Storage ):
    driver = lib.driver_start()
    driver = lib.login( driver )
    wide_odds_collect( storage, driver )

    for i in range( 0, 10 ):
        base_collect( storage )
        race_data_get.main( storage, driver )

        for horce_id in storage.current_horce_data.keys():
            if not storage.current_horce_data[horce_id].just_before_data_check():
                continue

        break
    
    driver.quit()
