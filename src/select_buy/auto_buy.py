import SekitobaLibrary as lib
from SekitobaLogger import logger

import config
from data_manage.storage import Storage

import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def login( driver ):
    driver.get('https://www.ipat.jra.go.jp/')
    
    time.sleep(2)
    id_box = driver.find_element( By.NAME, "inetid")
    id_box.send_keys( config.im_data.id )
    #time.sleep(5)
    id_box.submit()
    time.sleep(3)
    
    member_box = driver.find_element( By.NAME, "i" )
    member_box.send_keys( config.im_data.member )

    password_box = driver.find_element( By.NAME, "p" )
    password_box.send_keys( config.im_data.password )

    pars_box = driver.find_element( By.NAME, "r" )
    pars_box.send_keys( config.im_data.pars )

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
            
            if place in lib.textReplace( div.text ):
                break

    return place_num

def one_buy( storage: Storage, buy_data ):
    have_money = None
    driver = lib.driverStart()

    for i in range( 0, 5 ):
        driver = login( driver )

        try:
            driver.find_element( By.XPATH, '/html/body/div[1]/ui-view/div[2]/div[2]/button' ).click()
            time.sleep( 5 )
        except:
            time.sleep( 1 )

        try:
            driver.find_element( By.XPATH, '//*[@id="main"]/ui-view/div[2]/div[2]/button' ).click()
            time.sleep( 5 )
        except:
            time.sleep( 1 )

        have_money = money_get( driver )
        
        if not have_money == None:
            break
        
    if have_money == None:
        logger.fatal( "not get have_money" )
        return

    # 通常投票ボタン
    driver.find_element( By.CSS_SELECTOR, ".btn.btn-default.btn-lg.btn-block.btn-size" ).click()
    time.sleep( 5 )

    place = storage.today_data.place
    race_num = str( storage.today_data.num ) + "R"
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    number = place_button_num_get( soup, place )

    if not number == 1:
        place_button_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/select-course-race/div/div[2]/div[2]/div[2]/div[1]/div[{}]/button'.format( number )
        driver.find_element( By.XPATH, place_button_xpath ).click()

    time.sleep( 2 )
    aa = driver.find_elements( By.CSS_SELECTOR, ".btn.btn-default.btn-lg.btn-block" )

    for i in range( 0, len( aa ) ):
        check_text = aa[i].text.split( " " )
        if not len( check_text ) == 0 \
           and check_text[0] == race_num:
            aa[i].click()
            break

    time.sleep( 5 )
    all_money = 0
    money_table = { "7": "21", "8": "22", "9": "23", "4": "31", "5": "32", "6": "33", "1": "41", "2": "42", "3": "43", "0": "51" }

    bet_money = int( int( buy_data["bet_count"] * storage.base_money * 0.005 ) * 100 )
    buy_data["money"] = int( bet_money )
        
    #馬の選択
    horce_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/bet-basic-win-basic/table/tbody/tr[' + str( buy_data["horce_num"] ) + ']/td[2]/label'
    driver.find_element( By.XPATH, horce_xpath ).click()
    time.sleep( 1 )

    dentaku_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/button'
    driver.find_element( By.XPATH, dentaku_xpath ).click()
    time.sleep( 1 )

    #電卓操作で金額の入力
    for m in str( bet_money ):
        money_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/div[{}]/button[{}]'.format( money_table[m][0], money_table[m][1] )
        driver.find_element( By.XPATH, money_xpath ).click()
        time.sleep( 1 )

    math_set_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/button'
    driver.find_element( By.XPATH, math_set_xpath ).click()

    time.sleep( 1 )
    set_xpath ='/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[2]'
    driver.find_element( By.XPATH, set_xpath ).click()

    time.sleep( 2 )

    finish_button = driver.find_element( By.XPATH, '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[3]' )
    finish_button.click()
    
    time.sleep( 3 )
    #all_money_form = driver.find_element_by_xpath( '//*[@id="bet-list-top"]/div[4]/table/tbody/tr[4]/td/input' )
    all_money_form_xpath = '/html/body/div[1]/ui-view/navbar/div/div/ng-transclude/bet-list/div[1]/bet-list-cart/div/sticky-scroll/div/div[5]/table/tbody/tr[{}]/td/input'.format( 4 )
    driver.find_element( By.XPATH, all_money_form_xpath ).send_keys( str( bet_money ) )

    #buy_button = driver.find_element_by_xpath( '//*[@id="bet-list-top"]/div[4]/table/tbody/tr[5]/td/button' )
    buy_button_xpath = '//*[@id="bet-list-top"]/div[5]/table/tbody/tr[{}]/td/button'.format( 5 )
    driver.find_element( By.XPATH, buy_button_xpath ).click()
    time.sleep( 5 )
    
    ok_button = driver.find_element( By.XPATH, '/html/body/error-window/div/div/div[3]/button[1]' )
    ok_button.click()

    time.sleep( 5 )
    driver.quit()
