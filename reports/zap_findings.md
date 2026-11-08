# Relatório de Auditoria de Segurança — OWASP ZAP

## 1. Escopo e método

- Ferramenta: OWASP ZAP 2.17.0 (Docker), orquestrado por `scripts/run_zap_scan.py`.
- Alvo: `http://host.docker.internal:8000` (API HealthAssist).
- Execução: **Spider + Passive Scan**. O *Active Scan* não foi executado e a varredura não usou token JWT.
- Relatório bruto: `reports/zap_report.html` (gerado em 27/09/2026).

## 2. Resultado

| Severidade | Alertas |
| --- | ---: |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Informational | 1 |

Único alerta: **Authentication Request Identified** (informativo), em `/auth/token`. Ele apenas indica que o ZAP reconheceu o fluxo de login; não é vulnerabilidade.

Não havia findings Medium/High, portanto não houve o que corrigir. O resultado vale para o que foi exercitado, e deve ser lido com os limites abaixo.

## 3. Limites desta evidência

- O ZAP enxergou 4 endpoints e 83% das respostas foram 4xx. Sem token, os endpoints protegidos respondem 401 (coberto em `tests/test_authentication.py`), então o ZAP não alcançou a lógica autenticada.
- Sem Active Scan, o relatório **não** comprova ausência de injeção ou de falhas de autorização. Essas garantias vêm dos testes automatizados (`tests/`), não do ZAP.
- O código mudou depois desta varredura (rate limit em `/predict/`, schemas de resposta no OpenAPI). A varredura precisa ser repetida.

## 4. Controles e onde são verificados

| Controle | Implementação | Verificação |
| --- | --- | --- |
| Autenticação JWT | `app/security/jwt.py` | `tests/test_authentication.py` |
| BOLA | `app/routers/predict.py` (`log.user_id != current_user.id` → 404) | `tests/test_bola.py` |
| Validação de entrada | `app/schemas/predict.py` (`extra="forbid"`, limites de idade e tamanho) | `tests/test_input_validation.py` |
| Rate limiting | `/auth/token` 5/min, `/predict/` 30/min | `tests/test_rate_limit.py` |
| Headers de segurança | `app/middleware/security_headers.py` | `tests/test_security_headers_and_docs.py` |

## 5. Próximo passo

Repetir o ZAP com a especificação OpenAPI importada, Active Scan e token válido, e atualizar este relatório e `reports/security_checklist.md` com o novo resultado.