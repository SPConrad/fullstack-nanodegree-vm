from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from models import Base, User, Platform, Game

engine = create_engine('sqlite:///catalog-app.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


User2 = User(id=2, username='voltaspistol', password_hash='sporksandorks')
User3 = User(id=3, username='kandoras', password_hash='notapaladin')


session.add(User2)
session.commit()

session.add(User3)
session.commit()

platform1 = Platform(id=1, user_id=1, name='Playstation', manufacturer='Sony', release_date=datetime.date(1994, 12, 3))

session.add(platform1)
session.commit()

game1 = Game(user_id=4, title='Metal Gear Solid', developer='Konami Computer Entertainment Japan', 
    publisher='Konami', platform_id=1, release_date=datetime.date(1996, 12, 3))

session.add(game1)

session.commit()

game2 = Game(user_id=4, title='Gran Turismo', developer='Polys Entertainment', 
    publisher='Sony Computer Entertainment', platform_id=1, release_date=datetime.date(1998, 9, 3))

session.add(game2)

session.commit()

game3 = Game(user_id=4, title='Resident Evil 2', developer='Capcom', publisher='Capcom', 
    platform_id=1, release_date=datetime.date(1998, 01, 21))

session.add(game3)

session.commit()

game4 = Game(user_id=4, title='Tekken 3', developer='Namco', publisher='Namco Hometek', 
    platform_id=1, release_date=datetime.date(1998, 04, 29))

session.add(game4)

session.commit()


platform2 = Platform(id=2, user_id=1, name='Nintendo 64', manufacturer='Nintendo', release_date=datetime.date(1996, 9, 26))

session.add(platform2)
session.commit()

game5 = Game(user_id=4, title='Super Mario 64', developer='Nintendo EAD', 
    publisher='Nintendo', platform_id=2, release_date=datetime.date(1996, 12, 3))

session.add(game5)

session.commit()

game6 = Game(user_id=4, title='Mario Kart 64', developer='Nintendo EAD', 
    publisher='Nintendo', platform_id=2, release_date=datetime.date(1998, 9, 3))

session.add(game6)

session.commit()

game7 = Game(user_id=4, title='The Legend of Zelda: Ocarina of Time', developer='Nintendo EAD',
    publisher='Nintendo', platform_id=2, release_date=datetime.date(1998, 01, 21))

session.add(game7)

session.commit()

game8 = Game(user_id=4, title='Perfect Dark\"', developer='Rare', publisher='Nintendo', 
    platform_id=2, release_date=datetime.date(1998, 04, 29))

session.add(game8)

session.commit()