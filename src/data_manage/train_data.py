class TrainData:
    def __init__( self ):
        self.time = []
        self.wrap = []
        self.load = ""
        self.critic = ""
        self.rank = ""
        self.cource = ""

    def data_check( self ):
        if len( self.time ) == 0:
            return False
        elif len( self.wrap ) == 0:
            return False

        return True
