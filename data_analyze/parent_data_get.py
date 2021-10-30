import sekitoba_data_manage as dm
import sekitoba_library as lib

def main( horce_data, passing_data, parent_id ):
    result = {}
    result["rank"] = 0
    result["two_rate"] = 0
    result["three_rate"] = 0
    result["average_speed"] = 0
    result["limb"] = 0

    try:
        parent_data = horce_data[parent_id]
    except:
        return result

    parent_pd = lib.past_data( parent_data, [] )
    result["rank"] = parent_pd.rank()
    result["two_rate"] = parent_pd.two_rate()
    result["three_rate"] = parent_pd.three_rate()
    result["average_speed"] = parent_pd.average_speed()

    try:
        result["limb"] = lib.limb_search( passing_data[parent_id], parent_pd )
    except:
        return result

    return result

        
