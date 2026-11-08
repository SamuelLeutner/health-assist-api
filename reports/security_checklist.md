# Checklist final de segurança — HealthAssist API

Legenda: `[x]` verificado com evidência · `[ ]` pendente.

## Controles da aplicação

- [x] Autenticação JWT com expiração; token ausente, malformado, expirado, assinado com outra chave, sem assinatura e de usuário inexistente → 401 (`tests/test_authentication.py`)
- [x] Senhas armazenadas com hash bcrypt
- [x] `SECRET_KEY` com no mínimo 32 caracteres, validada na inicialização; `.env` fora do Git (`.gitignore`)
- [x] BOLA: log de outro usuário → 404, indistinguível de log inexistente (`tests/test_bola.py`)
- [x] Validação estrita: campos extras, tipos e limites rejeitados com 422 (`tests/test_input_validation.py`)
- [x] Rate limiting: `/auth/token` 5/min e `/predict/` 30/min → 429 (`tests/test_rate_limit.py`)
- [x] Headers: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`, `Referrer-Policy` (`tests/test_security_headers_and_docs.py`)
- [x] OpenAPI em `/docs` e `/openapi.json` com schema de entrada e de saída para os 4 endpoints (`tests/test_security_headers_and_docs.py`)
- [ ] Limite máximo de tamanho para `symptoms_description` (hoje só há mínimo): definir no T2 com base nos dados

## OWASP ZAP

- [x] Findings High: 0 · Medium: 0 (relatório de 27/09/2026, Spider + Passive Scan; ver `reports/zap_findings.md`)
- [ ] Nova varredura com OpenAPI importada, Active Scan e token JWT, após as mudanças de código
- [ ] Resultado da nova varredura registrado aqui (High/Medium = 0, ou findings corrigidos e revalidados)

## Integração contínua

- [x] Workflow `.github/workflows/security-tests.yml` roda `python -m pytest tests/ -v` em push e pull request para `main`/`master`
- [x] Link da execução bem-sucedida no GitHub Actions: https://github.com/SamuelLeutner/health-assist-api/actions/runs/42507608567/job/128813540637

## Pentest cruzado

- [ ] Colega adversário e URL/IP da API alvo registrados em `docs/planejamento_t2.md` (seção 7)