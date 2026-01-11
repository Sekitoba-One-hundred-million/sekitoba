import SekitobaLibrary as lib

from config import data_name

from test_config.config import *

from data_manage import Storage
from data_manage import TodayData
from data_create import DataCreate
from predict.predict_result import passing_rank_analyze

from data_collect import before_data_collect
from data_collect import just_before_data_collect

from test_predict import race_pace_simulation
from test_predict import train_score
from test_predict import first_passing_rank
from test_predict import last_passing_rank
from test_predict import up3
from test_predict import rank_score
from test_predict import rough_race
from test_predict import recovery_score

def data_check():
    test_race_id = "202406040904"#test_today_data_race_id_list[0]
    test_day = datetime.datetime( 2024, 9, 29 )
    today_data = TodayData( test_race_id, test_day )
    storage = Storage( today_data )
    driver = lib.driver_start()
    driver = lib.login( driver )
    before_data_collect.main( storage, driver ) # http通信のスクレイピングで入手するデータ
    just_before_data_collect.main( storage, driver )
    data_create = DataCreate( storage )
    data_create.create()

    race_pace_data = race_pace_simulation.data_check( test_race_id, data_create.analyze_data )

    for horce_id in data_create.analyze_data.keys():
        for key in race_pace_data.keys():
            data_create.analyze_data[horce_id]["predict_"+key] = race_pace_data[key]

    first_passing_rank_data = first_passing_rank.data_check( test_race_id, data_create.analyze_data )

    for horce_id in first_passing_rank_data.keys():
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank] = first_passing_rank_data[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_index] = first_passing_rank_data[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_stand] = first_passing_rank_data[horce_id]["stand"]

    last_passing_rank_data = last_passing_rank.data_check( test_race_id, data_create.analyze_data )

    for horce_id in last_passing_rank_data.keys():
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank] = last_passing_rank_data[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_index] = last_passing_rank_data[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_stand] = last_passing_rank_data[horce_id]["stand"]

    up3_data = up3.data_check( test_race_id, data_create.analyze_data )

    for horce_id in up3_data.keys():
        data_create.analyze_data[horce_id][data_name.predict_up3] = up3_data[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_up3_stand] = up3_data[horce_id]["stand"]

    rank_score.data_check( test_race_id, data_create.analyze_data )
    recovery_score.data_check( test_race_id, data_create.analyze_data )
    return
