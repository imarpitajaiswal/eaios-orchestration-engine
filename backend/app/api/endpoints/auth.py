from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token

router = APIRouter()

# 1. Define the OAuth2 Scheme
# This exact line is what tells Swagger UI to render the green "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """OAuth2 compatible token login, required for Next.js frontend."""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    
    return {
        "access_token": create_access_token(subject=user.email),
        "token_type": "bearer",
    }

# 2. A Protected Route
# The `Depends(oauth2_scheme)` acts as the bouncer. It requires a valid JWT to enter.
@router.get("/verify-token")
def verify_secure_access(token: str = Depends(oauth2_scheme)):
    """Test endpoint to verify the cryptographic padlock is working."""
    return {
        "status": "success", 
        "message": "Cryptographic handshake verified.", 
        "token": token
    }