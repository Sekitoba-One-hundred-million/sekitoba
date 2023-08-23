from selenium import webdriver

import sekitoba_library as lib
from data_manage.storage import Storage
from driver_data_collect import race_data_get
from driver_data_collect import omega_get

def main( storage: Storage ):
    driver = webdriver.Chrome( '/Users/kansei/Downloads/chromedriver_mac64/chromedriver' )

    race_data_get.main( storage, driver )
    omega_get.main( storage, driver )
    driver.close()
