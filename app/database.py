from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.user import Base
from typing import Generator

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./edumatch.db"

# Criação do engine
engine = create_engine(DATABASE_URL, echo=True)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Cria o banco de dados e as tabelas
    """
    Base.metadata.create_all(bind=engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()