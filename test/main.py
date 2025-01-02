import SekitobaDataManage as dm
import SekitobaLibrary as lib

#lib.proxyUse = False
dm.dl.prod_on()

import os
import sys

sys.path.append( "{}/src".format( os.getcwd() ) )

import test_today_data_get
import test_predict

if __name__ == "__main__":
    #test_today_data_get.predict_race_idGet_test()
    #test_today_data_get.today_data_test()
    test_predict.data_check()
    print( "test success!!" )
