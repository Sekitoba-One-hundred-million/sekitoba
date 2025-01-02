import json
import requests
import datetime

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

dm.dl.prod_on()

def main():
    race_data = ps.RaceData()
    key = "rank"
    colume = { "rank": [ "rank_score", "rank_simu_data.pickle" ] }
    race_id = "202406040904"
    horce_id = "2020101258"

    f = open( "/Volumes/Gilgamesh/sekitoba-log/2024-09-29" )
    log_all_data = f.readlines()
    log_dict_data = {}

    for str_data in log_all_data:
        str_data = str_data.replace( "\n", "" )
        split_data = str_data.split( " " )

        if split_data[3] == colume[key][0]:
            str_race_id = split_data[4].split( ":" )[1]

            if str_race_id == race_id:
                str_horce_id = split_data[5].split( ":" )[1]
                lib.dicAppend( log_dict_data, str_horce_id, {} )
                score_key = split_data[6].split( ":" )[0]
                score = float( split_data[6].split( ":" )[1] )
                log_dict_data[str_horce_id][score_key] = score

    f = open( "/Volumes/Gilgamesh/sekitoba-prod/{}_data.txt".format( colume[key][0] ) )
    key_list = []
    all_data = f.readlines()

    for str_data in all_data:
        str_data = str_data.replace( "\n", "" )
        key_list.append( str_data )
        
    simu_data = dm.pickle_load( colume[key][1] )

    for horce_id in simu_data[race_id].keys():
        print( horce_id )
        
        for i in range( 0, len( simu_data[race_id][horce_id]["data"] ) ):
            if "predict" in key_list[i] or "devi" in key_list[i] or "stand" in key_list[i]:
                continue
            
            simu_score = simu_data[race_id][horce_id]["data"][i]
            log_score = log_dict_data[horce_id][key_list[i]]

            if not round( simu_score, 4 ) == round( log_score, 4 ):
                print( key_list[i], horce_id, simu_score, log_score )

        print( "" )

def test():
    checkData = {}
    pace_learn_data = dm.pickle_load( "pace_learn_data.pickle" )
    first_passing_rank_learn_data = dm.pickle_load( "first_passing_rank_learn_data.pickle" )
    last_passing_rank_learn_data = dm.pickle_load( "last_passing_rank_learn_data.pickle" )
    up3_learn_data = dm.pickle_load( "up3_learn_data.pickle" )
    rank_learn_data = dm.pickle_load( "rank_learn_data.pickle" )

    url = "http://100.102.168.34:2244"
    checkData["pace"] = json.dumps( pace_learn_data["teacher"][0] )
    checkData["first-passing"] = json.dumps( first_passing_rank_learn_data["teacher"][0] )
    checkData["last-passing"] = json.dumps( last_passing_rank_learn_data["teacher"][0] )
    checkData["up3"] = json.dumps( up3_learn_data["teacher"][0] )
    checkData["rank"] = json.dumps( rank_learn_data["teacher"][0] )

    for k in checkData.keys():
        r = requests.post( url + k,
                        data = checkData[k],
                        headers={"Content-Type": "application/json"} )
        print( k, r.status_code )
        print( json.loads( r.text ) )
        print( "" )

if __name__ == "__main__":
    test()
