from bs4 import BeautifulSoup

import sekitoba_library as lib
from sekitoba_logger import logger
from data_manage.storage import Storage
from http_data_collect import horce_data_get
from http_data_collect import base_race_collect
from http_data_collect import jockey_data_collect
from http_data_collect import trainer_data_collect
from http_data_collect import train_data_collect

def main( storage: Storage ):
    logger.info( "start race_id:{} http_data_collect".format( storage.race_id ) )
    base_race_collect.main( storage )
    horce_data_get.main( storage )
    train_data_collect.main( storage )
    #jockey_data_collect.main( storage )
    #trainer_data_collect.main( storage )
    logger.info( "finish race_id:{} http_data_collect".format( storage.race_id ) )
