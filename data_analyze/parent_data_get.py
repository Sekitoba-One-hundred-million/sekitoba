import sekitoba_data_manage as dm
import sekitoba_library as lib

dm.dl.file_set( "parent_data.pickle" )

class parent_data_get:
    def __init__( self ):
        self.parent_data = dm.dl.data_get( "parent_data.pickle" )

    def main( self, horce_name, cd ):  
        result = {}
        result["father"] = {}
        result["father"]["dist"] = 0
        result["father"]["race_kind"] = 0
        result["father"]["rank"] = 0
        result["father"]["diff"] = 0
        result["father"]["up_time"] = 0
    
        result["mother"] = {}
        result["mother"]["dist"] = 0
        result["mother"]["race_kind"] = 0
        result["mother"]["rank"] = 0
        result["mother"]["diff"] = 0
        result["mother"]["up_time"] = 0

        try:
            data = self.parent_data[horce_name]
        except:
            return result

        result["father"]["dist"] = abs( data["father"]["dist"] - cd.dist() )
        result["father"]["race_kind"] = abs( data["father"]["race_kind"] - cd.race_kind() )
        result["father"]["rank"] = data["father"]["rank"]
        result["father"]["diff"] = data["father"]["diff"]
        result["father"]["up_time"] = data["father"]["up_time"]
        
        result["mother"]["dist"] = abs( data["mother"]["dist"] - cd.dist() )
        result["mother"]["race_kind"] = abs( data["mother"]["race_kind"] - cd.race_kind() )
        result["mother"]["rank"] = data["mother"]["rank"]
        result["mother"]["diff"] = data["mother"]["diff"]
        result["mother"]["up_time"] = data["mother"]["up_time"]

        return result

        
