import datetime
from bs4 import BeautifulSoup

from sekitoba_logger import logger
import sekitoba_library as lib
from data_manage.storage import Storage

def joceky_data_collect( jockey_id ):
    base_url = "https://db.netkeiba.com/?pid=jockey_detail&id=" + jockey_id + "&page="
    result = {}
    count = 1
    before_year = int( datetime.date.today().year ) - 1
    
    while 1:
        url = base_url + str( count )
        r,_  = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        tbody = soup.find( "tbody" )
        
        if tbody == None:
            break
        
        tr_tag = tbody.findAll( "tr" )

        if len( tr_tag ) == 0:
            break        
        else:
            for tr in tr_tag:
                td_tag = tr.findAll( "td" )
                key_day = td_tag[0].text
                key_race_num = td_tag[3].text
                try:
                    horce_id = td_tag[12].find( "a" ).get( "href" ).replace( "horse", "" ).replace( "/", "" )
                except:
                    horce_id = ""

                ymd = key_day.split( "/" )

                if not len( ymd ) == 3:
                    continue

                year = int( ymd[0] )
                
                if year < before_year:
                    return result
                elif before_year < year:
                    continue

                lib.dic_append( result, key_day, {} )
                lib.dic_append( result[key_day], key_race_num, {} )
                result[key_day][key_race_num]["place"] = td_tag[1].text
                result[key_day][key_race_num]["weather"] = td_tag[2].text
                result[key_day][key_race_num]["all_horce_num"] = td_tag[6].text
                result[key_day][key_race_num]["flame_num"] = td_tag[7].text
                result[key_day][key_race_num]["horce_num"] = td_tag[8].text
                result[key_day][key_race_num]["odds"] = td_tag[9].text
                result[key_day][key_race_num]["popular"] = td_tag[10].text
                result[key_day][key_race_num]["rank"] = td_tag[11].text
                result[key_day][key_race_num]["horce_id"] = horce_id
                result[key_day][key_race_num]["weight"] = td_tag[13].text
                result[key_day][key_race_num]["dist"] = td_tag[14].text
                result[key_day][key_race_num]["baba"] = td_tag[15].text
                result[key_day][key_race_num]["time"] = td_tag[16].text
                result[key_day][key_race_num]["diff"] = td_tag[17].text
                result[key_day][key_race_num]["passing"] = td_tag[18].text
                result[key_day][key_race_num]["pace"] = td_tag[19].text
                result[key_day][key_race_num]["up"] = td_tag[20].text
                
        count += 1
    
    return result

def jockey_year_rank( jockey_id ):
    url = "https://db.netkeiba.com/jockey/result/" + jockey_id
    result = {}
    r,_  = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        table_class = table.get( "class" )

        if not table_class == None and table_class[0] == "nk_tb_common":
            tr_tag = table.findAll( "tr" )

            for tr in tr_tag:
                td_tag = tr.findAll( "td" )

                if len( td_tag ) == 21:
                    year = 0

                    try:
                        year = int( lib.text_replace( td_tag[0].text ) )
                        rank = int( lib.text_replace( td_tag[1].text ) )
                    except:
                        continue

                    key_year = str( year )
                    result[key_year] = rank

    return result

def data_check( storage: Storage, horce_id ):
    first_name = "http_data_collect/jockey_data_collect"
    data_count = len( storage.data[horce_id]["jockey"] )
    horce_num = storage.data[horce_id]["horce_num"]
    
    if not data_count == 0:
        logger.info( "{} race_id:{} horce_num:{} data_count:{}".format( first_name, storage.race_id, horce_num, data_count ) )
    else:
        logger.warning( "{} race_id:{} horce_num:{} data_count:{}".format( first_name, storage.race_id, horce_num, data_count ) )

def main( storage: Storage ):
    base_url = "https://db.netkeiba.com/?pid=jockey_detail&id="
    jockey_year_base_url = "https://db.netkeiba.com/jockey/result/"
    
    for horce_id in storage.horce_id_list:
        jockey_id = storage.data[horce_id]["jockey_id"]
        storage.data[horce_id]["jockey"] = None
        storage.data[horce_id]["jockey_year_rank"] = None
        
        if jockey_id == None:
            continue
        
        url = base_url + jockey_id + "&page="
        storage.data[horce_id]["jockey"] = joceky_data_collect( url )
        storage.data[horce_id]["jockey_year_rank"] = jockey_year_rank( jockey_year_base_url + jockey_id )
        data_check( storage, horce_id )
        #logger.info( )
