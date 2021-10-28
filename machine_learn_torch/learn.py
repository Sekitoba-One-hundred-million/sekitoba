import random

import sekitoba_library as lib
import sekitoba_data_manage as dm
from machine_learn_torch import nn

def data_check( data ):
    result = {}
    result["teacher"] = []
    result["test_teacher"] = []
    result["answer"] = []
    result["test_answer"] = []
    ma = -1
    mi = 100
    
    for i in range( 0, len( data["answer"] ) ):
        r = random.random()
        ma = max( data["answer"][i], ma )
        mi = min( data["answer"][i], mi )
        
        if r < 0.1:
            result["test_teacher"].append( data["teacher"][i] )
            result["test_answer"].append( data["answer"][i] )
        else:
            result["teacher"].append( data["teacher"][i] )
            result["answer"].append( data["answer"][i] )

    return result, ma


def main( data, GPU = False ):
    learn_data, a_units = data_check( data )
    n_units = len( data["teacher"][0] )
    print( n_units, a_units )
    
    model = nn.StrightNN( n_units, a_units + 1 )
    model = nn.main( learn_data, model, GPU )
    dm.model_upload( "stright_horce_model.pickle", model )
    return model
