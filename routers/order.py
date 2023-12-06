from fastapi import APIRouter 

order_router = APIRouter(tags=['Order'])

@order_router.get('/')
async def order_test():
    return {
        'message':'Test order'
    }