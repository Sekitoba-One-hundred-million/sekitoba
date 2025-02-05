import SekitobaLibrary as lib
from SekitobaLogger import logger

import config
from data_manage.storage import Storage
from select_buy.buy_lib import *

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
    
def oneSelect( driver, bd ):
    betMoney = int( bd["count"] * 100 )
        
    #馬の選択
    horce_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/bet-basic-win-basic/table/tbody/tr[' + str( bd["horce_num"] ) + ']/td[2]/label'
    driver.find_element( By.XPATH, horce_xpath ).click()
    time.sleep( 1 )

    driver = setMoney( driver, bet_money)

    return driver

def wideSelect( driver, bd ):
    all_money = 0
    money_table = { "7": "21", "8": "22", "9": "23", "4": "31", "5": "32", "6": "33", "1": "41", "2": "42", "3": "43", "0": "51" }

    betMoney = bd["count"] * 100

    for horceNum in bd["horce_num"]:
        #馬の選択
        horce_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/div/span/bet-basic-quinellaplace-basic/table/tbody/tr[' + str( horceNum ) + ']/td[2]/label'
        driver.find_element( By.XPATH, horce_xpath ).click()
        time.sleep( 1 )

    driver = setMoney( driver, betMoney )

    return driver

def autoBuy( storage: Storage, buyData ):
    driver = lib.driver_start()
    haveMoney, driver = loginGetMoney( driver )

    if haveMoney == lib.escapeValue:
        logger.fatal( "not get have_money" )
        return

    driver = moveVotePage( storage, driver )

    for bd in buyData:
        kind = bd["kind"]
        driver = selectTicket( driver, kind )

        if kind == "one":
            driver = oneSelect( driver, bd )
        elif kind == "wide":
            driver = wideSelect( driver, bd )
    
    time.sleep( 300 )
    driver.quit()
    return
