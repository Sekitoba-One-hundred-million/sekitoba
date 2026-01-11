class ImportantData:
    def __init__( self ):
        self.id = ""
        self.member = ""
        self.password = ""
        self.pars = ""
        self.password_read()

    def password_read( self ):
        f = open( "/Volumes/Gilgamesh/.import/jra_pass.txt", "r" )
        str_data_list = f.readlines()

        for str_data in str_data_list:
            str_data = str_data.replace( "\n", "" )
            split_data = str_data.split( ":" )

            if split_data[0] == "id":
                self.id = split_data[1]
            elif split_data[0] == "member":
                self.member = split_data[1]
            elif split_data[0] == "password":
                self.password = split_data[1]
            elif split_data[0] == "pars":
                self.pars = split_data[1]
