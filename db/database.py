from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql://admin:1234@localhost:5431/postgres',
                       echo=True
                       ) 

Base = declarative_base()
Session = sessionmaker() 

