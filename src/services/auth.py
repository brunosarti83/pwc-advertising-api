from fastapi import HTTPException
from supabase import Client
from gotrue.errors import AuthApiError

from src.dependencies import get_supabase
from src.domain.models.auth import UserLogin, SupabaseSession

class AuthService:
    def __init__(self, supabase: Client = None):
        self.supabase = supabase or get_supabase()

    async def sign_up_user(self, user: UserLogin):
        try:
            response = self.supabase.auth.sign_up({"email": user.email, "password": user.password})
            if getattr(response, "error", None):
                raise HTTPException(status_code=400, detail=response.error.message)
            return {"message": "User created. Please verify your email to complete registration."}
        except AuthApiError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def sign_in_user(self, user: UserLogin) -> SupabaseSession:
        try:
            response = self.supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})
            if getattr(response, "error", None):
                raise HTTPException(status_code=400, detail=response.error.message)
            return response
        except AuthApiError as e:
            raise HTTPException(status_code=401, detail=str(e))
    
    async def sign_out_user(self):
        try:
            response = self.supabase.auth.sign_out()
            if getattr(response, "error", None):
                raise HTTPException(status_code=400, detail=response.error.message)
            return response
        except AuthApiError as e:
            raise HTTPException(status_code=400, detail=str(e))
