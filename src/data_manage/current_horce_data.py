import SekitobaLibrary as lib

class CurrentHorceData:
    def __init__( self ):
        self.horce_num = lib.escapeValue
        self.waku_num = lib.escapeValue
        self.age = lib.escapeValue
        self.sex = lib.escapeValue
        self.burden_weight = lib.escapeValue
        self.jockey_id = lib.escapeValue
        self.trainer_id = lib.escapeValue
        self.odds = lib.escapeValue
        self.popular = lib.escapeValue
        self.weight = lib.escapeValue
        self.father_id = ""
        self.mother_id = ""

    def before_data_check( self ):
        if self.horce_num == lib.escapeValue:
            return False
        elif self.waku_num == lib.escapeValue:
            return False
        elif self.age == lib.escapeValue:
            return False
        elif self.sex == lib.escapeValue:
            return False
        elif self.burden_weight == lib.escapeValue:
            return False
        elif self.jockey_id == "":
            return False
        elif self.trainer_id == "":
            return False

        return True

    def just_before_data_check( self ):
        if self.odds == lib.escapeValue:
            return False
        elif self.popular == lib.escapeValue:
            return False
        elif self.weight == lib.escapeValue:
            return False

        return True
