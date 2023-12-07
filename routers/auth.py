from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schema.schemas import SignUpModel, LoginModel
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import  AuthJWT
from fastapi.encoders import jsonable_encoder 
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import Session, engine
from model.models import User
 
auth_router = APIRouter(tags=['Auth'])

session = Session(bind=engine)

@auth_router.get('/')
async def auth_test(Authorize: AuthJWT=Depends()):
    try :
        Authorize.jwt_required()
    except Exception as ex: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )
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
    
    return new_user\
        
@auth_router.post('/login')
async def login(user:LoginModel, Authorize: AuthJWT=Depends()):
    print(user, user.__dict__)
    print('--')
    db_user = session.query(User).filter(User.user_name== user.user_name).first()
    
    if db_user is not None and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.user_name)
        refresh_token = Authorize.create_refresh_token(subject=db_user.user_name)
        
        response = {
            'access':access_token, 
            'refresh':refresh_token
        }      
         
        return jsonable_encoder(response)

    else : 
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail = 'Invalid User name or password'
        )    


@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT=Depends()):
    try :
        Authorize.jwt_refresh_token_required()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = 'Please provide a valid refresh token'
        )
    current_user = Authorize._get_jwt_identifier()
    print(current_user)
    print("----------")
    
    access_token = Authorize.create_access_token(subject=current_user)
    
    return jsonable_encoder(access_token)
    
    