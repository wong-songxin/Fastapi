

from pydantic import BaseModel,Field,ConfigDict
class LeaveInSchema(BaseModel):
    reason:str
    time:str
    days:str
    type:int

class UserInfoSchema(BaseModel):
    id:int
    nick_name:str

    model_config = ConfigDict(from_attributes=True)
class LeaveOutSchema(BaseModel):
    id:int
    reason: str
    time: str
    days: str
    type: int
    status:int
    owner:UserInfoSchema|None
    
    model_config = ConfigDict(from_attributes=True)