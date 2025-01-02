import random

roop_count = 10

def ramdom_odds_rate( horce_id_list ):
    rate_data = {}
    sum_rate = 0

    if len( horce_id_list ) == 0:
        return rate_data

    for horce_id in horce_id_list:
        rate_data[horce_id] = random.uniform( -0.1, 0.1 )
        sum_rate += rate_data[horce_id]

    sum_rate /= len( horce_id_list )
    a = 0
    
    for horce_id in horce_id_list:
        rate_data[horce_id] -= sum_rate

    return rate_data
