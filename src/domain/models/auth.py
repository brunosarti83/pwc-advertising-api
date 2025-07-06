from pydantic import BaseModel, EmailStr
from typing import Optional, Any

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SupabaseSession(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    user: Optional[Any] = None