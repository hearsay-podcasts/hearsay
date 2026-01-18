from datetime import timedelta

from fastapi import APIRouter, HTTPException, Response, status

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.core.config import settings
from app.core.security import create_access_token
from app.models import LoginRequest, Message, UserCreate, UserPublic, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserPublic)
def login(
    response: Response,
    session: SessionDep,
    credentials: LoginRequest,
) -> UserPublic:
    """
    Login with email and password. Sets httpOnly cookie with JWT.
    """
    user = crud.authenticate(
        session=session,
        email=credentials.email,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
    )

    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT != "local",  # HTTPS only in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return UserPublic.model_validate(user)


@router.post("/signup", response_model=UserPublic)
def signup(
    response: Response,
    session: SessionDep,
    user_in: UserRegister,
) -> UserPublic:
    """
    Create new user account. Auto-logs in by setting httpOnly cookie.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    user_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)

    # Auto-login: create JWT and set cookie
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT != "local",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return UserPublic.model_validate(user)


@router.post("/logout", response_model=Message)
def logout(response: Response) -> Message:
    """
    Logout by clearing the access token cookie.
    """
    response.delete_cookie(key="access_token", path="/")
    return Message(message="Successfully logged out")


@router.get("/me", response_model=UserPublic)
def get_current_user_info(current_user: CurrentUser) -> UserPublic:
    """
    Get current authenticated user information.
    """
    return UserPublic.model_validate(current_user)
