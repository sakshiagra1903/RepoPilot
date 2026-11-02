import re
from pydantic import BaseModel, Field, ConfigDict, field_validator
class RegisterIn(BaseModel):
    email:str; password:str=Field(min_length=10,max_length=128); full_name:str=Field(min_length=1,max_length=120)
    @field_validator('email')
    @classmethod
    def valid_email(cls,v):
        v=v.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",v): raise ValueError('Enter a valid email address')
        return v
class LoginIn(BaseModel):
    email:str; password:str
    @field_validator('email')
    @classmethod
    def valid_email(cls,v):
        v=v.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",v): raise ValueError('Enter a valid email address')
        return v
class TokenOut(BaseModel): access_token:str; refresh_token:str; token_type:str='bearer'
class UserOut(BaseModel): id:int; email:str; full_name:str; model_config=ConfigDict(from_attributes=True)
class RepoConnectIn(BaseModel): full_name:str=Field(pattern=r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
class ChatIn(BaseModel): repository_id:int; question:str=Field(min_length=3,max_length=4000); session_id:int|None=None
class TestIn(BaseModel): code:str=Field(min_length=1,max_length=30000); function_name:str|None=None
class ImproveIn(BaseModel): code:str=Field(min_length=1,max_length=30000)
class ProposalIn(BaseModel): repository_id:int; title:str=Field(min_length=3,max_length=200); description:str=''; patch:str=Field(min_length=1,max_length=100000)
