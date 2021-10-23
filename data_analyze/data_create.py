from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from data_analyze.train_index_get import train_index_get
from data_analyze.parent_data_get import parent_data_get

dm.dl.file_set( "race_cource_info.pickle" )
dm.dl.file_set( "race_cource_wrap.pickle" )
dm.dl.file_set( "first_pace_analyze_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "first_pace_analyze_data.pickle" )
dm.dl.file_set( "passing_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "corner_horce_body.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )

def use_corner_check( s ):
    if s == 4:
        return [ "1", "3" ]
    elif s == 3:
        return [ "2", "3" ]
    
    return [ "3" ]

def max_check( s ):
    try:
        return max( s )
    except:
        return -100
    
def learn_corner_check( rci_info ):
    result = []
    c = 0
    use_corner = use_corner_check( min( rci_info.count( "c" ), 4 ) )
    
    for i in range( 0, len( rci_info ) - 1 ):   
        check = rci_info.count( "c", i, len( rci_info ) )

        if rci_info[i] == "s" and rci_info[i+1] == "c":
            instance = {}
            instance["count"] = i
            instance["corner"] = None

            if check <= 4:
                instance["corner"] = use_corner[c]
                c += 1
            
            result.append( instance )

    return result

def main( update = False ):
    result = None
    
    if not update:
        result = dm.pickle_load( "straight_horce_body_learn_data.pickle" )

    if result == None:
        result = {}
    else:
        return result

    result["answer"] = []
    result["teacher"] = []
    simu_data = {}
    min_horce_body = 10000
    max_horce_body = -1

    race_data = dm.dl.data_get( "race_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    race_cource_wrap = dm.dl.data_get( "race_cource_wrap.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    first_pace_analyze_data = dm.dl.data_get( "first_pace_analyze_data.pickle" )
    passing_data = dm.dl.data_get( "passing_data.pickle" )
    race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )
    corner_horce_body = dm.dl.data_get( "corner_horce_body.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    train_index = train_index_get()
    parent_data = parent_data_get()

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
        use_learn_corner = learn_corner_check( rci_info )
        race_limb = [0] * 9
        train_index_list = train_index.main( race_data[k], horce_data, race_id )
        count = -1

        for kk in race_data[k].keys():
            horce_name = kk.replace( " ", "" )
            current_data, past_data = lib.race_check( horce_data[horce_name],
                                                          year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
            
            if not cd.race_check():
                continue
            
            try:
                limb_math = lib.limb_search( passing_data[horce_name], pd )
            except:
                limb_math = 0

            race_limb[limb_math] += 1

        for kk in race_data[k].keys():
            horce_name = kk.replace( " ", "" )
            current_data, past_data = lib.race_check( horce_data[horce_name],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            pad = parent_data.main( horce_name, cd )
            key_horce_num = str( int( cd.horce_number() ) )
            before_horce_body = 0
            count += 1
            
            for i in range( 0, len( use_learn_corner ) ):
                if not i == 0:
                    continue
                    
                t_instance = []
                change_data = []
                u = use_learn_corner[i]["count"]
                c = use_learn_corner[i]["corner"]
                try:
                    horce_body = corner_horce_body[race_id][c][key_horce_num]
                except:
                    horce_body = 0

                try:
                    before_horce_body = corner_horce_body[race_id][str(int(c)-1)][key_horce_num]
                except:
                    before_horce_body = 0

                speed, up_speed, pace_speed = pd.speed_index( baba_index_data[horce_name] )
                
                dm.dn.append( t_instance, race_limb[0], "その他の馬の数" )
                dm.dn.append( t_instance, race_limb[1], "逃げaの馬の数" )
                dm.dn.append( t_instance, race_limb[2], "逃げbの馬の数" )
                dm.dn.append( t_instance, race_limb[3], "先行aの馬の数" )
                dm.dn.append( t_instance, race_limb[4], "先行bの馬の数" )
                dm.dn.append( t_instance, race_limb[5], "差しaの馬の数" )
                dm.dn.append( t_instance, race_limb[6], "差しbの馬の数" )
                dm.dn.append( t_instance, race_limb[7], "追いの馬の数" )
                dm.dn.append( t_instance, race_limb[8], "後方の馬の数" )
                dm.dn.append( t_instance, float( key_place ), "場所" )
                dm.dn.append( t_instance, float( key_dist ), "距離" )
                dm.dn.append( t_instance, float( key_kind ), "芝かダート" )
                dm.dn.append( t_instance, float( key_baba ), "馬場" )
                dm.dn.append( t_instance, cd.id_weight(), "馬体重の増減" )
                dm.dn.append( t_instance, cd.burden_weight(), "斤量" )
                dm.dn.append( t_instance, cd.horce_number(), "馬番" )
                dm.dn.append( t_instance, cd.flame_number(), "枠番" )
                dm.dn.append( t_instance, cd.all_horce_num(), "馬の頭数" )
                dm.dn.append( t_instance, sum( rci_dist[0:u] ), "今まで走った距離" )
                dm.dn.append( t_instance, float( key_dist ) - sum( rci_dist[0:u] ), "残りの距離" )
                dm.dn.append( t_instance, rci_dist[u], "直線の距離" )
                dm.dn.append( t_instance, lib.limb_search( passing_data[horce_name], pd ), "過去データからの予想脚質" )
                dm.dn.append( t_instance, max_check( speed ), "最大のスピード指数" )
                dm.dn.append( t_instance, max_check( up_speed ), "最大の上り3Fのスピード指数" )
                dm.dn.append( t_instance, max_check( pace_speed ), "最大のペース指数" )
                dm.dn.append( t_instance, pd.three_average(), "過去3レースの平均順位" )
                dm.dn.append( t_instance, pd.dist_rank_average(), "過去同じ距離の種類での平均順位" )
                dm.dn.append( t_instance, pd.racekind_rank_average(), "過去同じレース状況での平均順位" )
                dm.dn.append( t_instance, pd.baba_rank_average(), "過去同じ馬場状態での平均順位" )
                dm.dn.append( t_instance, pd.jockey_rank_average(), "過去同じ騎手での平均順位" )
                dm.dn.append( t_instance, pd.three_average(), "複勝率" )
                dm.dn.append( t_instance, pd.two_rate(), "連対率" )
                dm.dn.append( t_instance, pd.get_money(), "獲得賞金" )
                dm.dn.append( t_instance, pd.best_weight(), "ベスト体重と現在の体重の差" )
                dm.dn.append( t_instance, pd.race_interval(), "中週" )
                dm.dn.append( t_instance, pd.average_speed(), "平均速度" )
                dm.dn.append( t_instance, pd.pace_up_check(), "ペースと上りの関係" )
                dm.dn.append( t_instance, train_index_list[count]["a"], "調教ペースの傾き" )
                dm.dn.append( t_instance, train_index_list[count]["b"], "調教ペースの切片" )
                dm.dn.append( t_instance, train_index_list[count]["time"], "調教ペースの指数タイム" )
                dm.dn.append( t_instance, pad["father"]["dist"] , "父親の適正距離との差" )
                dm.dn.append( t_instance, pad["father"]["race_kind"] , "父親の適正のレースの種類との差" )
                dm.dn.append( t_instance, pad["father"]["rank"] , "父親の平均順位" )
                dm.dn.append( t_instance, pad["father"]["diff"] , "父親の平均着差" )
                dm.dn.append( t_instance, pad["father"]["up_time"] , "父親の平均上り3Fのタイム" )                
                dm.dn.append( t_instance, pad["mother"]["dist"] , "母親の適正距離との差" )
                dm.dn.append( t_instance, pad["mother"]["race_kind"] , "母親の適正のレースの種類との差" )
                dm.dn.append( t_instance, pad["mother"]["rank"] , "母親の平均順位" )
                dm.dn.append( t_instance, pad["mother"]["diff"] , "母親の平均着差" )
                dm.dn.append( t_instance, pad["mother"]["up_time"] , "母親の平均上り3Fのタイム" )

                dm.dn.append( change_data, before_horce_body, "前の馬身(startは0))" )

                if year == "2020":
                    lib.dic_append( simu_data, race_id, {} )
                    lib.dic_append( simu_data[race_id], key_horce_num, { "data": [], "change": [] } )
                    simu_data[race_id][key_horce_num]["data"].append( t_instance )
                    simu_data[race_id][key_horce_num]["change"].append( change_data )

                if not c == None:
                    t_instance.extend( change_data )
                    min_horce_body = min( min_horce_body, horce_body )
                    max_horce_body = max( max_horce_body, horce_body )
                    result["answer"].append( horce_body )
                    result["teacher"].append( t_instance )
                
                    
    for i in range( 0, len( result["answer"] ) ):
        result["answer"][i] = min( int( result["answer"][i] * 2 ), 30 )

    hm = { "min": min_horce_body, "max": max_horce_body }

    print( len( result["answer"] ) , len( result["teacher"] ) )
    dm.pickle_upload( "straight_horce_body_learn_data.pickle", result )
    #dm.pickle_upload( "straight_horce_body_minmax.pickle", hm )
    #dm.pickle_upload( "straight_horce_body_simu_data.pickle", simu_data )
    dm.dl.data_clear()
    return result
