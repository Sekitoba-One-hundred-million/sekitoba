from bs4 import BeautifulSoup

from data_manage.storage import Storage
import sekitoba_library as lib
from sekitoba_logger import logger

def past_horce_data_get( soup ):
    horce_data = []
    tr_tag = soup.findAll( "tr" )
    
    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = lib.text_replace( td_tag[r].text )

                    if not r == 27:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )
    
    return horce_data

def time_index_get( soup ):
    time_inedx_data = []
    tr_tag = soup.findAll( "tr" )
    
    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            try:
                #str_birthday = lib.text_replace( td_tag[0].text )
                str_time_index = lib.text_replace( td_tag[19].text )
                time_inedx_data.append( lib.math_check( str_time_index ) )
            except:
                continue

    return time_inedx_data

def baba_index_get( soup ):
    baba_inedx_data = {}
    tr_tag = soup.findAll( "tr" )
    
    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            try:
                str_birthday = lib.text_replace( td_tag[0].text )
                str_baab_index = lib.text_replace( td_tag[16].text )
                baba_inedx_data[str_birthday] = lib.math_check( str_baab_index )
            except:
                continue

    return baba_inedx_data

def parent_id_get( soup ):
    parent_id = { "father": "", "mother": "" }
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        class_name = table.get( "class" )

        if not class_name == None and class_name[0] == "blood_table":
            td_tag = table.findAll( "td" )

            if not len( td_tag ) == 6:
                break

            try:
                parent_id["father"] = td_tag[0].find( "a" ).get( "href" ).split( "/" )[-2]
                parent_id["mother"] = td_tag[3].find( "a" ).get( "href" ).split( "/" )[-2]
            except:
                break

    return parent_id

def data_check( storage: Storage, horce_id ):
    first_name = "http_data_collect/horce_data_get"
    check_data_name = [ "time_index", "baba_index" ]
    horce_num = storage.data[horce_id]["horce_num"]
    
    for data_key in check_data_name:
        if not len( storage.data[horce_id][data_key] ) == 0:
            logger.info( "{} race_id:{} horce_num:{} {}:{}".format( first_name, storage.race_id, horce_num, data_key, storage.data[horce_id][data_key] ) )
        else:
            logger.warning( "{} fail race_id:{} horce_num:{} {}".format( first_name, storage.race_id, horce_num, data_key ) )

    if not len( storage.past_data[horce_id].past_data ) == 0:
        logger.info( "{} race_id:{} horce_num:{} past_data:{}".format( first_name, storage.race_id, horce_num, len( storage.data[horce_id][data_key] ) ) )
    else:
        logger.warning( "{} fail race_id:{} horce_num:{} past_data".format( first_name, storage.race_id, horce_num ) )
    
def main( storage: Storage ):
    cookie = lib.netkeiba_login()
    base_url = "https://db.netkeiba.com/horse/"
    
    for horce_id in storage.horce_id_list:
        url = base_url + horce_id
        r, _ = lib.request( url, cookie = cookie )
        soup = BeautifulSoup( r.content, "html.parser" )
        storage.data[horce_id]["time_index"] = time_index_get( soup )
        storage.data[horce_id]["baba_index"] = baba_index_get( soup )
        storage.data[horce_id]["parent_id"] = parent_id_get( soup )
        storage.past_data[horce_id] = lib.past_data( past_horce_data_get( soup ), [] )
        data_check( storage, horce_id )
        

    # parent horce data get
    for horce_id in storage.horce_id_list:
        for fm in storage.data[horce_id]["parent_id"]:
            parent_id = storage.data[horce_id]["parent_id"][fm]
            lib.dic_append( storage.data, parent_id, {} )

            url = base_url + parent_id
            r, _ = lib.request( url, cookie = cookie )
            soup = BeautifulSoup( r.content, "html.parser" )
            #storage.data[parent_id]["time_index"] = time_index_get( soup )
            #storage.data[parent_id]["baba_index"] = baba_index_get( soup )
            storage.past_data[parent_id] = lib.past_data( past_horce_data_get( soup ), [] )
