from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

from data_manage import Storage

# 1: サンダーサイレンス
# 2: ターントゥ
# 3: ノーザンダンサー
# 4: ナスルーラ
# 5: ネイティヴダンサー
# 6: ハンプトン
# 7: セントサイモン
# 8: その他

blood = { "#C4F2F9": 1, "#C6FFAA": 2, "#E0B7FF": 3, "#FFA6E2": 4,  "#FFD28E": 5, "#E8BF9B": 6, "#FFF99": 7, "#DDDDDD": 8 }

def blood_type_collect( storage: Storage ):
    result = {}
    url = "https://race.netkeiba.com/race/bias.html?race_id=" + storage.today_data.race_id
    cookie = lib.netkeiba_login()
    r, _ = lib.request( url, cookie = cookie )
    soup = BeautifulSoup( r.content, "html.parser" )    
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )
            
        if not class_name == None and len( class_name ) == 2 and class_name[0] == "List" and class_name[1] == "HorseList":
            td_tag = tr.findAll( "td" )
            
            try:
                horce_number = td_tag[1].text.replace( " ", "" ).replace( "\n", "" )
                father_style = td_tag[4].get( "style" ).replace( "background:", "" ).replace( ";", "" )
                mother_father_style = td_tag[5].get( "style" ).replace( "background:", "" ).replace( ";", "" )
                result[horce_number] = { "father": blood[father_style], "mother": blood[mother_father_style] }
            except:
                continue

    storage.blood_type_data = result
