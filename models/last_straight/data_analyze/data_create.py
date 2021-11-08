from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from data_analyze.train_index_get import train_index_get
from data_analyze import parent_data_get

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
dm.dl.file_set( "parent_id_data.pickle" )

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
        result = dm.pickle_load( "last_straight_learn_data.pickle" )

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
    parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
    
    train_index = train_index_get()

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
        popular_limb = -1
        train_index_list = train_index.main( race_data[k], horce_data, race_id )
        count = -1

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )
            
            if not cd.race_check():
                continue
            
            try:
                limb_math = lib.limb_search( passing_data[horce_id], pd )
            except:
                limb_math = 0

            if cd.popular() == 1:
                popular_limb = limb_math
                
            race_limb[limb_math] += 1

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            #pad = parent_data.main( horce_name, cd )
            key_horce_num = str( int( cd.horce_number() ) )
            before_horce_body = 0
            count += 1
            
            t_instance = []
            change_data = []

            try:
                before_horce_body = corner_horce_body[race_id]["4"][key_horce_num]
            except:
                before_horce_body = 0

            father_id = parent_id_data[horce_id]["father"]
            mother_id = parent_id_data[horce_id]["mother"]
            speed, up_speed, pace_speed = pd.speed_index( baba_index_data[horce_id] )
            father_data = parent_data_get.main( horce_data, passing_data, father_id )
            mother_data = parent_data_get.main( horce_data, passing_data, mother_id )
                
            dm.dn.append( t_instance, race_limb[0], "その他の馬の数" )
            dm.dn.append( t_instance, race_limb[1], "逃げaの馬の数" )
            dm.dn.append( t_instance, race_limb[2], "逃げbの馬の数" )
            dm.dn.append( t_instance, race_limb[3], "先行aの馬の数" )
            dm.dn.append( t_instance, race_limb[4], "先行bの馬の数" )
            dm.dn.append( t_instance, race_limb[5], "差しaの馬の数" )
            dm.dn.append( t_instance, race_limb[6], "差しbの馬の数" )
            dm.dn.append( t_instance, race_limb[7], "追いの馬の数" )
            dm.dn.append( t_instance, race_limb[8], "後方の馬の数" )
            dm.dn.append( t_instance, popular_limb, "一番人気の馬の脚質" )
            dm.dn.append( t_instance, float( key_place ), "場所" )
            dm.dn.append( t_instance, float( key_dist ), "距離" )
            dm.dn.append( t_instance, float( key_kind ), "芝かダート" )
            dm.dn.append( t_instance, float( key_baba ), "馬場" )
            dm.dn.append( t_instance, cd.popular(), "人気" )
            dm.dn.append( t_instance, cd.id_weight(), "馬体重の増減" )
            dm.dn.append( t_instance, cd.burden_weight(), "斤量" )
            dm.dn.append( t_instance, cd.horce_number(), "馬番" )
            dm.dn.append( t_instance, cd.flame_number(), "枠番" )
            dm.dn.append( t_instance, cd.all_horce_num(), "馬の頭数" )
            dm.dn.append( t_instance, float( key_dist ) - rci_dist[-1], "今まで走った距離" )
            dm.dn.append( t_instance, rci_dist[-1], "直線の距離" )
            dm.dn.append( t_instance, lib.limb_search( passing_data[horce_id], pd ), "過去データからの予想脚質" )
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
            dm.dn.append( t_instance, father_data["rank"], "父親の平均順位" )
            dm.dn.append( t_instance, father_data["two_rate"], "父親の連対率" )
            dm.dn.append( t_instance, father_data["three_rate"], "父親の副賞率" )
            dm.dn.append( t_instance, father_data["average_speed"], "父親の平均速度" )
            dm.dn.append( t_instance, father_data["limb"], "父親の脚質" )
            dm.dn.append( t_instance, mother_data["rank"], "母親の平均順位" )
            dm.dn.append( t_instance, mother_data["two_rate"], "母親の連対率" )
            dm.dn.append( t_instance, mother_data["three_rate"], "母親の副賞率" )
            dm.dn.append( t_instance, mother_data["average_speed"], "母親の平均速度" )
            dm.dn.append( t_instance, mother_data["limb"], "母親の脚質" )                
            dm.dn.append( change_data, before_horce_body, "前の馬身(startは0))" )

            if year == "2020":
                lib.dic_append( simu_data, race_id, {} )
                simu_data[race_id][key_horce_num] = {}
                simu_data[race_id][key_horce_num]["answer"] = { "rank": cd.rank(), "odds": cd.odds() }
                simu_data[race_id][key_horce_num]["data"] = t_instance
                simu_data[race_id][key_horce_num]["change"] = change_data

            result["answer"].append( cd.diff() )
            result["teacher"].append( t_instance + change_data )
                
                    
    for i in range( 0, len( result["answer"] ) ):
        result["answer"][i] = min( max( int( result["answer"][i] * 10 + 10 ), 0 ), 50 )

    print( len( result["answer"] ) , len( result["teacher"] ) )
    dm.pickle_upload( "last_straight_learn_data.pickle", result )
    #dm.pickle_upload( "straight_horce_body_minmax.pickle", hm )
    dm.pickle_upload( "last_straight_simu_data.pickle", simu_data )
    dm.dl.data_clear()
    return result
