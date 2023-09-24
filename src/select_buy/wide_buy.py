import sekitoba_library as lib
from sekitoba_logger import logger

import config
from data_manage import Storage

import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def login( driver ):
    driver.get('https://www.ipat.jra.go.jp/')

    time.sleep(2)
    id_box = driver.find_element( By.NAME, "inetid")
    id_box.send_keys( config.important_data.id )
    #time.sleep(5)
    id_box.submit()
    time.sleep(3)
    
    member_box = driver.find_element( By.NAME, "i" )
    member_box.send_keys( config.important_data.member )

    password_box = driver.find_element( By.NAME, "p" )
    password_box.send_keys( config.important_data.password )

    pars_box = driver.find_element( By.NAME, "r" )
    pars_box.send_keys( config.important_data.pars )

    driver.find_element( By.CLASS_NAME, "buttonModern" ).click()
    
    return driver

def money_get( driver ):
    money = 0
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    td_tag = soup.findAll( "td" )

    for td in td_tag:
        class_name = td.get( "class" )

        if not class_name == None and \
          len( class_name ) == 3 and \
          class_name[0] == "text-lg" and \
          class_name[1] == "text-right" and \
          class_name[2] == "ng-binding":
            str_money = td.text
            money = ""

            for sm in str_money:
                if str.isdecimal( sm ):
                    money += sm

            if len( money ) == 0:
                return None

            money = int( money )
            money = int( money / 100 )

    return money

def place_button_num_get( soup, place ):
    place_num = 0
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None and len( class_name ) == 1 and class_name[0] == "place-name":
            place_num += 1
            
            if place in lib.text_replace( div.text ):
                break

    return place_num

def wide_buy( buy_data_list, storage: Storage ):
    driver = lib.driver_start()
    driver = login( driver )
