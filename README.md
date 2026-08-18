# HealthAssist API - Triagem Médica

API desenvolvida para o Projeto de Bloco de Análise e Segurança de Agentes de IA (Tema 3).

## Objetivo
Servir como backend seguro para triagem médica automatizada, priorizando o cumprimento da LGPD para dados sensíveis de saúde e prevenindo ataques de Negação de Serviço (DoS).

## Como Executar Localmente

1. Instalar dependências:
   pip install -r requirements.txt

2. Iniciar servidor:
   uvicorn app.main:app --reload

3. Endpoints principais:
   - GET /health: Estado da API (Acesso público).
   - POST /auth/token: Autenticação e geração do token JWT.
   - POST /predict: Classificação de triagem (Requer autenticação Bearer JWT).
