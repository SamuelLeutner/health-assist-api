Observação: para a elaboração das seções textuais deste relatório EDA, utilizei o modelo ChatGPT, desenvolvido pela OpenAI.

A ferramenta foi alimentada com o contexto do conjunto de dados, as hipóteses validadas e os outputs estatísticos obtidos nas etapas anteriores, fiz uso do modelo na estruturação e refinamento da escrita acadêmica, seguindo as categorias solicitadas na Questão 7.

### 1. Problema:
O projeto HealthAssist tem como objetivo desenvolver uma API com suporte de inteligência artificial para auxiliar na triagem inicial de usuários a partir de perguntas e relatos relacionados à saúde.

Antes da construção de um modelo de classificação, é necessário compreender como os usuários formulam suas perguntas, quais tipos de intenção aparecem com maior frequência e como os profissionais respondem a essas solicitações.

As principais questões investigadas foram:
- Quais são os tipos de pergunta mais frequentes?
- Qual é o tamanho típico das perguntas e respostas?
- Existem diferenças no tamanho das mensagens entre diferentes tipos de questão?
- Perguntas maiores tendem a receber respostas maiores?
- Determinadas categorias apresentam respostas mais extensas que outras?
- Até que ponto o tamanho das perguntas influencia no tamanho das respostas?
- Como o problema de identificação da intenção pode ser formulado como classificação?

<hr>

### 2. Dados Usados
Foi utilizado o dataset AKCIT/MedPT composto de perguntas e respostas de usuários e profissionais da área de saúde, extraido da plataforma Doctoralia.

As principais variáveis utilizadas na elaboração do projeto foram:

- id;
- question - Perguntas dos usuários;
- answer - Respostas dos profissionais;
- condition - Problema de saúde relacionado a pergunta;
- medical_specialty - Especialidade do profissional;
- question_type - Tipo da Questão.

Fora as variáveis originais, foram criadas também:

- answer_word_count - Contagem de palavras na resposta;
- question_word_count - Contagem de palavras na pergunta;
- contagem_especialidades - Quantidade de especialidades associadas ao registro;
- especialidade_principal - Especialidade utilizada para agrupar os registros durante a análise entre especialidade e tipo de questão.

#### 2.1. Análise do Data Frame:
======== Valores Nulos ========
id                   0
question             0
answer               0
condition            0
medical_specialty    0
question_type        0
======== Valores Nulos ========

======== Valores Duplicados ========
0
======== Valores Duplicados ========

======== Categorias ========
question_type
Tratamento                           142143
Diagnóstico                          130206
Epidemiologia                         45511
Estilo de vida saudável               21746
Outros                                19897
Escolha de profissionais de saúde     19167
Anatomia e fisiologia                  5425
Name: count, dtype: int64
======== Categorias ========

======== Describe ========
count         384095
unique             7
top       Tratamento
freq          142143
Name: question_type, dtype: object
======== Describe ========
<hr>

### 3. Análise
#### 3.1. Distribuição de Questão por Tipo
O gráfico de barras mostrou que as categorias **Tratamento** e **Diagnóstico** apresentam frequência consideravelmente superior às demais, esse resultado sugere uma tendência dos usuários a procurar a plataforma quando já possuem algum sintoma ou problema de saúde e desejam compreender o que pode estar acontecendo ou conhecer possíveis formas de tratamento.

Categorias relacionadas à prevenção e estilo de vida aparecem com menor frequência, indicando que a maior parte das interações possui caráter mais voltado à resolução de problemas já percebidos.

![[questao-por-tipo.png]]

#### 3.2. Tamanho das Perguntas
O histograma de quantidade de palavras mostrou que a maior parte das perguntas utiliza menos de 100 palavras, com maior concentração em perguntas relativamente curtas, apesar disso, existem casos mais extensos, indicando que o sistema não pode assumir que todas as entradas serão pequenas.

![[tamanho-das-perguntas.png]]

Isso é relevante para a aplicação porque indica que a entrada típica do chatbot provavelmente será curta, porém o sistema deve permanecer preparado para relatos maiores e mais detalhados.
#### 3.3. Tamanho das Respostas
As respostas apresentam comportamento semelhante, porém com maior dispersão, a maior parte das respostas possui tamanho relativamente reduzido, enquanto alguns casos ultrapassam várias centenas de palavras.

![[tamanho-das-respostas.png]]

Isso demonstra uma maior diversidade no nível de detalhamento das respostas fornecidas pelos profissionais.
#### 3.4. Distribuição por Tipo de Questão
Os boxplots reforçam os padrões encontrados nos histogramas, na maior parte das categorias, as perguntas apresentam medianas relativamente baixas, enquanto existem diversos valores extremos.

Nas respostas, as medianas também permanecem relativamente próximas entre as categorias, porém existe uma quantidade significativa de outliers.

![[boxplot-resposta-por-tipo-questao.png]]

![[boxplot-questao-por-tipo-questao.png]]

Algumas categorias, como **Estilo de vida saudável** e **Outros**, aparentaram apresentar respostas mais extensas, levantando a hipótese de que determinados tipos de questão possam exigir explicações mais detalhadas.
#### 3.5. Relação entre Tamanho da Pergunta e da Resposta
O scatterplot foi utilizado para observar a relação entre, question_word_count x answer_word_count

![[scatter-PerguntaxResposta.png]]

![[scatter-PerguntaxResposta-TipodeQuestao.png]]

Baseado na visualização do gráfico é possível concluir que não necessariamente uma pergunta maior vai ter uma resposta mais extensa, com diversas perguntas relativamente pequenas recebendo respostas grandes.
#### 3.6. Correlações
O heatmap de correlação foi utilizado para analisar as associações entre as variáveis numéricas e variáveis categóricas transformadas para representação numérica.

![[sns-heatmap-correlacao-variaveis.png]]

![[sns-heatmap-especialidade-questiontype.png]]

Analisando o heatmap acima, é possível ver com um pouco mais de clareza a correlação entre o tamanho da resposta e os tipos de questões, e parece que assim como tinhamos visto, existe uma correlação, apesar de pequena entre a quantia de palavras nas respostas e o tipo da pergunta, visto que nas categorias outro e estilo de vida saudável como tinhamos levantado aparece uma correlação maior.
#### 3.7. Teste de Hipótese
Baseado na análise feita desde o tp-1 até o presente momento e observando os scatterplots e os heatmaps gerados, decidi dar continuidade na hipotese levantada no tp-1 que é:

h0 - As respostas da categoria de estilo de vida saudavel não tendem a ser maiores que as respostas da categoria de Tratamento

h1 - As respostas da categoria de estilo de vida saudavel tendem a ser maiores que as respostas da categoria de Tratamento

Como existem muitos outliers e respostas que podem ir de 20 palavras até 600 palavras decidi usar mann-whitney U ao invés de t-test.

=================================
Mediana de Estilo de vida saudável: 48.0
Mediana de Tratamento: 41.0

U: 1715493161.5
P valor: 3.6006338519089664e-151
\=================================

O teste com Mann-Whitney apresentou um p-valor inferior a 0,05, encontramos então evidencias estatísticas de que as respostas ligadas a Estilo de vida saudável são maiores que as respostas da categoria Tratamento, ou seja, existem categorias cujas respostas são mais complexas.

![[prova-scipy.png]]

![[prova-mannwhitneyu.png]]
#### 3.8. Regressão Linear

Como etapa anterior ao desenvolvimento do modelo de classificação, foi implementado um modelo de regressão linear para analisar se o tamanho da pergunta realizada pelo usuário possui relação suficiente para estimar o tamanho da resposta fornecida pelo profissional.

Foram utilizadas duas variáveis numéricas derivadas dos textos: `question_word_count`, representando a quantidade de palavras presentes na pergunta, e `answer_word_count`, representando a quantidade de palavras presentes na resposta.

A variável `question_word_count` foi utilizada como variável independente e `answer_word_count` como variável alvo. Os dados foram separados entre conjuntos de treinamento e teste, utilizando 80% dos registros para treinamento e 20% para avaliação.

O modelo foi avaliado utilizando as métricas R² e RMSE.

**R²:** 0.0136

**RMSE:** 46.7981

O valor de R² indica que aproximadamente 1,3% da variação existente no tamanho das respostas pode ser explicada apenas pelo tamanho das perguntas. Já o RMSE indica que as previsões realizadas pelo modelo apresentam um erro típico de aproximadamente 46,8 palavras.

![[print-r2.png]]
Para analisar o comportamento dos erros do modelo, foi utilizado um gráfico de resíduos. Em uma regressão linear adequada, é esperado que esses resíduos estejam distribuídos de maneira relativamente aleatória ao redor de zero.

![[residual-plot.png]]

Baseado no formato do gráfico, parece que existe um formato de funil perto dos menores pontos, que implica que os resíduos possuem uma dispersão maior e para valores previstos maiores a dispersão diminui, ou seja a variação dos erros não é constante e vai contra uma das hipóteses clássicas da regressão linear. 

Também foi elaborado um Q-Q Plot para verificar visualmente o comportamento da distribuição dos resíduos.

![[qq-plot.png]]

O gráfico apresentou uma distribuição anormal dos resíduos, com uma clara tendencia a valores acima do esperado nas extremidades. Os valores negativos ultrapassam o previsto mas se mantém perto da linha já nas extremidades com valores maiores, eles ultrapassam a previsão de maneira extrema. Essa análise dos gráficos mostra que existe um limite claro no uso do modelo visto que a previsão tem um erro considerável.

A regressão apresenta algumas limitações importantes. O tamanho da pergunta representa apenas uma característica da interação e não considera aspectos como o tipo da questão, a condição médica, a especialidade do profissional ou a complexidade do conteúdo.

Além disso, como observado anteriormente nos histogramas e boxplots, existem diversos outliers e uma grande variação no tamanho das respostas, incluindo respostas de várias centenas de palavras. Dessa forma, perguntas com tamanhos semelhantes podem receber respostas bastante diferentes.

A regressão linear deve, portanto, ser interpretada como uma análise exploratória da relação entre duas variáveis numéricas derivadas do texto e não como o modelo principal da HealthAssist.

<hr>

### 4. Insights Principais
1. **Tratamento e Diagnóstico concentram grande parte das perguntas**, indicando que os usuários tendem a procurar a plataforma quando já possuem alguma necessidade de saúde percebida.
2. **As perguntas são predominantemente curtas**, o que sugere que o modelo de classificação deverá lidar principalmente com entradas objetivas, embora também existam relatos longos.
3. **As respostas apresentam maior variação de tamanho**, mostrando que o nível de detalhamento fornecido pelos profissionais depende bastante do contexto da pergunta.
4. **O tipo da pergunta parece influenciar parcialmente o comportamento das respostas**, porém não explica sozinho sua extensão, indicando que outras variáveis também podem ser relevantes.
5. **O teste de Mann-Whitney reforçou a diferença observada entre determinadas categorias**, mostrando que o tipo de intenção pode estar relacionado ao tamanho das respostas.
6. **6. O tamanho da pergunta possui capacidade limitada para prever o tamanho da resposta**, reforçando que características adicionais do conteúdo precisam ser consideradas para representar adequadamente as interações.
<hr>

### 5. Limitações
A análise apresenta algumas limitações. O dataset representa interações realizadas em uma plataforma específica e, portanto, o comportamento observado não necessariamente representa todos os usuários de sistemas de saúde ou de chatbots médicos, além disso, a quantidade de palavras foi utilizada como medida de tamanho das mensagens, mas essa variável não representa diretamente a qualidade, complexidade ou relevância clínica do conteúdo.

Algumas variáveis, como especialidade médica e condição, possuem grande quantidade de categorias, o que dificulta determinadas análises estatísticas diretas.

A presença de outliers e distribuições assimétricas também exige cuidado na interpretação de médias e correlações.

A regressão linear também possui capacidade limitada neste contexto, pois utiliza apenas o tamanho da pergunta para estimar o tamanho da resposta. Diversos fatores não representados pelo modelo podem influenciar essa variável, como a intenção da pergunta, condição apresentada, especialidade médica e nível de detalhamento escolhido pelo profissional.

Por fim, associação estatística não implica relação causal. Por exemplo, uma determinada categoria apresentar respostas maiores não significa necessariamente que o tipo da pergunta seja a causa dessa diferença.
<hr>

### 6. Problema de Classificação e Próximos Passos

Após a análise exploratória e a etapa de regressão, o problema principal da aplicação pode ser formalizado como uma tarefa de classificação:

**Dado o texto de uma pergunta realizada por um usuário em um contexto de atendimento de saúde, qual é a intenção associada a essa pergunta?**

A variável `question`, contendo o texto escrito pelo usuário, será utilizada como entrada do modelo, enquanto `question_type` será utilizada como variável alvo.

Dessa forma:

`question → modelo de classificação → question_type`

Como a variável `question_type` possui sete categorias possíveis, trata-se de um problema de **classificação multiclasse**.

As classes existentes no dataset são:

- Tratamento;
    
- Diagnóstico;
    
- Epidemiologia;
    
- Estilo de vida saudável;
    
- Outros;
    
- Escolha de profissionais de saúde;
    
- Anatomia e fisiologia.
    

A distribuição dessas classes já demonstrou um desbalanceamento considerável durante a análise exploratória. Tratamento e Diagnóstico possuem bem mais dados enquanto categorias como Anatomia e fisiologia possuem quantidade significativamente inferior.

Esse comportamento será importante durante o treinamento e avaliação do classificador, já que um modelo pode apresentar uma acurácia aparentemente elevada ao favorecer as classes com maior quantidade de exemplos. Por esse motivo, além da acurácia, deverão ser observadas métricas como precision, recall, F1-score e matriz de confusão.

A regressão linear utilizada na etapa anterior não é adequada para o problema principal da aplicação porque sua finalidade é prever valores numéricos contínuos. No problema da HealthAssist, a saída esperada não é um valor numérico, mas uma das categorias existentes em `question_type`.

Transformar artificialmente essas categorias em números também não resolveria o problema, pois criaria relações de ordem e distância que não existem entre as intenções. Por exemplo, definir Diagnóstico como 1 e Tratamento como 2 não significa que Tratamento seja numericamente maior que Diagnóstico. Além disso, uma regressão poderia produzir valores intermediários que não corresponderiam a nenhuma classe válida.

Portanto, a próxima etapa do projeto será preparar os textos presentes em `question` para utilização em um modelo de classificação multiclasse, separar os dados entre conjuntos de treinamento e teste e comparar o desempenho dos modelos utilizando métricas adequadas para o desbalanceamento identificado.