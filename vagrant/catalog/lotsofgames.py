from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Platform, Game

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

platform1 = Platform(user_id=1, name='Playstation', manufacturer='Sony', release_date='1994-12-03')

session.add(platform1)
session.commit()

game1 = Game(user_id=1, name='Metal Gear Solid', developer='Konami Computer Entertainment Japan', 
    publisher='Konami', platform=1, release_date='1996-12-03')

session.add(game1)

session.commit()

game2 = Game(user_id=1, name='Gran Turismo', developer='Polys Entertainment', 
    publisher='Sony Computer Entertainment', platform=1, release_date='1998-09-03')

session.add(game2)

session.commit()

game3 = Game(user_id=1, name='Resident Evil 2', developer='Capcom', publisher='Capcom', 
    platform=1, release_date='1998-01-21')

session.add(game3)

session.commit()

game4 = Game(user_id=1, name='Tekken 3', developer='Namco', publisher='Namco Hometek', 
    platform=1, release_date='1998-04-29')

session.add(game4)

session.commit()

