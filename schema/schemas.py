from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    user_name: str 
    user_email: str 
    password: str 
    is_staff: Optional[bool]
    is_activate: Optional[bool] 
    
    class Config:
        orm_mode = True 
        scheme_extra = {
            'example':{
                'user_name': 'test_user', 
                'user_email': 'test@test.com', 
                'password': 'password',
                'is_staff': False, 
                'is_activate': True 
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str = '1c869dd3c47764cb0cfbd0b2818ea3efcea1a330d17cdff0b28e00c66111b45c'


class LoginModel(BaseModel):
    user_name:str 
    password:str 


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int    
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'SMALL'
    user_id: Optional[int] 
    
    class Confing: 
        orm_mode = True 
        scheme_extra = {
            'example':{
                'quantity': 2, 
                'pizza_size': 'SMALL'
            }
        }
