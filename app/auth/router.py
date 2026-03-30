"""
Authentication router using Supabase Auth.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from app.db.supabase_client import supabase
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    user_id: str
    email: str


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Dependency to extract and verify the current user from the Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.replace("Bearer ", "")
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {
            "id": str(user_response.user.id),
            "email": user_response.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest):
    """Register a new user with email and password."""
    try:
        response = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Signup failed")

        return AuthResponse(
            access_token=response.session.access_token if response.session else "",
            user_id=str(response.user.id),
            email=response.user.email
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup error: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Log in an existing user."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })
        if not response.user or not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
            email=response.user.email
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login error: {str(e)}")


@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    """Log out the current user."""
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout error: {str(e)}")


@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""
    return user
