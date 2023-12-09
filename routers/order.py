from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException  
from fastapi_jwt_auth import AuthJWT 
from model.models import User, Orders 
from schema.schemas import OrderModel, OrderStatusModel
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
async def order_test(Authorize: AuthJWT=Depends()):
    """
        ## A order test route   
    """
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


@order_router.post('/')
async def place_an_order(order: OrderModel, Authorize: AuthJWT=Depends()):
    """
        ## A order insert route  
    """
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )

    current_user = Authorize.get_jwt_subject()    

    user = session.query(User).filter(User.user_name == current_user).first()

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


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = 'Invalid Token'
        )
    
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.user_name == current_user).first()
    print(user, type(user))
    print('='*20)
    
    if user.is_staff:
        orders = session.query(Orders).all()

        return jsonable_encoder(orders)

    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = 'You are not a super user'
    )
    

@order_router.get('/{id}')
async def get_order_by_id(id:int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.get_jwt_subject()
    except Exception as ex :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = 'Invalid Token'
        ) 
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.user_name == user).first()
    
    if current_user.is_staff:
        order = session.query(Orders).filter(Orders.id == id).first()
        
        return jsonable_encoder(order)
    
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = 'You are not a super user'
    )
    

@order_router.get('/user/')
async def get_order_by_user(Authorize : AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        
    except Exception as ex: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )

    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.user_name == user).first()
    
    return jsonable_encoder(current_user.orders)


@order_router.get('/user/{order_id}')
async def get_specific_user(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        
    except Exception as ex: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Token'
        )

    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.user_name == user).first()
    
    orders = current_user.orders
    print(orders)
    print('*'*30)
    for order in orders:
        if order.id == order_id :
            return jsonable_encoder(order)
    
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST, 
        detail = 'No order with search id' 
    )


@order_router.put('/update/orders/{order_id}')
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try :
        Authorize.jwt_required()
    except Exception as e : 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = 'Invalid Token'
        )
    order_db = session.query(Orders).filter(Orders.id == order_id).first()
    print(order_db.__dict__)
    print('*'*20)
    
    if not order_db : 
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = 'No order with search id'
        )
    
    order_db.quantity = order.quantity 
    order_db.pizza_size = order.pizza_size 
    print(order_db)
    session.commit()
    
    return jsonable_encoder(order_db)


@order_router.put('/update/status/{order_id}')
async def update_order_status(order_id: int, order: OrderStatusModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = 'Invalid Token'
        )
    
    user_name = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.user_name == user_name).first()
    
    if current_user.is_staff:
        order_db = session.query(Orders).filter(Orders.id == order_id).first()
        order_db.order_status = order.order_status 
        
        session.commit 
        
        return jsonable_encoder(order_db)
    
    raise HTTPException (
        status_code = status.HTTP_400_BAD_REQUEST, 
        detail = 'You are not a staff'
    )

@order_router.delete('/delete/{order_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = 'Invalid Token'
        ) 
    
    order_db = session.query(Orders).filter(Orders.id == order_id).first()
    
    if not order_db : 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = 'No order with search id' 
        ) 
    
    session.delete(order_db)
    session.commit()
    
    return jsonable_encoder(order_db)