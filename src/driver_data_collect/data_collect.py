import sekitoba_library as lib
from data_manage import Storage
from driver_data_collect import race_data_get
from driver_data_collect import omega_get

def main( storage: Storage ):
    driver = lib.driver_start()
    race_data_get.main( storage, driver )
    omega_get.main( storage, driver )
    driver.close()
