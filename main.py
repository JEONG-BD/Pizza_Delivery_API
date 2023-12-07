from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from routers.auth import auth_router 
from routers.order import order_router  
from schema.schemas import Settings 

import uvicorn

app = FastAPI() 
app.include_router(auth_router, prefix='/auth')
app.include_router(order_router, prefix='/order')

@AuthJWT.load_config
def get_config():
    return Settings()


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)