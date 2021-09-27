from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_cource_info.pickle" )
dm.dl.file_set( "race_cource_wrap.pickle" )
dm.dl.file_set( "first_pace_analyze_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "first_pace_analyze_data.pickle" )
dm.dl.file_set( "passing_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "corner_horce_body.pickle" )

def main( update = False ):
    result = None
    
    if not update:
        result = dm.pickle_load( "straight_horce_body__learn_data.pickle" )

    if result == None:
        result = {}
    else:
        return result

    result["answer"] = []
    result["teacher"] = []

    race_data = dm.dl.data_get( "race_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    race_cource_wrap = dm.dl.data_get( "race_cource_wrap.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    first_pace_analyze_data = dm.dl.data_get( "first_pace_analyze_data.pickle" )
    passing_data = dm.dl.data_get( "passing_data.pickle" )
    race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )
    corner_horce_body = dm.dl.data_get( "corner_horce_body.pickle" )

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        try:
            current_wrap = race_cource_wrap[race_id]
        except:
            continue

        key_place = str( race_info[race_id]["place"] )
        key_dist = str( race_info[race_id]["dist"] )
        key_kind = str( race_info[race_id]["kind"] )        
        key_baba = str( race_info[race_id]["baba"] )
        
        info_key_dist = key_dist
        
        if race_info[race_id]["out_side"]:
            info_key_dist += "外"
            
        rci_dist = race_cource_info[key_place][key_kind][info_key_dist]["dist"]
        rci_info = race_cource_info[key_place][key_kind][info_key_dist]["info"]
        s = 0
        check = -1
        c = rci_info.count( "c" )

        if 4 < c:
            for i in range( 0, len( rci_info ) ):
                check = rci_info.count( "c", i, len( rci_info ) )

                if check == 4:
                    s = i
                    break
        
        check_s = []
        for i in range( s, len( rci_info ) - 1 ):
            if rci_info[i] == "s":
                check_s.append( i )

        s = 0

        if len( check_s ) == 1:
            s = 2
                
        for kk in race_data[k].keys():
            horce_name = kk.replace( " ", "" )
            current_data, past_data = lib.race_check( horce_data[horce_name],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue
                
            key_horce_num = str( int( cd.horce_number() ) )
            
            for i in range( 0, len( check_s ) ):
                t = int( i * 2 + 1 + ( c % 2 ) + s )
                try:
                    horce_body = corner_horce_body[race_id][str(t)][key_horce_num]
                except:
                    continue

                result["answer"].append( horce_body )
                
        
