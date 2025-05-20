from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..dependencies import get_current_user, get_current_admin_user
from ...domain.models.user import User, Token, UserCreate
from ...domain.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user as get_current_user_auth,
    pwd_context,
    SessionLocal,
    UserDB,
    UserRole
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint para registrar un nuevo usuario
@router.post("/register", response_model=User, status_code=201)
async def register_user(user: UserCreate = Body(...), current_user: User = Depends(get_current_admin_user)):
    """
    Registra un nuevo usuario en el sistema.
    
    Este endpoint permite a los administradores crear nuevos usuarios en el sistema,
    verificando que el nombre de usuario y correo electrónico no existan previamente.
    La contraseña se almacena de forma segura utilizando hash.
    
    Args:
        user: Datos del nuevo usuario a crear (username, email, password, role)
        current_user: Usuario administrador autenticado que realiza el registro
    
    Permisos: Solo administradores
    
    Returns:
        User: Datos del usuario creado (sin la contraseña en texto plano)
    
    Raises:
        HTTPException: Si el usuario o email ya existe en la base de datos
    """
    db = SessionLocal()
    existing_user = db.query(UserDB).filter((UserDB.username == user.username) | (UserDB.email == user.email)).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="El usuario o email ya existe.")
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return User(
        username=db_user.username,
        email=db_user.email,
        hashed_password=db_user.hashed_password,
        role=db_user.role,
        is_active=db_user.is_active
    )

# Endpoint para iniciar sesión y obtener un token de acceso
@router.post("/login", response_model=Token)
async def login_user(email: str = Body(...), password: str = Body(...)):
    """
    Autentica a un usuario y genera un token de acceso.
    
    Este endpoint verifica las credenciales del usuario (email y contraseña) y,
    si son correctas, genera un token JWT con información del usuario y su rol,
    que se utilizará para autenticar solicitudes posteriores.
    
    Args:
        email: Correo electrónico del usuario
        password: Contraseña del usuario
    
    Permisos: Acceso público
    
    Returns:
        Token: Token de acceso JWT y su tipo
    
    Raises:
        HTTPException: Si las credenciales son incorrectas
    """
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.email == email).first()
    db.close()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}
