from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Importar todos os modelos para garantir que as tabelas sejam criadas
from app.models.user import Base
from app.models.progress import Progress
from app.models.achievement import Achievement, user_achievements

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./edumatch.db"

# Criação do engine
engine = create_engine(DATABASE_URL, echo=True)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Cria o banco de dados e as tabelas
    Importa todos os modelos para garantir que sejam registrados
    """
    # Importar modelos aqui garante que todos estejam registrados
    import app.models.user
    import app.models.progress
    import app.models.achievement
    
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