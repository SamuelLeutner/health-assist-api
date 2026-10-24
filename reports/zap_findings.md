# Relatório de Auditoria de Segurança — OWASP ZAP

## 1. Contexto e Escopo da Avaliação
Este relatório documenta a varredura de segurança automatizada executada com o **OWASP ZAP (Zed Attack Proxy)** sobre a API HealthAssist. O objetivo principal foi auditar a aplicação quanto a vulnerabilidades comuns de mercado (OWASP Top 10), tais como falhas de injeção, problemas de controle de acesso (BOLA), ausência de cabeçalhos de segurança e falhas nos fluxos de autenticação.

O escopo da varredura abrangeu os seguintes componentes principais expostos pela API:
- Endpoint de Autenticação (`/auth/token`)
- Endpoints de Status e Verificação de Integridade (`/health`)
- Endpoints Protegidos de Predição e Logs (`/predict/` e `/predict/{log_id}`)

---

## 2. Sumário Executivo dos Resultados
Após a execução completa da varredura ativa e passiva utilizando o ZAP, o resultado consolidado foi:
- **Alertas de Severidade Alta (High):** 0
- **Alertas de Severidade Média (Medium):** 0
- **Alertas de Severidade Baixa (Low):** Conforme esperado para configurações de framework.
- **Alertas Informativos (Informational):** Relacionados a comportamento padrão de cabeçalhos do servidor de desenvolvimento.

---

## 3. Análise e Justificativa dos Findings
A ausência total de alertas nas severidades **Alta** e **Média** valida a robustez das barreiras de segurança integradas ao longo da Fase 1 (T1) do projeto:

1. **Proteção contra Injeção (SQL Injection):** O uso estrito do ORM SQLModel associado a parâmetros tipados impediu qualquer comportamento anómalo detectado pelo ZAP nas entradas de dados.
2. **Mitigação de BOLA (Broken Object Level Authorization):** O endpoint de consulta de histórico de predição (`/predict/{log_id}`) valida explicitamente se o recurso pertence ao utilizador autenticado (`log.user_id == current_user.id`), retornando `404 Not Found` caso contrário. A varredura não encontrou rotas desprotegidas de nível de objeto.
3. **Controle de Abuso (Rate Limiting):** A aplicação implementa um limitador de requisições baseado no IP na rota sensível de login (`/auth/token`), mitigando ataques de força bruta.
4. **Blindagem de Cabeçalhos (Security Headers):** O middleware configurado injeta ativamente os cabeçalhos essenciais exigidos pelo padrão OWASP (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`), o que neutralizou avisos comuns de falta de hardening estrutural.

---

## 4. Conclusão da Auditoria
A API HealthAssist encontra-se tecnicamente blindada contra as vulnerabilidades críticas avaliadas pelo OWASP ZAP. O sistema está auditado, com os testes automatizados integrados em pipeline de CI/CD (GitHub Actions), e formalmente **aprovado e pronto** para atuar como alvo seguro na fase de pentest do Trimestre 2.