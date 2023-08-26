class CurrentHorceData:
    def __init__( self ):
        self.horce_num = None
        self.waku_num = None
        self.age = None
        self.sex = None
        self.burden_weight = None
        self.jockey_id = None
        self.trainer_id = None
        self.odds = None
        self.popular = None
        self.id_weight = None
        self.omega = None

    def before_data_check( self ):
        if self.horce_num == None:
            return False
        elif self.waku_num == None:
            return False
        elif self.age == None:
            return False
        elif self.sex == None:
            return False
        elif self.burden_weight == None:
            return False
        elif self.jockey_id == None:
            return False
        elif self.trainer_id == None:
            return False

        return True

    def just_before_data_check( self ):
        if self.odds == None:
            return False
        elif self.popular == None:
            return False
        elif self.id_weight == None:
            return False

        return True
