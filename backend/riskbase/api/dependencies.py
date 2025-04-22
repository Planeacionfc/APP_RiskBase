from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..domain.auth import get_current_user
from ..domain.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Nuevo get_current_user que toma el token del header Authorization (Bearer ...)
def get_current_user_dependency(token: str = Depends(oauth2_scheme)) -> User:
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="No se pudo validar credenciales")
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user_dependency),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return current_user
