from core import db
class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username  = db.Column(db.String(120), unique=True)
        phone_num = db.Column(db.String(120), unique=True)
        password  = db.Column(db.String(120))
        likes     = db.Column(db.String(1200) )
        dislikes   = db.Column(db.String(1200))
        exiting   = db.Column(db.String)
        avator    = db.Column(db.String(1200))
        age       = db.Column(db.Integer)
        sex       = db.Column(db.String)
        willlike  =  db.Column(db.String)
        def __init__(self, username, password, exiting,age,sex,likes="",dislikes="",willlike=""):
           self.username = username
           self.password = password
           self.exiting = exiting
           self.age     = int(age)
           self.sex     = sex
           self.likes    = ""
           self.dislikes = ""
           self.avator  = "shit"
        def __repr__(self):
            return "<ACCOUNT NAME IS %r>" % self.username
        def is_authenticated(self):
            return True

        def is_active(self):
              return True

        def is_anonymous(self):
              return False

        def get_id(self):
              return unicode(self.id)
