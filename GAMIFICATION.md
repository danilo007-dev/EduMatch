# 🎮 Sistema de Gamificação do EduMatch

## Visão Geral

O sistema de gamificação transforma o aprendizado em uma experiência divertida e motivadora, onde o **Edu** 🐶 acompanha cada passo do usuário!

## 🏗️ Estrutura

### Modelos

#### 📊 Progress (Progresso)
- **matchpoints**: Pontuação acumulada do usuário
- **level**: Nível atual (calculado: `level = (matchpoints // 500) + 1`)
- Relacionamento 1:1 com User

#### 🏆 Achievement (Conquista)
- **name**: Nome da conquista
- **description**: Descrição do que foi alcançado
- **points_required**: MatchPoints necessários para desbloquear
- Relacionamento many-to-many com User

### 🎯 Sistema de Pontos (MatchPoints)

- Cada ação de aprendizado gera MatchPoints
- **500 pontos = 1 nível**
- O Edu comemora cada conquista! 🐾

## 📡 Endpoints Disponíveis

### 1. Consultar Progresso
```http
GET /gamification/progress/{user_id}
```

**Resposta:**
```json
{
  "message": "🐾 O Edu está orgulhoso de você! Você está no nível 4 com 820 MatchPoints!",
  "progress": {
    "matchpoints": 820,
    "level": 4
  }
}
```

### 2. Adicionar Pontos
```http
POST /gamification/progress/add
```

**Body:**
```json
{
  "user_id": 1,
  "points": 100
}
```

**Resposta (sem subir de nível):**
```json
{
  "message": "🎉 Muito bem! +100 MatchPoints! O Edu está aplaudindo (com as patinhas)!",
  "progress": {
    "matchpoints": 920,
    "level": 4
  },
  "level_up": false
}
```

**Resposta (subindo de nível):**
```json
{
  "message": "🎉 Uau! O Edu está latindo de alegria! Você ganhou 100 MatchPoints e subiu para o nível 5!",
  "progress": {
    "matchpoints": 1020,
    "level": 5
  },
  "level_up": true
}
```

### 3. Listar Conquistas do Usuário
```http
GET /gamification/achievements/{user_id}
```

**Resposta:**
```json
{
  "message": "🏆 Aqui estão suas 3 conquista(s)! O Edu está muito orgulhoso!",
  "achievements": [
    {
      "id": 1,
      "name": "Primeiro Passo",
      "description": "Conclua sua primeira meta de aprendizado!",
      "points_required": 50
    }
  ]
}
```

### 4. Listar Todas as Conquistas Disponíveis
```http
GET /gamification/achievements
```

### 5. Desbloquear Conquistas
```http
POST /gamification/achievements/unlock
```

**Body:**
```json
{
  "user_id": 1,
  "points": 0
}
```

**Resposta:**
```json
{
  "message": "🏆 Parabéns! O Edu trouxe uma medalha nova: 'Primeiro Passo'!",
  "unlocked": [
    {
      "id": 1,
      "name": "Primeiro Passo",
      "description": "Conclua sua primeira meta de aprendizado!",
      "points_required": 50
    }
  ]
}
```

### 6. Criar Nova Conquista (Admin)
```http
POST /gamification/achievements/create?name=Nome&description=Descrição&points_required=100
```

## 🏆 Conquistas Iniciais

| Conquista | Descrição | MatchPoints Necessários |
|-----------|-----------|------------------------|
| 🥇 Primeiro Passo | Conclua sua primeira meta de aprendizado! | 50 |
| 📚 Estudante Dedicado | Acumule 100 MatchPoints! | 100 |
| 🔥 Em Chamas! | Alcance 250 MatchPoints! | 250 |
| 🎯 Aprendiz Determinado | Conquiste 500 MatchPoints e alcance o nível 2! | 500 |
| 🧠 Mestre do Conhecimento | Acumule 1000 MatchPoints! | 1000 |
| ⭐ Gênio em Ascensão | Alcance 2500 MatchPoints! | 2500 |
| 👑 Lenda do EduMatch | Conquiste incríveis 5000 MatchPoints! | 5000 |
| 🛡️ Guardião do Saber | Atinja 10000 MatchPoints - O Edu está sem palavras! | 10000 |

## 🚀 Como Inicializar

### 1. Criar as tabelas
```bash
uvicorn app.main:app --reload
```

### 2. Popular conquistas iniciais
```bash
python init_achievements.py
```

### 3. Testar no navegador
Acesse: http://127.0.0.1:8000/docs

## 🐶 Personalidade do Edu

O Edu é o mascote virtual do EduMatch! Ele:
- 🎉 Celebra cada conquista
- 💪 Motiva nos momentos difíceis
- 🏆 Comemora quando você sobe de nível
- 🐾 Está sempre presente nas respostas da API

### Exemplos de Mensagens do Edu:

**Progresso:**
- "🐾 O Edu está orgulhoso de você!"
- "🐶 Uau! O Edu está impressionado!"

**Subida de Nível:**
- "🎉 Uau! O Edu está latindo de alegria!"
- "🚀 INCRÍVEL! O Edu está muito orgulhoso!"

**Motivação:**
- "🐶 O Edu acredita em você!"
- "💪 Não desista! O Edu está aqui para te apoiar!"

**Conquistas:**
- "🏆 Parabéns! O Edu trouxe uma medalha nova!"
- "🎊 CONQUISTA DESBLOQUEADA! O Edu está super empolgado!"

## 💡 Próximos Passos

- [ ] Adicionar streaks (dias consecutivos de estudo)
- [ ] Sistema de rankings entre usuários
- [ ] Desafios diários
- [ ] Recompensas especiais
- [ ] Integração com IA para desafios personalizados

---

**Desenvolvido com 💙 pelo Edu e sua equipe!**
