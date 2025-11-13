from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import random

from app.database import get_session
from app.models.progress import Progress
from app.models.achievement import Achievement
from app.models.user import User

router = APIRouter()

# Schemas para requests e responses
class AddPointsRequest(BaseModel):
    user_id: int
    points: int

class ProgressResponse(BaseModel):
    matchpoints: int
    level: int

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    points_required: int
    
    class Config:
        from_attributes = True

# Funções auxiliares para calcular nível
def calculate_level(matchpoints: int) -> int:
    """
    Calcula o nível baseado nos MatchPoints
    Cada nível = 500 pontos
    """
    return (matchpoints // 500) + 1

def get_edu_progress_message(username: str, level: int, matchpoints: int) -> str:
    """Mensagens do Edu sobre o progresso"""
    messages = [
        f"🐾 O Edu está orgulhoso de você, {username}! Você está no nível {level} com {matchpoints} MatchPoints!",
        f"🐶 Uau, {username}! Nível {level} e {matchpoints} MatchPoints! O Edu está impressionado!",
        f"✨ Incrível, {username}! Você alcançou o nível {level} com {matchpoints} MatchPoints! Continue assim!",
        f"🎯 {username}, você está arrasando! Nível {level} e {matchpoints} MatchPoints! O Edu está latindo de alegria!"
    ]
    return random.choice(messages)

def get_edu_points_added_message(username: str, points: int, new_level: int, level_up: bool) -> str:
    """Mensagens do Edu quando pontos são adicionados"""
    if level_up:
        messages = [
            f"🎉 Uau! O Edu está latindo de alegria! Você ganhou {points} MatchPoints e subiu para o nível {new_level}!",
            f"🚀 INCRÍVEL, {username}! +{points} MatchPoints e você alcançou o nível {new_level}! O Edu está muito orgulhoso!",
            f"⭐ PARABÉNS! {points} MatchPoints conquistados e NÍVEL {new_level} DESBLOQUEADO! O Edu não para de abanar o rabo!",
            f"🏆 QUE SHOW! Você ganhou {points} MatchPoints e chegou ao nível {new_level}! O Edu preparou uma festinha virtual! 🎊"
        ]
    else:
        messages = [
            f"🎉 Muito bem, {username}! +{points} MatchPoints! O Edu está aplaudindo (com as patinhas)!",
            f"✨ Excelente! +{points} MatchPoints adicionados! O Edu está orgulhoso do seu progresso!",
            f"🐾 Boa, {username}! Você ganhou {points} MatchPoints! Continue assim que logo vem o próximo nível!",
            f"💪 Isso aí! +{points} MatchPoints! O Edu sabe que você vai longe!"
        ]
    return random.choice(messages)

def get_edu_low_progress_message(username: str) -> str:
    """Mensagens motivacionais do Edu"""
    messages = [
        f"🐶 O Edu acredita em você, {username}! Continue aprendendo que logo vem o próximo nível!",
        f"💪 Não desista, {username}! O Edu está aqui para te apoiar em cada passo!",
        f"🌟 Cada passo conta, {username}! O Edu sabe que você é capaz de grandes conquistas!",
        f"🎯 Continue focado, {username}! O Edu vai estar ao seu lado em toda a jornada!"
    ]
    return random.choice(messages)

def get_edu_achievement_message(username: str, achievement_name: str) -> str:
    """Mensagens do Edu ao desbloquear conquista"""
    messages = [
        f"🏆 Parabéns, {username}! O Edu trouxe uma medalha nova: '{achievement_name}'!",
        f"🎊 CONQUISTA DESBLOQUEADA! '{achievement_name}'! O Edu está super empolgado!",
        f"⭐ {username}, você desbloqueou: '{achievement_name}'! O Edu preparou biscoitos virtuais para comemorar! 🍪",
        f"🌟 QUE INCRÍVEL! Conquista '{achievement_name}' alcançada! O Edu não cabe em si de felicidade!"
    ]
    return random.choice(messages)

# Rotas

@router.get("/progress/{user_id}")
async def get_progress(user_id: int, session: Session = Depends(get_session)):
    """
    🐾 Obtém o progresso atual do usuário
    """
    # Buscar usuário
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="🚫 Usuário não encontrado! O Edu não conseguiu localizar este perfil."
        )
    
    # Buscar ou criar progresso
    progress = session.query(Progress).filter(Progress.user_id == user_id).first()
    if not progress:
        # Criar progresso inicial
        progress = Progress(user_id=user_id, matchpoints=0, level=1)
        session.add(progress)
        session.commit()
        session.refresh(progress)
    
    return {
        "message": get_edu_progress_message(user.username, progress.level, progress.matchpoints),
        "progress": {
            "matchpoints": progress.matchpoints,
            "level": progress.level
        }
    }

@router.post("/progress/add")
async def add_points(request: AddPointsRequest, session: Session = Depends(get_session)):
    """
    🎯 Adiciona MatchPoints ao usuário e recalcula o nível
    """
    # Buscar usuário
    user = session.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="🚫 Usuário não encontrado! O Edu não conseguiu localizar este perfil."
        )
    
    # Buscar ou criar progresso
    progress = session.query(Progress).filter(Progress.user_id == request.user_id).first()
    if not progress:
        progress = Progress(user_id=request.user_id, matchpoints=0, level=1)
        session.add(progress)
    
    # Guardar nível anterior
    old_level = progress.level
    
    # Adicionar pontos
    progress.matchpoints += request.points
    
    # Recalcular nível
    new_level = calculate_level(progress.matchpoints)
    progress.level = new_level
    
    # Verificar se subiu de nível
    level_up = new_level > old_level
    
    session.commit()
    session.refresh(progress)
    
    return {
        "message": get_edu_points_added_message(user.username, request.points, new_level, level_up),
        "progress": {
            "matchpoints": progress.matchpoints,
            "level": progress.level
        },
        "level_up": level_up
    }

@router.get("/achievements/{user_id}")
async def get_user_achievements(user_id: int, session: Session = Depends(get_session)):
    """
    🏆 Lista todas as conquistas do usuário
    """
    # Buscar usuário
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="🚫 Usuário não encontrado! O Edu não conseguiu localizar este perfil."
        )
    
    # Buscar conquistas do usuário
    achievements = user.achievements
    
    if not achievements:
        return {
            "message": f"🐶 {user.username}, você ainda não tem conquistas! O Edu está ansioso para celebrar a primeira com você!",
            "achievements": []
        }
    
    return {
        "message": f"🏆 {user.username}, aqui estão suas {len(achievements)} conquista(s)! O Edu está muito orgulhoso!",
        "achievements": [
            {
                "id": ach.id,
                "name": ach.name,
                "description": ach.description,
                "points_required": ach.points_required
            }
            for ach in achievements
        ]
    }

@router.get("/achievements")
async def get_all_achievements(session: Session = Depends(get_session)):
    """
    📋 Lista todas as conquistas disponíveis no sistema
    """
    achievements = session.query(Achievement).all()
    
    return {
        "message": f"🏆 O Edu preparou {len(achievements)} conquistas para você desbloquear!",
        "achievements": [
            {
                "id": ach.id,
                "name": ach.name,
                "description": ach.description,
                "points_required": ach.points_required
            }
            for ach in achievements
        ]
    }

@router.post("/achievements/unlock")
async def unlock_achievements(request: AddPointsRequest, session: Session = Depends(get_session)):
    """
    🎊 Verifica e desbloqueia conquistas baseadas nos MatchPoints do usuário
    """
    # Buscar usuário
    user = session.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="🚫 Usuário não encontrado! O Edu não conseguiu localizar este perfil."
        )
    
    # Buscar progresso
    progress = session.query(Progress).filter(Progress.user_id == request.user_id).first()
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="🚫 Progresso não encontrado! O Edu recomenda começar sua jornada primeiro."
        )
    
    # Buscar conquistas disponíveis que o usuário ainda não tem
    user_achievement_ids = [ach.id for ach in user.achievements]
    available_achievements = session.query(Achievement).filter(
        Achievement.points_required <= progress.matchpoints,
        ~Achievement.id.in_(user_achievement_ids) if user_achievement_ids else True
    ).all()
    
    if not available_achievements:
        return {
            "message": f"🐶 {user.username}, você já desbloqueou todas as conquistas disponíveis no seu nível! O Edu está impressionado!",
            "unlocked": []
        }
    
    # Desbloquear as conquistas
    newly_unlocked = []
    for achievement in available_achievements:
        user.achievements.append(achievement)
        newly_unlocked.append({
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "points_required": achievement.points_required
        })
    
    session.commit()
    
    if len(newly_unlocked) == 1:
        message = get_edu_achievement_message(user.username, newly_unlocked[0]["name"])
    else:
        message = f"🎉 INCRÍVEL! {user.username} desbloqueou {len(newly_unlocked)} conquistas! O Edu está organizando uma festa! 🎊"
    
    return {
        "message": message,
        "unlocked": newly_unlocked
    }

@router.post("/achievements/create")
async def create_achievement(
    name: str,
    description: str,
    points_required: int,
    session: Session = Depends(get_session)
):
    """
    🎯 Cria uma nova conquista no sistema (admin)
    """
    # Verificar se já existe
    existing = session.query(Achievement).filter(Achievement.name == name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"🚫 A conquista '{name}' já existe! O Edu sugere escolher outro nome."
        )
    
    # Criar conquista
    achievement = Achievement(
        name=name,
        description=description,
        points_required=points_required
    )
    
    session.add(achievement)
    session.commit()
    session.refresh(achievement)
    
    return {
        "message": f"🏆 Conquista '{name}' criada com sucesso! O Edu está animado para ver os usuários desbloquearem!",
        "achievement": {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "points_required": achievement.points_required
        }
    }
