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