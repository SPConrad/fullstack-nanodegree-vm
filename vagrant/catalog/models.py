import random, string, datetime
from sqlalchemy import Column,Integer,String,Date,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

#You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

    
def _get_date():
    return datetime.datetime.now()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String(32))
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            #valid token, but has expired
            return None
        except BadSignature:
            #invalid token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        return {
        'username' : self.username,
        'id' : self.id
    }

class Platform(Base):
    __tablename__ = 'platform'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    release_date = Column(Date)
    manufacturer = Column(String(250))
    created = Column(Date, default=_get_date)
    updated = Column(Date, onupdate=_get_date)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'id' : self.id,
        'release_date' : self.release_date,
        'manufacturer' : self.manufacturer
    }

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    release_date = Column(Date)
    developer = Column(String(250))
    publisher = Column(String(250))
    platform_id = Column(String(250), ForeignKey('platform.id'))
    created = Column(Date, default=_get_date)
    updated = Column(Date, onupdate=_get_date)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialze(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'id' : self.id,
        'publisher' : self.publisher,
        'developer' : self.developer,
        'release_date' : self.release_date,
        'platform_id' : self.platform
    }


engine = create_engine('sqlite:///catalog-app.db')

Base.metadata.create_all(engine)