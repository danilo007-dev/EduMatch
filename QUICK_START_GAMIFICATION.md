# 🚀 Guia Rápido de Uso - Sistema de Gamificação

## 🎯 Passo a Passo para Testar

### 1. Instalar Dependências (se ainda não instalou)
```bash
pip install -r requirements.txt
```

### 2. Inicializar o Servidor
```bash
uvicorn app.main:app --reload
```

### 3. Inicializar Conquistas (em outro terminal)
```bash
python init_achievements.py
```

### 4. Acessar a Documentação Interativa
Abra seu navegador em: **http://127.0.0.1:8000/docs**

---

## 🧪 Testando as Funcionalidades

### Passo 1: Registrar um Usuário
**Endpoint:** `POST /register`
```json
{
  "username": "danilo",
  "email": "danilo@edumatch.com",
  "password": "senha123"
}
```

### Passo 2: Fazer Login
**Endpoint:** `POST /login`
```json
{
  "username": "danilo",
  "password": "senha123"
}
```
> 💡 Guarde o `user.id` da resposta!

### Passo 3: Verificar Progresso Inicial
**Endpoint:** `GET /gamification/progress/{user_id}`

Substitua `{user_id}` pelo ID retornado no login (geralmente 1).

### Passo 4: Adicionar Pontos
**Endpoint:** `POST /gamification/progress/add`
```json
{
  "user_id": 1,
  "points": 100
}
```

🎉 Teste adicionar diferentes quantidades:
- `50` pontos → Desbloqueia "Primeiro Passo"
- `100` pontos → Desbloqueia "Estudante Dedicado"
- `500` pontos → Sobe para nível 2!

### Passo 5: Desbloquear Conquistas
**Endpoint:** `POST /gamification/achievements/unlock`
```json
{
  "user_id": 1,
  "points": 0
}
```

### Passo 6: Ver Suas Conquistas
**Endpoint:** `GET /gamification/achievements/{user_id}`

### Passo 7: Ver Todas as Conquistas Disponíveis
**Endpoint:** `GET /gamification/achievements`

---

## 🎮 Testando Subida de Níveis

Para testar o sistema de níveis, adicione pontos gradualmente:

1. **Nível 1** (0-499 pontos)
   ```json
   {"user_id": 1, "points": 250}
   ```

2. **Nível 2** (500-999 pontos)
   ```json
   {"user_id": 1, "points": 300}
   ```
   🎉 Você subiu de nível!

3. **Nível 3** (1000-1499 pontos)
   ```json
   {"user_id": 1, "points": 500}
   ```

---

## 🐶 Mensagens do Edu

O Edu responde de forma personalizada em cada ação:

### 📊 Ao consultar progresso:
> "🐾 O Edu está orgulhoso de você, Danilo! Você está no nível 4 com 820 MatchPoints!"

### 🎉 Ao adicionar pontos (sem subir de nível):
> "🎉 Muito bem, Danilo! +100 MatchPoints! O Edu está aplaudindo (com as patinhas)!"

### 🚀 Ao subir de nível:
> "🎉 Uau! O Edu está latindo de alegria! Você ganhou 100 MatchPoints e subiu para o nível 5!"

### 🏆 Ao desbloquear conquista:
> "🏆 Parabéns, Danilo! O Edu trouxe uma medalha nova: 'Primeiro Passo'!"

---

## 🧪 Teste Automatizado

Execute o teste completo sem precisar do servidor:

```bash
python test_gamification.py
```

Este script testa:
- ✅ Criação de banco e tabelas
- ✅ Criação de usuário
- ✅ Sistema de pontos
- ✅ Cálculo de níveis
- ✅ Criação de conquistas
- ✅ Desbloqueio de conquistas

---

## 📊 Tabela de Níveis

| Nível | MatchPoints Necessários |
|-------|------------------------|
| 1 | 0 - 499 |
| 2 | 500 - 999 |
| 3 | 1000 - 1499 |
| 4 | 1500 - 1999 |
| 5 | 2000 - 2499 |
| 10 | 4500 - 4999 |
| 20 | 9500 - 9999 |

**Fórmula:** `level = (matchpoints // 500) + 1`

---

## 🎯 Exemplos de Uso Completo

### Cenário 1: Novo Usuário Começa a Aprender

1. **Registrar** → "🐶 Olá! Eu sou o Edu..."
2. **Consultar progresso** → "0 pontos, Nível 1"
3. **Completar primeira atividade** → `+50 pontos`
4. **Desbloquear conquista** → "🏆 Primeiro Passo!"

### Cenário 2: Usuário Evolui Rapidamente

1. **Adicionar 250 pontos** → "Quase lá!"
2. **Adicionar mais 300 pontos** → "🎉 NÍVEL 2!"
3. **Ver conquistas** → 3 medalhas desbloqueadas
4. **Adicionar 500 pontos** → "🚀 NÍVEL 3!"

---

## 🐛 Troubleshooting

### Erro: "Usuário não encontrado"
→ Certifique-se de usar o `user_id` correto

### Erro: "Módulo não encontrado"
→ Execute: `pip install -r requirements.txt`

### Banco não cria tabelas
→ Delete `edumatch.db` e reinicie o servidor

### Conquistas não aparecem
→ Execute: `python init_achievements.py`

---

## ✨ Próximos Passos

Após testar o sistema de gamificação:

1. ✅ Sistema de autenticação funcionando
2. ✅ Sistema de gamificação implementado
3. ⏭️ **Próximo:** Integrar com sistema de estudos
4. ⏭️ **Futuro:** Dashboard visual
5. ⏭️ **Futuro:** IA para personalização

---

**Divirta-se testando! 🐶🎮**

*O Edu está ansioso para acompanhar seu progresso!*
