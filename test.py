from bs4 import BeautifulSoup
import sekitoba_library as lib
#import sekitoba_data_manage as dm

#from data_manage.storage import Storage
#import data_analyze
#from predict_and_buy import auto_buy
from http_data_collect import base_race_collect

#dm.dl.prod_on()

if __name__ == "__main__":
    #url = "https://race.netkeiba.com/race/shutuba.html?race_id=202204020410"
    #url = "https://db.netkeiba.com/jockey/result/01184"
    #r, _ = lib.request( url )
    #soup = BeautifulSoup( r.content, "html.parser" )
    #print( http_data_collect.jockey_data_collect.jockey_year_rank( url ) )
    #stock_data: dict[ str, Storage ] = dm.pickle_load( "stock_data.pickle", prod = True )
    #data_analyze.main( stock_data )
    #for k in stock_data.keys():
    #    print( k )
    #    users_data = data_analyze.users_data.UsersData( stock_data[k] )
    #    for horce_id in stock_data[k].horce_id_list:
    #        users_data.race_interval( horce_id )
    #    break
    #auto_buy.one_buy( [ { "horce_num": 3, "money": 2 }, { "horce_num": 6, "money": 1 } ] )
    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202201020201"
    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202201020201"
    r, _ = lib.request( base_url )
    soup = BeautifulSoup( r.content, "html.parser" )
