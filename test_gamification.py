"""
Script de teste rápido para o sistema de gamificação
Testa as principais funcionalidades sem precisar do servidor
"""
from app.database import create_db_and_tables, SessionLocal
from app.models.user import User
from app.models.progress import Progress
from app.models.achievement import Achievement
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_gamification_system():
    """Testa o sistema de gamificação"""
    
    print("🚀 Iniciando teste do sistema de gamificação...")
    print("=" * 60)
    
    # Criar banco e tabelas
    print("\n1️⃣ Criando banco de dados e tabelas...")
    create_db_and_tables()
    print("✅ Banco criado com sucesso!")
    
    session = SessionLocal()
    
    try:
        # Criar usuário de teste
        print("\n2️⃣ Criando usuário de teste...")
        password_hash = pwd_context.hash("senha123")
        test_user = User(
            username="teste_edu",
            email="teste@edumatch.com",
            password_hash=password_hash
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        print(f"✅ Usuário criado: {test_user.username} (ID: {test_user.id})")
        
        # Criar progresso inicial
        print("\n3️⃣ Criando progresso inicial...")
        progress = Progress(
            user_id=test_user.id,
            matchpoints=0,
            level=1
        )
        session.add(progress)
        session.commit()
        session.refresh(progress)
        print(f"✅ Progresso criado: {progress.matchpoints} pontos, Nível {progress.level}")
        
        # Adicionar pontos
        print("\n4️⃣ Adicionando pontos...")
        progress.matchpoints += 100
        progress.level = (progress.matchpoints // 500) + 1
        session.commit()
        print(f"✅ +100 pontos! Total: {progress.matchpoints} pontos, Nível {progress.level}")
        
        # Adicionar mais pontos para subir de nível
        print("\n5️⃣ Adicionando mais pontos para subir de nível...")
        progress.matchpoints += 450
        progress.level = (progress.matchpoints // 500) + 1
        session.commit()
        print(f"✅ +450 pontos! Total: {progress.matchpoints} pontos, Nível {progress.level}")
        print("🎉 NÍVEL UP! O Edu está comemorando! 🐶")
        
        # Criar conquistas
        print("\n6️⃣ Criando conquistas de teste...")
        achievements_data = [
            Achievement(name="Primeiro Passo", description="Primeiros 50 pontos!", points_required=50),
            Achievement(name="Estudante Dedicado", description="100 pontos!", points_required=100),
            Achievement(name="Nível 2 Alcançado", description="500 pontos!", points_required=500)
        ]
        
        for ach in achievements_data:
            existing = session.query(Achievement).filter(Achievement.name == ach.name).first()
            if not existing:
                session.add(ach)
        
        session.commit()
        print("✅ Conquistas criadas!")
        
        # Desbloquear conquistas
        print("\n7️⃣ Verificando conquistas desbloqueadas...")
        available_achievements = session.query(Achievement).filter(
            Achievement.points_required <= progress.matchpoints
        ).all()
        
        for ach in available_achievements:
            if ach not in test_user.achievements:
                test_user.achievements.append(ach)
                print(f"🏆 Conquista desbloqueada: {ach.name}")
        
        session.commit()
        
        # Listar conquistas do usuário
        print("\n8️⃣ Conquistas do usuário:")
        for ach in test_user.achievements:
            print(f"  🏅 {ach.name}: {ach.description} ({ach.points_required} pontos)")
        
        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("🐶 O Edu está muito feliz com os resultados!")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_gamification_system()
