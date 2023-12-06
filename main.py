from fastapi import FastAPI
from routers.auth import auth_router 
from routers.order import order_router  
import uvicorn

app = FastAPI() 
app.include_router(auth_router, prefix='/auth')
app.include_router(order_router, prefix='/order')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)