"""
Script para inicializar conquistas padrão do EduMatch
Execute este arquivo para popular o banco de dados com conquistas iniciais
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, create_db_and_tables
from app.models.achievement import Achievement

def init_achievements():
    """
    Cria conquistas iniciais no banco de dados
    """
    # Criar tabelas se não existirem
    create_db_and_tables()
    
    session = SessionLocal()
    
    # Lista de conquistas iniciais
    achievements_data = [
        {
            "name": "Primeiro Passo",
            "description": "Conclua sua primeira meta de aprendizado!",
            "points_required": 50
        },
        {
            "name": "Estudante Dedicado",
            "description": "Acumule 100 MatchPoints!",
            "points_required": 100
        },
        {
            "name": "Em Chamas! 🔥",
            "description": "Alcance 250 MatchPoints!",
            "points_required": 250
        },
        {
            "name": "Aprendiz Determinado",
            "description": "Conquiste 500 MatchPoints e alcance o nível 2!",
            "points_required": 500
        },
        {
            "name": "Mestre do Conhecimento",
            "description": "Acumule 1000 MatchPoints!",
            "points_required": 1000
        },
        {
            "name": "Gênio em Ascensão",
            "description": "Alcance 2500 MatchPoints!",
            "points_required": 2500
        },
        {
            "name": "Lenda do EduMatch",
            "description": "Conquiste incríveis 5000 MatchPoints!",
            "points_required": 5000
        },
        {
            "name": "Guardião do Saber",
            "description": "Atinja 10000 MatchPoints - O Edu está sem palavras!",
            "points_required": 10000
        }
    ]
    
    try:
        # Verificar quais conquistas já existem
        existing_achievements = session.query(Achievement).all()
        existing_names = {ach.name for ach in existing_achievements}
        
        added_count = 0
        for ach_data in achievements_data:
            if ach_data["name"] not in existing_names:
                achievement = Achievement(**ach_data)
                session.add(achievement)
                added_count += 1
                print(f"✅ Conquista adicionada: {ach_data['name']}")
            else:
                print(f"⏭️  Conquista já existe: {ach_data['name']}")
        
        session.commit()
        print(f"\n🎉 Inicialização completa! {added_count} nova(s) conquista(s) adicionada(s)!")
        print(f"🐶 O Edu está animado com as {len(achievements_data)} conquistas disponíveis!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inicializar conquistas: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 Iniciando configuração de conquistas do EduMatch...")
    print("🐶 O Edu está preparando as medalhas...\n")
    init_achievements()
