import sys
sys.path.append( "/Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/sekitoba/" )
sys.path.append( "/Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/sekitoba/storage" )

from data_manage.storage import Storage
import SekitobaDataManage as dm

stock_data = dm.pickle_load( "stock_data.pickle", prod = True )
args = sys.argv

if len( args ) == 1:
    print( "not set race_id" )
    sys.exit( 0 )

race_id = args[1]
key = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id

if not key in stock_data.keys():
    print( "not found race_id:{}".format( race_id ) )
    sys.exit( 0 )

stock_data.pop( key )
dm.pickle_upload( "stock_data.pickle", stock_data, prod = True )
print( "delete data race_id:{}".format( race_id ) )
