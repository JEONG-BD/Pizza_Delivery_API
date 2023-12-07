from .database import engine, Base 
from model.models import User, Orders 

Base.metadata.create_all(bind=engine)