# Pergunta de classificação — HealthAssist

## 1. Formulação

> Dado o texto livre de uma pergunta feita por um usuário em um contexto de atendimento de saúde, qual é a **intenção** associada a ela?

| Elemento | Definição |
| --- | --- |
| Entrada | `question` — texto em português (coluna do dataset AKCIT/MedPT) |
| Saída | `question_type` — uma entre 7 classes (classificação **multiclasse, rótulo único**) |
| Uso na API | `POST /predict/` devolverá a intenção prevista e a confiança do modelo |

## 2. Classes e distribuição no dataset

Total: **384.095** registros (`df.shape = (384095, 6)`). Fonte: `notebooks/tp_3_health_assist.ipynb`, Exercício 05.

| Classe (`question_type`) | Registros | % do total |
| --- | ---: | ---: |
| Tratamento | 142.143 | 37,01 |
| Diagnóstico | 130.206 | 33,90 |
| Epidemiologia | 45.511 | 11,85 |
| Estilo de vida saudável | 21.746 | 5,66 |
| Outros | 19.897 | 5,18 |
| Escolha de profissionais de saúde | 19.167 | 4,99 |
| Anatomia e fisiologia | 5.425 | 1,41 |

Consequências diretas:

- Desbalanceamento forte: a maior classe tem cerca de 26 vezes mais exemplos que a menor (142.143 / 5.425).
- Um classificador que sempre responde "Tratamento" já obtém **37,01% de acurácia**. Esse é o piso que qualquer modelo precisa superar e é a razão de a métrica principal ser o **F1 macro**, não a acurácia.

## 3. Por que aprendizado supervisionado (e não apenas abordagens estatísticas)

1. **Existem rótulos para o que se quer prever.** São 384.095 exemplos com `question_type` preenchido; prever um rótulo conhecido a partir de exemplos rotulados é, por definição, aprendizado supervisionado.
2. **A estatística inferencial feita até aqui responde perguntas sobre grupos, não sobre instâncias.** O teste de Mann–Whitney (TP3) mostrou que respostas de "Estilo de vida saudável" tendem a ser maiores que as de "Tratamento" (p < 0,05). Isso descreve diferença entre distribuições; não atribui classe a uma pergunta nova.
3. **Atributos numéricos de tamanho têm pouco poder explicativo neste dataset.** A regressão simples entre tamanho da pergunta e da resposta teve R² = 0,0136 e RMSE = 46,80 palavras. Nos boxplots, a mediana do tamanho das perguntas fica em torno de 15 a 40 palavras na maioria das categorias, ou seja, as classes se sobrepõem em tamanho. O sinal está no **conteúdo textual**, não no comprimento.
4. **O espaço de entrada é de alta dimensionalidade e esparso** (vocabulário de um texto coloquial em português, com 384 mil exemplos). Regras manuais para separar 7 classes não escalam; um modelo linear sobre TF-IDF aprende os pesos diretamente dos dados.
5. **O desbalanceamento exige tratamento próprio** (pesos de classe, F1 macro, recall por classe), algo que estatística descritiva ou testes de hipótese não resolvem.

A hipótese será verificada em vez de assumida. O T2 compara três coisas no mesmo protocolo: (a) baseline de classe majoritária; (b) regressão logística usando apenas atributos de tamanho; (c) TF-IDF + modelo linear. O supervisionado só se justifica se (c) superar (a) e (b) em F1 macro.

## 4. Cuidados com os dados

- **Mesma pergunta em várias linhas.** O `df.head()` mostra a mesma pergunta repetida com respostas diferentes. Por isso o split treino/teste é **agrupado por pergunta**; dividir por linha vazaria a mesma pergunta entre treino e teste e inflaria as métricas.
- **Qualidade dos rótulos não auditada:** `question_type` vem do dataset e não foi validado manualmente.
- **Dados de saúde (LGPD):** o texto enviado à API é armazenado em `prediction_logs.input_data`; definir retenção e minimização antes de produção.

## 5. Métricas de avaliação

| Métrica | Papel |
| --- | --- |
| F1 macro | métrica principal (trata as 7 classes com o mesmo peso) |
| Precisão, recall e F1 por classe | detectar se classes pequenas (ex.: Anatomia e fisiologia, 1,41%) estão sendo ignoradas |
| Matriz de confusão | identificar confusões sistemáticas (ex.: Diagnóstico × Tratamento) |
| Acurácia | apenas secundária, sempre ao lado do baseline de 37,01% |

## 6. Relação com a API

O `POST /predict/` atual é um *stub*: devolve sempre `"Urgência Moderada"` com confiança `0.95`, sem modelo. As categorias de urgência não existem no dataset; as classes válidas são as sete acima. A troca do stub pelo classificador, e do campo `triage_category` por `intent`, faz parte do T2 (`docs/planejamento_t2.md`).