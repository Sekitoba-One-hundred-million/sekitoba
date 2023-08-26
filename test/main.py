import os
import sys

sys.path.append( "{}/src".format( os.getcwd() ) )

import test_today_data_get

if __name__ == "__main__":
    #test_today_data_get.predict_race_id_get_test()
    test_today_data_get.today_data_test()
    print( "test success!!" )
