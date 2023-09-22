import sekitoba_library as lib
from data_manage import Storage
from data_collect.http_data_collect import *
from data_collect.driver_data_collect import *

def base_collect( storage: Storage ):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.today_data.race_id

    for i in range( 0, 10 ):
        r, _ = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )

        if not storage.before_data_check():
            storage.dist = dist_race_kind_get( soup )
            storage.outside = outside_get( soup )
            storage.weather = weather_get( soup )
            storage.baba = baba_get( soup )
            storage.race_money = race_money_get( soup )

        tr_tag = soup.findAll( "tr" )

        for tr in tr_tag:
            tr_class_name = tr.get( "class" )

            if not tr_class_name == None and tr_class_name[0] == "HorseList":
                td_tag = tr.findAll( "td" )
                horce_id = horce_id_get( td_tag )
                current_horce_data = CurrentHorceData()
                current_horce_data.horce_num = horce_number_get( td_tag )
                current_horce_data.waku_num = waku_number_get( td_tag )
                current_horce_data.age = age_get( td_tag )
                current_horce_data.sex = sex_get( td_tag )
                current_horce_data.burden_weight = burden_weight_get( td_tag )
                current_horce_data.jockey_id = joceky_id_get( td_tag )
                current_horce_data.trainer_id = trainer_id_get( td_tag )
                storage.current_horce_data[horce_id] = current_horce_data

                if not horce_id in storage.horce_id_list:
                    storage.horce_id_list.append( horce_id )
                
        storage.all_horce_num = len( storage.horce_id_list )
        current_horce_data_check = False

        for horce_id in storage.current_horce_data.keys():
            current_horce_data_check = storage.current_horce_data[horce_id].before_data_check()

        if storage.before_data_check() and \
          current_horce_data_check:
            break


def main( storage: Storage ):
    base_collect( storage )
    train_collect( storage )

    #driver = lib.driver_start()
    #omega_get.main( storage, driver )
    #driver.close()