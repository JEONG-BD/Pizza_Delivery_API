from fastapi import APIRouter 

auth_router = APIRouter(tags=['Auth'])

@auth_router.get('/')
async def auth_test():
    return {
        'message':'Test auth'
    }