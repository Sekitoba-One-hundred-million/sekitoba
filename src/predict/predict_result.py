import SekitobaLibrary as lib
from SekitobaLogger import logger

from config import data_name
from data_create import DataCreate
from predict.train_score import TrainScore
from predict.race_pace_simulation import RacePaceSimulation
from predict.rough_race import RoughRace
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

def log_write( race_id, kind, log_data ):
    log_text = ""

    for horce_id in log_data.keys():
        for score_key in log_data[horce_id].keys():
            log_text += "{} race_id:{} horce_id:{} {}:{}\n".format( kind, race_id, horce_id, score_key, log_data[horce_id][score_key] )

    logger.info( log_text )

def main( data_create: DataCreate ):
    data_create.create()

    if len( data_create.analyze_data ) < 5:
        return None

    race_id = data_create.storage.today_data.race_id
    race_pace_simulation = RacePaceSimulation( data_create.analyze_data ).predict()    

    for horce_id in data_create.analyze_data.keys():
        for key in race_pace_simulation.keys():
            data_create.analyze_data[horce_id]["predict_"+key] = race_pace_simulation[key]

    fp = FirstPassingRank( data_create.analyze_data )
    first_passing_rank = fp.predict()
    log_write( race_id, "first_passing_rank", fp.log_data )
    
    for horce_id in first_passing_rank.keys():
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank] = first_passing_rank[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_index] = first_passing_rank[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_first_passing_rank_stand] = first_passing_rank[horce_id]["stand"]

    lp = LastPassingRank( data_create.analyze_data )
    last_passing_rank = LastPassingRank( data_create.analyze_data ).predict()
    log_write( race_id, "last_passing_rank", lp.log_data )

    for horce_id in last_passing_rank.keys():
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank] = last_passing_rank[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_index] = last_passing_rank[horce_id]["index"]
        data_create.analyze_data[horce_id][data_name.predict_last_passing_rank_stand] = last_passing_rank[horce_id]["stand"]

    up3 = Up3( data_create.analyze_data )
    up3_data = up3.predict()
    log_write( race_id, "up3", up3.log_data )

    for horce_id in up3_data.keys():
        data_create.analyze_data[horce_id][data_name.predict_up3] = up3_data[horce_id]["score"]
        data_create.analyze_data[horce_id][data_name.predict_up3_stand] = up3_data[horce_id]["stand"]

    rs = RankScore( data_create.analyze_data )
    rank_score = rs.predict()
    log_write( race_id, "rank_score", rs.log_data )

    return rank_score
