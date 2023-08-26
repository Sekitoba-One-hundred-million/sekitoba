import sekitoba_library as lib
from bs4 import BeautifulSoup

class TodayData:
    def __init__( self, race_id, race_date ):
        self.race_id = race_id
        self.url = "https://race.netkeiba.com/race/shutuba.html?race_id={}".format( self.race_id )
        self.year = int( race_id[0:4] )
        self.place_num = int( race_id[4:6] )
        self.place = lib.place_check( self.place_num )
        self.day = int( race_id[9] )
        self.num = int( race_id[7] )
        self.race_num = int( race_id[10:12] )
        self.race_date: datetime.datetime = race_date
        self.race_timestamp = -1
        self.bet_race = False

    def race_time_get( self ):
        time_data = ""
        r, _ = lib.request( self.url )
        soup = BeautifulSoup( r.content, "html.parser" )
        div_tag = soup.findAll( "div" )

        for div in div_tag:
            class_name = div.get( "class" )

            if not class_name == None \
              and class_name[0] == "RaceName":
                race_name = lib.text_replace( div.text )

                if "障害" in race_name:
                    self.race_timestamp = 0
                    self.bet_race = False
                    break

            if not class_name == None \
              and class_name[0] == "RaceData01":
                text_data = div.text.replace( "\n", "" )
                text_data = text_data.replace( " ", "" )
                split_text = text_data.split( "/" )
                time_data = lib.text_replace( split_text[0].replace( "発走", "" ) )

                if split_text[1][0] == "芝" \
                  or split_text[1][0] == "ダ":
                   self.bet_race  = True

                self.race_timestamp = self.time_change( time_data )
                break

    def time_change( self, str_time ):
        split_time = str_time.split( ":" )

        if not len( split_time ) == 2:
            return -1

        hour = 0
        minute = 0
        
        try:
            hour = int( split_time[0] )
            minute = int( split_time[1] )
        except:
            return -1

        return int( hour * 60 + minute )
