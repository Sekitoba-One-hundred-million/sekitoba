import time
from selenium import webdriver
from bs4 import BeautifulSoup

import sekitoba_library as lib

def main():
    result = []
    url = "https://race.netkeiba.com/top/"
    driver = webdriver.Chrome()

    driver, _ = lib.driver_request( driver, url )        
    time.sleep( 5 )

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )

    p_tag = soup.findAll( "p" )

    for p in p_tag:
        instance = {}
        class_name = p.get( "class" )
        if not class_name == None \
           and class_name[0] == "RaceList_DataTitle":
            text_data = p.text.split( " " )
            instance["place"] = text_data[1]
            
            instance["number"] = ""
            instance["day"] = ""

            for i in range( 0, len( text_data[0] ) ):
                if str.isdecimal( text_data[0][i] ):
                    instance["number"] += text_data[0][i]

            for i in range( 0, len( text_data[2] ) ):
                if str.isdecimal( text_data[2][i] ):
                    instance["day"] += text_data[2][i]

            result.append( instance )

    driver.close()

    return result
    
