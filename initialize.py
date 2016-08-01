from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database import Base, User, Gallery

engine = create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSessionMaker = sessionmaker(bind=engine)
dbSession = DBSessionMaker()

### These are the commands you just saw live.

marvin = User(
        firstname = 'Marvin',
        lastname = 'Arnold',
        email = 'marvin@meet.mit.edu',
        username = 'marvinarnold',
        password = '123',
        nationality = 'American',
        gender ='male',
        date = '14/12',
        bio = 'I like tacos and football',
        profilepic = 'pretty picture'
        )


# This deletes everything in your database.
dbSession.query(User).delete()
dbSession.commit()

# This adds some rows to the database. Make sure you `commit` after `add`ing!
dbSession.add(marvin)
dbSession.commit()
