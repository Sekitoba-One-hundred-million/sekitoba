import sekitoba_library as lib
from sekitoba_logger import logger

import config
from today_data_get.data_get import TodayData

import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

def login( driver ):
    driver.get('https://www.ipat.jra.go.jp/')

    time.sleep(2)
    id_box = driver.find_element_by_name("inetid")
    id_box.send_keys( config.important_data.id )
    #time.sleep(5)
    id_box.submit()
    time.sleep(3)
    
    member_box = driver.find_element_by_name( "i" )
    member_box.send_keys( config.important_data.member )

    password_box = driver.find_element_by_name( "p" )
    password_box.send_keys( config.important_data.password )

    pars_box = driver.find_element_by_name( "r" )
    pars_box.send_keys( config.important_data.pars )

    driver.find_element_by_class_name( "buttonModern" ).click()
    
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

def quinella_button_num_get( driver ):
    num = 0
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    select_tag = soup.findAll( "select" )

    for select in select_tag:
        id_name = select.get( "id" )
        
        if not id_name == None and id_name == "bet-basic-type":
            option_tag = select.findAll( "option" )
            
            for i in range( 0, len( option_tag ) ):
                num += 1
                label = option_tag[i].get( "label" )
                
                if not label == None and label == "馬連":
                    num -= 1
                    break
            
    return num

def one_buy( buy_data_list, today_data: TodayData ):
    have_money = None
    driver = webdriver.Chrome()

    for i in range( 0, 5 ):
        driver = login( driver )
        time.sleep( 5 )

        try:
            driver.find_element_by_xpath( '//*[@id="main"]/ui-view/div[2]/div[2]/button' ).click()
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
    driver.find_element_by_css_selector( ".btn.btn-default.btn-lg.btn-block.btn-size" ).click()
    time.sleep( 5 )
    
    place = today_data.place
    race_num = str( today_data.num ) + "R"
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    number = place_button_num_get( soup, place )

    if not number == 1:
        place_button_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/select-course-race/div/div[2]/div[2]/div[2]/div[1]/div[{}]/button'.format( number )
        driver.find_element_by_xpath( place_button_xpath ).click()

    time.sleep( 2 )
    aa = driver.find_elements_by_css_selector( ".btn.btn-default.btn-lg.btn-block" )

    for i in range( 0, len( aa ) ):
        check_text = aa[i].text.split( " " )
        if not len( check_text ) == 0 \
           and check_text[0] == race_num:
            aa[i].click()
            break

    time.sleep( 5 )
    all_money = 0
    money_table = { "7": "21", "8": "22", "9": "23", "4": "31", "5": "32", "6": "33", "1": "41", "2": "42", "3": "43", "0": "51" }

    for buy_data in buy_data_list:
        bet_money = max( int( buy_data["rate"] * have_money * 0.25 ), 1 )
        buy_data["money"] = int( bet_money )
        
        #馬の選択
        horce_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/bet-basic-win-basic/table/tbody/tr[' + str( buy_data["horce_num"] ) + ']/td[2]/label'
        driver.find_element_by_xpath( horce_xpath ).click()
        time.sleep( 1 )

        dentaku_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/button'
        driver.find_element_by_xpath( dentaku_xpath ).click()
        time.sleep( 1 )

        #電卓操作で金額の入力
        for m in str( bet_money ):
            money_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/div[{}]/button[{}]'.format( money_table[m][0], money_table[m][1] )
            driver.find_element_by_xpath( money_xpath ).click()
            time.sleep( 1 )

        math_set_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/button'
        driver.find_element_by_xpath( math_set_xpath ).click()

        time.sleep( 1 )
        set_xpath ='/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[2]'
        driver.find_element_by_xpath( set_xpath ).click()

        all_money += int( bet_money * 100 )
        time.sleep( 2 )

    finish_button = driver.find_element_by_xpath( '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[3]' )
    finish_button.click()
    
    time.sleep( 3 )
    #all_money_form = driver.find_element_by_xpath( '//*[@id="bet-list-top"]/div[4]/table/tbody/tr[4]/td/input' )
    all_money_form_xpath = '/html/body/div[1]/ui-view/navbar/div/div/ng-transclude/bet-list/div[1]/bet-list-cart/div/sticky-scroll/div/div[5]/table/tbody/tr[{}]/td/input'.format( len( buy_data_list ) + 3 )
    driver.find_element_by_xpath( all_money_form_xpath ).send_keys( str( all_money ) )

    #buy_button = driver.find_element_by_xpath( '//*[@id="bet-list-top"]/div[4]/table/tbody/tr[5]/td/button' )
    buy_button_xpath = '//*[@id="bet-list-top"]/div[5]/table/tbody/tr[{}]/td/button'.format( len( buy_data_list ) + 4 )
    driver.find_element_by_xpath( buy_button_xpath ).click()
    time.sleep( 5 )
    
    ok_button = driver.find_element_by_xpath( '/html/body/error-window/div/div/div[3]/button[1]' )
    ok_button.click()

    time.sleep( 5 )
    driver.quit()


def quinella_buy( buy_data_list, today_data: TodayData ):
    money = 1#int( 100 * len( result["number"] ) )
    driver = webdriver.Chrome()
    driver = login( driver )
    time.sleep( 5 )

    try:
        driver.find_element_by_xpath( '//*[@id="main"]/ui-view/div[2]/div[2]/button' ).click()
        time.sleep( 5 )
    except:
        time.sleep( 1 )

    # 通常投票ボタン
    driver.find_element_by_css_selector( ".btn.btn-default.btn-lg.btn-block.btn-size" ).click()
    time.sleep( 5 )
    
    place = today_data.place
    race_num = str( today_data.num ) + "R"
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    number = place_button_num_get( soup, place )

    if not number == 1:
        place_button_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/select-course-race/div/div[2]/div[2]/div[2]/div[1]/div[{}]/button'.format( number )
        driver.find_element_by_xpath( place_button_xpath ).click()

    time.sleep( 2 )
    aa = driver.find_elements_by_css_selector( ".btn.btn-default.btn-lg.btn-block" )

    for i in range( 0, len( aa ) ):
        check_text = aa[i].text.split( " " )
        if not len( check_text ) == 0 \
           and check_text[0] == race_num:
            aa[i].click()
            break

    time.sleep( 5 )

    #馬連を選択
    buy_kind_select_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[2]/select'
    buy_kind_num = quinella_button_num_get( driver )
    Select( driver.find_element_by_xpath( buy_kind_select_xpath ) ).select_by_index( buy_kind_num )
    time.sleep( 2 )
    
    all_money = 0
    money_table = { "7": "21", "8": "22", "9": "23", "4": "31", "5": "32", "6": "33", "1": "41", "2": "42", "3": "43", "0": "51" }

    for buy_data in buy_data_list:
        #馬の選択
        horce1_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/div/span/bet-basic-quinella-basic/table/tbody/tr[{}]/td[2]/label'.format( str( buy_data["horce_num_1"] ) )
        driver.find_element_by_xpath( horce1_xpath ).click()

        horce2_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/div/div/span/div/span/bet-basic-quinella-basic/table/tbody/tr[{}]/td[2]/label'.format( str( buy_data["horce_num_2"] ) )
        driver.find_element_by_xpath( horce2_xpath ).click()
        time.sleep( 1 )

        dentaku_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/button'
        driver.find_element_by_xpath( dentaku_xpath ).click()
        time.sleep( 1 )

        #電卓操作で金額の入力
        for m in str( buy_data["money"] ):
            money_xpath = '/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/div[{}]/button[{}]'.format( money_table[m][0], money_table[m][1] )
            driver.find_element_by_xpath( money_xpath ).click()
            time.sleep( 1 )

        math_set_xpath = '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[1]/ten-key/div/div/div[2]/button'
        driver.find_element_by_xpath( math_set_xpath ).click()

        time.sleep( 1 )
        set_xpath ='/html/body/div[1]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[2]'
        driver.find_element_by_xpath( set_xpath ).click()

        all_money += int( buy_data["money"] * 100 )
        time.sleep( 2 )

    finish_button = driver.find_element_by_xpath( '//*[@id="main"]/ui-view/div[2]/ui-view/main/div/div[3]/select-list/div/div/div[3]/div[4]/button[3]' )
    finish_button.click()
    
    time.sleep( 3 )
    all_money_form_xpath = '/html/body/div[1]/ui-view/navbar/div/div/ng-transclude/bet-list/div[1]/bet-list-cart/div/sticky-scroll/div/div[5]/table/tbody/tr[{}]/td/input'.format( len( buy_data_list ) + 3 )
    driver.find_element_by_xpath( all_money_form_xpath ).send_keys( str( all_money ) )

    buy_button_xpath = '//*[@id="bet-list-top"]/div[5]/table/tbody/tr[{}]/td/button'.format( len( buy_data_list ) + 4 )
    driver.find_element_by_xpath( buy_button_xpath ).click()
    time.sleep( 5 )
    
    ok_button = driver.find_element_by_xpath( '/html/body/error-window/div/div/div[3]/button[1]' )
    ok_button.click()

    time.sleep( 5 )
    driver.quit()
