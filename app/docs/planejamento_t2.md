# Planejamento T2 — Classificador de intenções e integração na API

## 1. Escopo

Treinar um classificador de intenção (`question` → `question_type`, 7 classes) e integrá-lo ao `POST /predict/`, preservando as proteções já existentes (JWT, BOLA, rate limiting, validação, headers). Definição do problema, classes e distribuição: `docs/pergunta_de_classificacao.md`.

## 2. Protocolo experimental

| Decisão | Escolha | Motivo |
| --- | --- | --- |
| Alvo | `question_type` (7 classes) | rótulo presente no dataset |
| Split | 80/20 **agrupado por texto da pergunta** | a mesma pergunta aparece em várias linhas; split por linha vaza dados |
| Validação | `StratifiedGroupKFold` (k = 5) sobre o treino | preserva a proporção das classes sem separar perguntas iguais |
| Teste | conjunto separado, usado uma única vez ao final | evita escolher modelo olhando o teste |
| Métrica principal | F1 macro | classes de 1,41% a 37,01% |

## 3. Engenharia de atributos

Entrada única: o texto de `question`.

- `TfidfVectorizer` em um `Pipeline` junto com o classificador (o vetorizador é ajustado só nos dados de treino de cada *fold*, sem vazamento).
- Configuração inicial, a ser ajustada por busca em grade: `ngram_range=(1, 2)`, `min_df=5`, `sublinear_tf=True`, `strip_accents="unicode"` (usuários costumam digitar sem acento).
- Variação a testar: n-gramas de caracteres (`analyzer="char_wb"`, 3–5) para robustez a erros de digitação.
- Stopwords **não** serão removidas na primeira rodada: palavras interrogativas ("como", "o que", "qual") tendem a carregar a intenção. A remoção entra como ablação e só é adotada se melhorar o F1 macro.

## 4. Modelos candidatos

| Modelo | Papel | Justificativa técnica |
| --- | --- | --- |
| `DummyClassifier(most_frequent)` | baseline 1 | piso de 37,01% de acurácia |
| Regressão logística só com atributos de tamanho | baseline 2 | testa se o comprimento já separa as classes (o EDA indica que não) |
| **Regressão logística multinomial** (TF-IDF, `class_weight="balanced"`) | candidato principal | gera probabilidades por classe (necessárias para `confidence` e limiares), é rápida em atributos esparsos e seus coeficientes são auditáveis |
| `LinearSVC` (TF-IDF, `class_weight="balanced"`) | candidato alternativo | forte em texto de alta dimensionalidade; sem probabilidade nativa, usa `CalibratedClassifierCV` |
| `ComplementNB` | baseline rápido opcional | desenhado para texto com classes desbalanceadas |

Critério de escolha: maior F1 macro na validação agrupada; em caso de empate, preferir o modelo com probabilidades nativas e menor latência. Modelos baseados em *transformers* ficam fora do T2 (custo de treino e de inferência incompatível com o escopo) e são trabalho futuro.

## 5. Critérios de aceite

- F1 macro do modelo escolhido superior ao dos dois baselines.
- Recall por classe reportado, com atenção explícita a "Anatomia e fisiologia".
- Matriz de confusão e análise dos erros mais frequentes no relatório.

## 6. Integração na API

- Serializar o `Pipeline` completo (TF-IDF + modelo) com `joblib` e carregá-lo **uma vez**, na inicialização da aplicação.
- Carregar apenas artefatos gerados pelo próprio projeto, com *hash* conferido na carga (desserializar `joblib`/`pickle` executa código).
- Contrato: `PredictResponse` passa a expor `intent` (uma das 7 classes) e `confidence` (probabilidade real); o valor fixo `0.95` e a categoria `"Urgência Moderada"` saem.
- Limitar o tamanho da entrada em `PredictRequest` (hoje só existe `min_length`); o EDA mostra textos de até centenas de palavras, então o limite precisa ser definido com base nos dados.
- Manter o rate limiting (`30/minute`) e os testes de BOLA; adicionar testes do contrato de predição e de entrada acima do limite.

## 7. Segurança ofensiva (TP4 / TP5)


| Campo | Valor |
| --- | --- |
| Colega adversário | Arthur e Sandy |
| URL/IP da API alvo | [URL ou IP da API do colega] |
| Escopo e janela autorizados | [definir] |
| Minha API (alvo do colega) | [URL ou IP onde ela ficará disponível] |

Estado da minha API como alvo: ver `reports/security_checklist.md`.