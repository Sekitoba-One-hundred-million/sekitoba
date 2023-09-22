import sekitoba_library as lib

from config import data_name
from data_create import DataCreate
from predict.train_score import TrainScore
from predict.race_pace_simulation import RacePaceSimulation
from predict.first_passing_rank import FirstPassingRank
from predict.last_passing_rank import LastPassingRank
from predict.up3 import Up3
from predict.rank_score import RankScore
from predict.recovery_score import RecoveryScore

def passing_rank_analyze( passing_data ):
    result = {}
    check_data = []
    stand_score_list = []
    
    for horce_id in passing_data.keys():
        check_data.append( { "horce_id": horce_id, "score": passing_data[horce_id] } )
        stand_score_list.append( passing_data[horce_id] )

    next_rank = 1
    continue_count = 1
    before_score = 1
    check_data = sorted( check_data, key = lambda x: x["score"] )
    stand_score_list = lib.standardization( stand_score_list )

    for i in range( 0, len( check_data ) ):
        predict_score = -1
        current_score = int( check_data[i]["score"] + 0.5 )

        if continue_count >= 2:
            next_rank += continue_count
            continue_count = 0
            
        if i == 0:
            predict_score = 1
        elif before_score == current_score:
            continue_count += 1
            predict_score = next_rank
        else:
            next_rank += continue_count
            continue_count = 1
            predict_score = next_rank

        horce_id = check_data[i]["horce_id"]
        result[horce_id] = {}
        result[horce_id]["score"] = check_data[i]["score"]
        result[horce_id]["index"] = predict_score
        result[horce_id]["stand"] = stand_score_list[i]

    return result        

def main( data_create: DataCreate ):
    data_create.create()
    print( "start" )
    race_pace_simulation = RacePaceSimulation( data_create.analyze_data ).predict()

    for horce_id in data_create.analyze_data.keys():
        data_create.analyze_data[horce_id][data_name.predict_pace] = race_pace_simulation

    train_score = TrainScore( data_create.analyze_data ).predict()

    for horce_id in train_score.keys():
        data_create.analyze_data[horce_id][data_name.predict_train_score] = train_score[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_train_score_index] = train_score[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_train_score_stand] = train_score[horce_id]["stand"]

    first_passing_rank = FirstPassingRank( data_create.analyze_data ).predict()
    first_passing_rank = passing_rank_analyze( first_passing_rank )
    
    for horce_id in first_passing_rank.keys():
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank] = first_passing_rank[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_index] = first_passing_rank[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_stand] = first_passing_rank[horce_id]["stand"]

    last_passing_rank = LastPassingRank( data_create.analyze_data ).predict()

    for horce_id in last_passing_rank.keys():
        last_passing_rank[horce_id] += data_create.analyze_data[horce_id][data_name.predict_first_passing_rank]

    last_passing_rank = passing_rank_analyze( last_passing_rank )
    
    for horce_id in last_passing_rank.keys():
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank] = last_passing_rank[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_index] = last_passing_rank[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_stand] = last_passing_rank[horce_id]["stand"]

    up3 = Up3( data_create.analyze_data ).predict()

    for horce_id in up3.keys():
        data_create.analyze_data[horce_id][data_name.predict_up3] = up3[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_up3_index] = up3[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_up3_stand] = up3[horce_id]["stand"]

    rank_score = RankScore( data_create.analyze_data ).predict()
    recovery_score = RecoveryScore( data_create.analyze_data ).predict()
