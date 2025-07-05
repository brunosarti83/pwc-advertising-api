from fastapi import HTTPException
from supabase import Client

from src.dependencies import get_supabase
from src.domain.models import UserLogin
from src.domain.models import SupabaseSession

class AuthService:
    def __init__(self, supabase: Client = None):
        self.supabase = supabase or get_supabase()

    async def sign_up_user(self, user: UserLogin):
        response = self.supabase.auth.sign_up({"email": user.email, "password": user.password})
        if getattr(response, "error", None):
            raise HTTPException(status_code=400, detail=response.error.message)
        return {"message": "User created. Please verify your email to complete registration."}

    async def sign_in_user(self, user: UserLogin) -> SupabaseSession:
        response = self.supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})
        if getattr(response, "error", None):
            raise HTTPException(status_code=401, detail=response.error.message)
        return response
