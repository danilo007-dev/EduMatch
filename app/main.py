from fastapi import FastAPI
from app.routes import auth, gamification
from app.database import create_db_and_tables

# Criar aplicação FastAPI
app = FastAPI(
    title="EduMatch API", 
    description="🎮 Plataforma de aprendizado gamificada com IA - Assistido pelo Edu",
    version="1.0.0"
)

# Incluir rotas
app.include_router(auth.router, tags=["Autenticação"])
app.include_router(gamification.router, prefix="/gamification", tags=["🎮 Gamificação"])

@app.on_event("startup")
def on_startup():
    """Criar banco de dados na inicialização"""
    create_db_and_tables()

@app.get("/")
def read_root():
    return {
        "message": "🐶 Bem-vindo ao EduMatch API! Eu sou o Edu, seu assistente de aprendizado! 🚀",
        "docs": "Acesse /docs para ver a documentação interativa",
        "version": "1.0.0",
        "features": [
            "🔐 Autenticação JWT",
            "🎮 Sistema de Gamificação (MatchPoints, Níveis e Conquistas)",
            "🏆 Conquistas Desbloqueáveis",
            "🐾 Edu - Seu companheiro virtual"
        ]
    }
