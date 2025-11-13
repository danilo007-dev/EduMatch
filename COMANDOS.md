# ⚡ COMANDOS RÁPIDOS - EduMatch

## 🚀 Iniciar o Projeto

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar servidor FastAPI
```bash
uvicorn app.main:app --reload
```

### 3. Popular conquistas (execute em outro terminal)
```bash
python init_achievements.py
```

### 4. Acessar documentação interativa
Abra no navegador: **http://127.0.0.1:8000/docs**

---

## 🧪 Testes

### Teste automatizado completo
```bash
python test_gamification.py
```

---

## 📡 Endpoints Principais

### Autenticação
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login
- `GET /me` - Informações do usuário logado

### Gamificação
- `GET /gamification/progress/{user_id}` - Ver progresso
- `POST /gamification/progress/add` - Adicionar pontos
- `GET /gamification/achievements` - Todas conquistas
- `GET /gamification/achievements/{user_id}` - Conquistas do usuário
- `POST /gamification/achievements/unlock` - Desbloquear conquistas

---

## 🎯 Teste Rápido no Swagger

1. Acesse http://127.0.0.1:8000/docs
2. Registre um usuário em `/register`
3. Veja progresso em `/gamification/progress/1`
4. Adicione pontos em `/gamification/progress/add`
5. Desbloqueie conquistas em `/gamification/achievements/unlock`
6. Veja suas conquistas em `/gamification/achievements/1`

---

## 📚 Documentação

- **README.md** - Visão geral do projeto
- **GAMIFICATION.md** - Documentação técnica completa
- **QUICK_START_GAMIFICATION.md** - Guia detalhado de uso
- **ETAPA_1.5_COMPLETA.md** - Resumo da implementação

---

## 🐶 O Edu está pronto para ajudar!

Divirta-se testando! 🎮🏆
