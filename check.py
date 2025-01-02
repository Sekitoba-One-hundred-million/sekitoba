import SekitobaLibrary as lib
import SekitobaDataManage as dm

def main():
    race_id = "202406040602"
    horce_id = "2022104722"
    
    #f = open( "/Volumes/Gilgamesh/sekitoba-prod/rank_score_data.txt" )
    f = open( "/Volumes/Gilgamesh/sekitoba-prod/first_passing_rank_score_data.txt" )
    key_list = []
    all_data = f.readlines()

    for str_data in all_data:
        str_data = str_data.replace( "\n", "" )
        key_list.append( str_data )
    
    #simu_data = dm.local_pickle_load("rank_simu_data.pickle")
    #simu_old_data = dm.local_pickle_load("rank_simu_data.pickle.old")
    simu_data = dm.local_pickle_load("first_passing_rank_simu_data.pickle")
    simu_old_data = dm.local_pickle_load("first_passing_rank_simu_data.pickle.backup-1727804550")

    for i in range( 0, len( key_list ) ):
        key = key_list[i]
        data = simu_data[race_id][horce_id]["data"][i]
        old_data = simu_old_data[race_id][horce_id]["data"][i]

        if not data == old_data:
            print( "{} data:{} old_data:{}".format( key, data, old_data ) )

def pace_main():
    race_id = "202406040602"

    f = open( "/Volumes/Gilgamesh/sekitoba-prod/rough_race_score_data.txt" )
    key_list = []
    all_data = f.readlines()

    for str_data in all_data:
        str_data = str_data.replace( "\n", "" )
        key_list.append( str_data )

    simu_data = dm.pickle_load("pace_learn_data.pickle")
    simu_old_data = dm.pickle_load("pace_learn_data.pickle.backup-1727800765")
    data = {}
    old_data = {}

    for i in range( 0, len( simu_data["race_id"] ) ):
        race_id = simu_data["race_id"][i]
        data[race_id] = {}
        
        for r in range( 0, len( key_list ) ):
            key = key_list[r]
            data[race_id][key] = simu_data["teacher"][i][r]

    for i in range( 0, len( simu_old_data["race_id"] ) ):
        race_id = simu_old_data["race_id"][i]
        old_data[race_id] = {}
        
        for r in range( 0, len( key_list ) ):
            key = key_list[r]
            old_data[race_id][key] = simu_old_data["teacher"][i][r]

    for race_id in old_data.keys():
        for key in old_data[race_id].keys():
            if not data[race_id][key] == old_data[race_id][key]:
                print( race_id, key, data[race_id][key], old_data[race_id][key] )

if __name__ == "__main__":
    pace_main()
