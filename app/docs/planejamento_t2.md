# Planejamento de Arquitetura e Transição para T2 (Frente de Engenharia e API)

## 1. Contexto e Preparação da API para o Trimestre 2 (T2)

Durante o Trimestre 1 (T1), o foco esteve concentrado na construção do arcabouço de engenharia de software da API, na blindagem de segurança (autenticação JWT, rate limiting, headers OWASP e mitigação de BOLA) e na automação de testes com CI/CD. No Trimestre 2 (T2), a API está estruturada para receber a integração com os modelos preditivos e a fase de segurança ofensiva (pentest cruzado).

### Definição do Problema no Escopo da API

* **Endpoint de Predição (`/predict/`):** Projetado para receber o texto descritivo de um atendimento ou sintoma inserido por um utilizador autenticado, processar a requisição com validação rigorosa de schemas e retornar a categoria de triagem correspondente.
* **Persistência de Logs:** Os resultados das predições continuam blindados por regras de autorização de nível de objeto (BOLA), garantindo que cada utilizador aceda estritamente aos seus próprios dados de histórico.

---

## 2. Diretrizes de Integração de Modelos e Features (Preparação da API)

Para garantir que a API suporte a transição dos dados textuais para os algoritmos preditivos que serão integrados no T2, a arquitetura foi preparada para absorver:

1. **Feature Engineering / Vetorização:** Utilização prevista de pipelines com **TF-IDF (Term Frequency-Inverse Document Frequency)** para conversão de texto em vetores numéricos compatíveis com os endpoints de inferência.
2. **Modelos Candidatos (Alvos de Integração na API):**
* **Regressão Logística (Logistic Regression):** Como modelo *baseline* leve e de alta eficiência para inferência rápida na API.
* **Support Vector Machine (SVM) com Kernel Linear:** Avaliado para lidar com a alta dimensionalidade gerada pelo processamento de linguagem natural (NLP).

---

## 3. Formalização das Classes de Triagem para os Schemas da API

Para manter a consistência dos contratos de dados (`Pydantic Schemas`) na API, as respostas de predição mapearão as entradas para as seguintes classes discretas:

* **Urgência Alta (Emergência):** Sintomas críticos que exigem atendimento imediato (ex: dor intensa no peito, falta de ar súbita, desmaios).
* **Urgência Moderada:** Sintomas que requerem avaliação médica breve, mas sem risco iminente de vida (ex: febre persistente há dias, dor de cabeça forte).
* **Pouco Urgente / Dúvida Geral:** Casos leves, orientações ou dúvidas gerais sobre saúde e medicação.

---

## 4. Segurança Ofensiva e Alvo de Pentest (TP4 / TP5)

Como parte integrante do planejamento técnico de transição para as próximas etapas:

* **Prontidão do Alvo:** A API encontra-se auditada, com o pipeline de CI/CD ativo no GitHub Actions e pronta para atuar como alvo seguro.
* **Colega Adversário Identificado:** Colega Adversário / Alvo de Pentest: A definir via sorteio oficial conduzido pelo professor (conforme orientação em aula), ficando a API do grupo pronta e parametrizada para receber a auditoria de qualquer equipe designada.