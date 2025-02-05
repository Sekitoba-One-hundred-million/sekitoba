import sys

import SekitobaLibrary as lib
import SekitobaDataManage as dm

SCORE_NAME = "first_passing_rank"

def get_teacher_data( race_id ):
    score_data = {}
    #train_data = dm.pickle_load( "train_learn_data.pickle" )
    teacher_data = dm.pickle_load( SCORE_NAME + "_simu_data.pickle" )
    #up3_data = dm.pickle_load( "up3_learn_data.pickle" )
    score_name_list = []
    #teacher_data = dm.pickle_load( "rank_simu_data.pickle" )
    #f = open( "/Volumes/Gilgamesh/sekitoba-prod/rank_score_data.txt" )
    f = open( "/Volumes/Gilgamesh/sekitoba-prod/" + SCORE_NAME + "_score_data.txt" )
    all_data = f.readlines()

    for str_data in all_data:
        score_name_list.append( str_data.replace( "\n", "" ) )

    if not race_id in teacher_data:
        print( "not found teacher_data {}".format( race_id ) )
        sys.exit( 1 )
        return None

    for horce_id in teacher_data[race_id].keys():
        score_data[horce_id] = {}
        
        for i in range( 0, len( score_name_list ) ):
            score_data[horce_id][score_name_list[i]] = teacher_data[race_id][horce_id]["data"][i]

    return score_data

def get_log_data( log_name, check_race_id ):
    log_path = "/Volumes/Gilgamesh/sekitoba-log/" + log_name

    log_predict_data = {}
    f = open( log_path, "r" )
    log_all_data = f.readlines()
    f.close()

    for str_data in log_all_data:
        str_data = str_data.replace( "\n", "" )
        split_data = str_data.split( " " )

        if split_data[3] == SCORE_NAME:
            log_race_id = split_data[4].split( ":" )[1]

            if not log_race_id == check_race_id:
                continue

            log_horce_id = split_data[5].split( ":" )[1]
            score_name = split_data[6].split( ":" )[0]
            score = float( split_data[6].split( ":" )[1] )
            lib.dic_append( log_predict_data, log_horce_id, {} )
            log_predict_data[log_horce_id][score_name] = score

    return log_predict_data

def main():
    log_name = "2024-01-28"
    check_race_id = "202408020201"
    check_horce_id = "2021107078"
    
    log_data = get_log_data( log_name, check_race_id )
    teacher_data = get_teacher_data( check_race_id )
    
    for horce_id in log_data.keys():
        #if not horce_id == check_horce_id:
        #    continue
        
        for score_name in log_data[horce_id].keys():
            if "true_skill" in score_name or \
              "judgment" in score_name or \
              "power" in score_name:
                continue

            #if not "speed_index" == score_name:
            #    continue
            
            if not log_data[horce_id][score_name] == teacher_data[horce_id][score_name]:
                print( check_race_id, horce_id, score_name, log_data[horce_id][score_name], teacher_data[horce_id][score_name] )

if __name__ == "__main__":
    main()
