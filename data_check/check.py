from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
import sekitoba_data_manage as dm

from data_manage.storage import Storage
from http_data_collect import base_race_collect

STOCKDATA = "stock_data.pickle"

def bace_race_data_check( storage: Storage ):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + storage.race_id
    check = True

    while 1:
        # dist race_moneyは必ず取れるので取れていないとおかしい httpでのrequestが失敗していたと判断
        if storage.dist == None or storage.race_money == None:
            str_log = "not_get_data {} {}R".format( storage.today_data.place, storage.today_data.num )
            print( str_log )
            logger.info( str_log )
            base_race_collect.main( storage )
            check = False

    return check

def http_data_check( stock_data: dict[ str, Storage ] ):
    count = 0
    
    for k in stock_data.keys():
        check = True
        check = bace_race_data_check( stock_data[k] )

        if not check:
            dm.pickle_upload( STOCKDATA, stock_data, prod = True )
