from selenium import webdriver

from data_manage.storage import Storage
from http_data_collect import base_race_collect
from driver_data_collect import race_data_get

def main( storage: Storage ):
    driver = webdriver.Chrome( '/Users/kansei/Downloads/chromedriver_mac64/chromedriver' )
    base_race_collect.main( storage, before = True )
    race_data_get.main( storage, driver )
