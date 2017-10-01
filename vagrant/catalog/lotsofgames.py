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

platform1 = Platform(id=1, user_id=1, name='Playstation', medium='CD',
                     internet_enabled=False,
                     controller_ports=2, manufacturer='Sony',
                     release_date=datetime.date(1994, 12, 3))

session.add(platform1)
session.commit()

game1 = Game(user_id=1, title='Metal Gear Solid',
             developer='Konami Computer Entertainment Japan',
             publisher='Konami', platform_id=1,
             release_date=datetime.date(1996, 12, 3))

session.add(game1)

session.commit()

game2 = Game(user_id=1, title='Gran Turismo', developer='Polys Entertainment',
             publisher='Sony Computer Entertainment', platform_id=1,
             release_date=datetime.date(1998, 9, 3))

session.add(game2)

session.commit()

game3 = Game(user_id=1, title='Resident Evil 2', developer='Capcom',
             publisher='Capcom', platform_id=1,
             release_date=datetime.date(1998, 01, 21))

session.add(game3)

session.commit()

game4 = Game(user_id=1, title='Tekken 3', developer='Namco',
             publisher='Namco Hometek', platform_id=1,
             release_date=datetime.date(1998, 04, 29))

session.add(game4)

session.commit()


platform2 = Platform(id=2, user_id=1, name='Nintendo 64',
                     manufacturer='Nintendo', release_date=datetime.date(
                         1996, 9, 26), medium='cartridge',
                     internet_enabled=False, controller_ports=4)

session.add(platform2)
session.commit()

game5 = Game(user_id=1, title='Super Mario 64', developer='Nintendo EAD',
             genre='platform adventure', multiplayer=False,
             online_multiplayer=False, multiplatform=False,
             publisher='Nintendo', platform_id=2,
             release_date=datetime.date(1996, 12, 3))

session.add(game5)

session.commit()

game6 = Game(user_id=1, title='Mario Kart 64', developer='Nintendo EAD',
             genre='kart racer', multiplayer=True, online_multiplayer=False,
             multiplatform=False, publisher='Nintendo', platform_id=2,
             release_date=datetime.date(1998, 9, 3))

session.add(game6)

session.commit()

game7 = Game(user_id=1, title='The Legend of Zelda: Ocarina of Time',
             developer='Nintendo EAD', genre='adventure', multiplayer=False,
             online_multiplayer=False, multiplatform=False,
             publisher='Nintendo', platform_id=2,
             release_date=datetime.date(1998, 01, 21))

session.add(game7)

session.commit()

game8 = Game(user_id=1, title='Perfect Dark\"', developer='Rare',
             publisher='Nintendo', genre='Shooter', multiplayer=True,
             online_multiplayer=False, multiplatform=False, platform_id=2,
             release_date=datetime.date(1998, 04, 29))

session.add(game8)

session.commit()


platform3 = Platform(id=3, user_id=1, name='Xbox 360',
                     manufacturer='Microsoft',
                     release_date=datetime.date(2005, 11, 22), medium='DVD',
                     internet_enabled=True, controller_ports=3)

session.add(platform3)
session.commit()

game9 = Game(user_id=1, title='Halo 3', developer='Bungie Studios',
             genre='Shooter', multiplayer=True, online_multiplayer=True,
             multiplatform=False, publisher='Microsoft Game Studios',
             platform_id=3, release_date=datetime.date(2006, 11, 25))

session.add(game9)

session.commit()

game10 = Game(user_id=1, title='Gears of War', developer='Epic Games',
              genre='Shooter', multiplayer=True, online_multiplayer=True,
              multiplatform=False, publisher='Microsoft Game Studios',
              platform_id=3, release_date=datetime.date(2013, 9, 10))

session.add(game10)

session.commit()

game11 = Game(user_id=1, title='NHL 2K14', developer='EA Sports',
              genre='Sports', multiplayer=True,
              online_multiplayer=True, multiplatform=True, publisher='EA',
              platform_id=3, release_date=datetime.date(2013, 9, 10))

session.add(game11)

session.commit()

game12 = Game(user_id=1, title='Grand Theft Auto V',
              developer='Rockstar North', publisher='Rockstar Games',
              genre='Sandbox Shooter', multiplayer=True,
              online_multiplayer=True, multiplatform=True,
              platform_id=3, release_date=datetime.date(2013, 9, 17))

session.add(game12)

session.commit()

game12 = Game(user_id=1, title='Halo 3 ODST', developer='Bungie Studios',
              publisher='Microsoft Games', genre='Shooter', multiplayer=True,
              online_multiplayer=True, multiplatform=False,
              platform_id=3, release_date=datetime.date(2009, 9, 22))

session.add(game12)

session.commit()
