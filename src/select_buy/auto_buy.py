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

def quinella_buy( driver, bd ):
    all_money = 0
    money_table = { "7": "21", "8": "22", "9": "23", "4": "31", "5": "32", "6": "33", "1": "41", "2": "42", "3": "43", "0": "51" }

    betMoney = bd["count"] * 100

    for horce_num in bd["horce_num"]:
        #馬の選択
        horce_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/div/span/bet-basic-quinella-basic/table/tbody/tr[' + str( horce_num ) + ']/td[2]/label'
        element = driver.find_element( By.XPATH, horce_xpath )

        #if horce_num < 5:
        #    driver.execute_script("window.scrollTo(0, 0);")

        driver.execute_script( "arguments[0].click();", element )
        time.sleep( 1 )

    driver = setMoney( driver, betMoney )

    return driver

def autoBuy( storage: Storage, betData, driver ):
    haveMoney, driver = loginGetMoney( driver )

    if haveMoney == lib.escapeValue:
        logger.fatal( "not get have_money" )
        return

    bet_money = 0
    driver = moveVotePage( storage, driver )
    driver = selectTicket( driver, "quinella" )

    for bd in betData:
        driver = quinella_buy( driver, bd )
        bet_money += bd["count"]

    bet_money = int( bet_money * 100 )
    finishClick( driver, bet_money )
    return driver
