import math
import torch
import random
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

S = 250

def softmax( data ):
    result = []
    sum_data = 0    

    for i in range( 0, len( data ) ):
        sum_data += math.exp( data[i] )

    for i in range( 0, len( data ) ):
        result.append( math.exp( data[i] ) / sum_data )

    return result

def probability( p_data ):
    number = -1
    count = 0
    r_check = random.random()
    
    for i in range( 0, len( p_data ) ):
        count += p_data[i]
        
        if r_check <= count:
            number = i
            break

    if number == -1:
        number = len( p_data )

    return number

def main( teacher_data, models, rci_info ):
    result = {}
    before_data = [ 0 ]
    predict_check = False
    
    for horce_id in teacher_data["last_straight"].keys():
        corner_count = 0
        straight_count = 0
        
        for i in range( 0, len( rci_info ) - 1 ):
            if rci_info[i] == "s" and rci_info[i+1] == "c":
                t_data = teacher_data["straight"][horce_id][straight_count] + before_data
                predict_horce_body = models["straight"].forward( torch.tensor( np.array( [ t_data ], dtype = np.float32 ) ) ).detach().numpy()
                straight_count += 1
                predict_check = True
            elif rci_info[i] == "c" and rci_info[i+1] == "c":
                t_data = teacher_data["corner"][horce_id][corner_count] + before_data
                predict_horce_body = models["corner"].forward( torch.tensor( np.array( [ t_data ], dtype = np.float32 ) ) ).detach().numpy()
                corner_count += 1
                predict_check = True

            if predict_check:
                horce_body = probability( softmax( predict_horce_body[0] ) ) / 2
                before_data = [ horce_body ]
                predict_check = False
                print( horce_id, before_data )

        t_data = teacher_data["last_straight"][horce_id] + before_data
        predict_diff = models["last_straight"].forward( torch.tensor( np.array( [ t_data ], dtype = np.float32 ) ) ).detach().numpy()
        diff = probability( softmax( predict_diff[0] ) ) / 10
        result[horce_id] = diff

    print( result )
    return result
