from fastapi import APIRouter, Depends, status
from db.database import Session, engine
from model.models import User
from schema.schemas import SignUpModel
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash
 
auth_router = APIRouter(tags=['Auth'])

session = Session(bind=engine)

@auth_router.get('/')
async def auth_test():
    return {
        'message':'Test auth'
    }

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    print(user)
    print("========")
    db_email = session.query(User).filter(User.user_email == user.user_email).first()
    
    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with the email already exists'

        )
    
    
    db_name = session.query(User).filter(User.user_name == user.user_email).first()
    
    if db_name is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with the name already exists'

        )
    
    new_user = User(
        user_name = user.user_name, 
        user_email = user.user_email, 
        password = generate_password_hash(user.password),
        is_activate = user.is_activate, 
        is_staff = user.is_staff 
    ) 
    
    session.add(new_user)
    
    session.commit()
    
    return new_user