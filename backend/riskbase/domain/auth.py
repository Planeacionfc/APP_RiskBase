from jose import JWTError, jwt
from passlib.context import CryptContext
from .models.user import User, UserInDB, TokenData, UserRole
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional
from datetime import datetime, timedelta


load_dotenv()

# Configuración de seguridad
db_url = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}/{os.getenv('DATABASE')}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Entidad User para la base de datos
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.ADMIN, nullable=False)
    is_active = Column(Boolean, default=True)

# Crear tabla y usuario admin predeterminado al iniciar

# def init_admin_user():
#     Base.metadata.create_all(bind=engine)
#     db = SessionLocal()
#     admin_user = db.query(UserDB).filter(UserDB.username == "admin").first()
#     if admin_user:
#         print("El usuario admin ya existe.")
#     else:
#         hashed_password = pwd_context.hash("admin123")
#         new_admin = UserDB(
#             username="admin",
#             email="admin@prebel.com",
#             hashed_password=hashed_password,
#             role=UserRole.ADMIN,
#             is_active=True
#         )
#         db.add(new_admin)
#         db.commit()
#         print("Usuario admin creado correctamente.")
#     db.close()

# # Ejecutar al importar este módulo
# init_admin_user()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[UserInDB]:
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user:
        return UserInDB(**user.__dict__)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str) -> Optional[UserInDB]:
    credentials_exception = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            credentials_exception = "Credenciales inválidas"
        token_data = TokenData(username=username)
    except JWTError:
        credentials_exception = "Credenciales inválidas"

    if credentials_exception:
        return None

    user = get_user(username=token_data.username)
    if user is None:
        return None
    return user
