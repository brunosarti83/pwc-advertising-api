from fastapi import APIRouter, Depends, HTTPException, Request
from supabase import Client

from src.dependencies import get_supabase
from src.domain.models.auth import SupabaseSession, UserLogin
from src.limiter import limiter
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/sign-up", status_code=201)
@limiter.limit("100/minute")
async def signup_user(request: Request, user: UserLogin, supabase: Client = Depends(get_supabase)):
    result = await AuthService(supabase=supabase).sign_up_user(user)
    return result

@router.post("/sign-in", response_model=SupabaseSession)
@limiter.limit("100/minute")
async def signin_user(request: Request, user: UserLogin, supabase: Client = Depends(get_supabase)):
    result = await AuthService(supabase=supabase).sign_in_user(user)
    if result.session:
        return SupabaseSession(
            access_token=getattr(result.session, "access_token", None),
            refresh_token=getattr(result.session, "refresh_token", None),
            token_type=getattr(result.session, "token_type", None),
            expires_in=getattr(result.session, "expires_in", None),
            user=result.user
        )
    raise HTTPException(status_code=401, detail="Invalid credentials or email not verified.")

@router.post("/sign-out")
@limiter.limit("100/minute")
async def signout_user(request: Request, supabase: Client = Depends(get_supabase)):
    result = await AuthService(supabase=supabase).sign_out_user()
    return { "message": "User signed out." }
