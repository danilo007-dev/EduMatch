from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import random

from app.database import get_session
from app.models.user import User, UserCreate, UserLogin, UserResponse, Token

# Configurações de segurança
SECRET_KEY = "seu-secret-key-super-seguro-aqui"  # Em produção, use variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Busca usuário pelo username"""
    return session.query(User).filter(User.username == username).first()

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Busca usuário pelo email"""
    return session.query(User).filter(User.email == email).first()

def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    """Autentica usuário"""
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_edu_welcome_message(username: str) -> str:
    """Mensagens de boas-vindas do Edu com personalidade"""
    messages = [
        f"� Olá, {username}! Eu sou o Edu, seu novo companheiro de aprendizado! Pronto para começarmos sua jornada? ✨",
        f"🐶 Oi, {username}! Aqui é o Edu! Já estou preparando seus primeiros desafios de aprendizado. Que tal escolher uma meta semanal? 🎯",
        f"🐶 Bem-vindo ao EduMatch, {username}! Sou o Edu e estou super animado para te ajudar a aprender de forma divertida! 🚀",
        f"� E aí, {username}! Eu sou o Edu, seu assistente pessoal de estudos. Juntos vamos fazer seu aprendizado decolar! ✈️"
    ]
    return random.choice(messages)

def get_edu_login_message(username: str) -> str:
    """Mensagens de retorno do Edu"""
    messages = [
        f"� Bem-vindo de volta, {username}! O Edu sentiu sua falta 😄",
        f"🐶 Que bom te ver novamente, {username}! Tenho novidades incríveis para você! 🌟",
        f"🐶 Oi de novo, {username}! Preparei alguns exercícios especiais enquanto você estava fora! 📚",
        f"🐶 {username} voltou! O Edu está aqui e pronto para continuar nossa jornada de aprendizado! 🚀"
    ]
    return random.choice(messages)

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    � Cadastro de novo usuário com saudação especial do Edu
    """
    # Verificar se username já existe
    if get_user_by_username(session, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="🚫 Ops! Este nome de usuário já existe. O Edu sugere tentar outro! 😅"
        )
    
    # Verificar se email já existe
    if get_user_by_email(session, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="🚫 Este email já está cadastrado! O Edu lembra que você pode fazer login. 😊"
        )
    
    # Criar usuário
    password_hash = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    # Resposta com mensagem personalizada do Edu
    return {
        "message": get_edu_welcome_message(user.username),
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }

@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    � Login do usuário with saudação carinhosa do Edu
    """
    # Autenticar usuário
    user = authenticate_user(session, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="🚫 Usuário ou senha incorretos! O Edu sugere verificar os dados. 🔍",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Resposta com token e mensagem do Edu
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email
        ),
        message=get_edu_login_message(user.username)
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    � Obter informações do usuário autenticado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="🚫 Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(session, username)
    if user is None:
        raise credentials_exception
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email
    )