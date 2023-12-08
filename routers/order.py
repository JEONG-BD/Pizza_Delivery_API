from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException  
from fastapi_jwt_auth import AuthJWT 
from model.models import User, Orders 
from schema.schemas import OrderModel
from db.database import Session, engine
from fastapi.encoders import jsonable_encoder


order_router = APIRouter(tags=['Order'])


session = Session(bind=engine)

@order_router.get('/')
async def order_test():
    return {
        'message':'Test order'
    }


@order_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )
    return {
        'message':'Hello World'
    }


@order_router.post('/order')
async def place_an_order(order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )

    current_user = Authorize.get_jwt_subject()    
    print(current_user)
    user = session.query(User).filter(User.user_name == current_user).first()
    print(user)
    new_order = Orders(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )
    new_order.user = user 
    
    session.add(new_order)
    session.commit()
    
    response = {
        'pizza_size':new_order.pizza_size, 
        'quantity': new_order.quantity, 
        'id': new_order.id, 
        'order_statis': new_order.order_status
    }
    
    return jsonable_encoder(response)