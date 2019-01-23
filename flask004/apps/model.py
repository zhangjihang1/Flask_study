class User:
    def __init__(self, name=None, psw=None, email=None,
                 age=None, birthday=None, face=None):
        self.name = name
        self.psw = psw
        self.email = email
        self.age = age
        self.birthday = birthday
        self.face = face

    def toList(self):
        return [self.name, self.psw, self.email, self.age, self.birthday, self.face]

    def fromList(self, user_info):
        self.name = user_info[0]
        self.psw = user_info[1]
        self.email = user_info[2]
        self.age = user_info[3]
        self.birthday = user_info[4]
        self.face = user_info[5]

    def getAttrs(self):
        return ('name', 'psw', 'email', 'age', 'birthday', 'face')
