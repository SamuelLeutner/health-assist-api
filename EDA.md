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
- question_word_count - Contagem de palavras na pergunta.

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

![[Pasted image 20260927094650.png|413]]

#### 3.2. Tamanho das Perguntas
O histograma de quantidade de palavras mostrou que a maior parte das perguntas utiliza menos de 100 palavras, com maior concentração em perguntas relativamente curtas, apesar disso, existem casos mais extensos, indicando que o sistema não pode assumir que todas as entradas serão pequenas.

![[Pasted image 20260927094746.png|566]]

Isso é relevante para a aplicação porque indica que a entrada típica do chatbot provavelmente será curta, porém o sistema deve permanecer preparado para relatos maiores e mais detalhados.
#### 3.3. Tamanho das Respostas
As respostas apresentam comportamento semelhante, porém com maior dispersão, a maior parte das respostas possui tamanho relativamente reduzido, enquanto alguns casos ultrapassam várias centenas de palavras.

![[Pasted image 20260927094929.png|571]]

Isso demonstra uma maior diversidade no nível de detalhamento das respostas fornecidas pelos profissionais.
#### 3.4. Distribuição por Tipo de Questão
Os boxplots reforçam os padrões encontrados nos histogramas, na maior parte das categorias, as perguntas apresentam medianas relativamente baixas, enquanto existem diversos valores extremos.

Nas respostas, as medianas também permanecem relativamente próximas entre as categorias, porém existe uma quantidade significativa de outliers.

![[Pasted image 20260927095143.png|533]]

![[Pasted image 20260927095154.png|548]]

Algumas categorias, como **Estilo de vida saudável** e **Outros**, aparentaram apresentar respostas mais extensas, levantando a hipótese de que determinados tipos de questão possam exigir explicações mais detalhadas.
#### 3.5. Relação entre Tamanho da Pergunta e da Resposta
O scatterplot foi utilizado para observar a relação entre, question_word_count x answer_word_count

![[Pasted image 20260927095344.png|585]]

![[Pasted image 20260927100328.png]]

Baseado na visualização do gráfico é possível concluir que não necessariamente uma pergunta maior vair ter uma resposta mais complexa e extensa, com diversas perguntas relativamente pequenas recebendo respostas grandes.
#### 3.6. Correlações
O heatmap de correlação foi utilizado para analisar as associações entre as variáveis numéricas e variáveis categóricas transformadas para representação numérica.

![[Pasted image 20260927095723.png]]

![[Pasted image 20260927095738.png]]

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
<hr>

### 4. Insights Principais
1. **Tratamento e Diagnóstico concentram grande parte das perguntas**, indicando que os usuários tendem a procurar a plataforma quando já possuem alguma necessidade de saúde percebida.
2. **As perguntas são predominantemente curtas**, o que sugere que o modelo de classificação deverá lidar principalmente com entradas objetivas, embora também existam relatos longos.
3. **As respostas apresentam maior variação de tamanho**, mostrando que o nível de detalhamento fornecido pelos profissionais depende bastante do contexto da pergunta.
4. **O tipo da pergunta parece influenciar parcialmente o comportamento das respostas**, porém não explica sozinho sua extensão, indicando que outras variáveis também podem ser relevantes.
5. **O teste de Mann-Whitney reforçou a diferença observada entre determinadas categorias**, mostrando que o tipo de intenção pode estar relacionado ao tamanho das respostas.
<hr>

### 5. Limitações
A análise apresenta algumas limitações. O dataset representa interações realizadas em uma plataforma específica e, portanto, o comportamento observado não necessariamente representa todos os usuários de sistemas de saúde ou de chatbots médicos, além disso, a quantidade de palavras foi utilizada como medida de tamanho das mensagens, mas essa variável não representa diretamente a qualidade, complexidade ou relevância clínica do conteúdo.

Algumas variáveis, como especialidade médica e condição, possuem grande quantidade de categorias, o que dificulta determinadas análises estatísticas diretas.

A presença de outliers e distribuições assimétricas também exige cuidado na interpretação de médias e correlações.

Por fim, associação estatística não implica relação causal. Por exemplo, uma determinada categoria apresentar respostas maiores não significa necessariamente que o tipo da pergunta seja a causa dessa diferença.
<hr>

### 6. Próximos Passos:
A análise exploratória mostra que question_type pode ser utilizada como variável alvo para a próxima etapa do projeto, na qual será desenvolvido um modelo de classificação capaz de identificar automaticamente a intenção de uma nova pergunta.

O modelo receberia a questão do usuário, a `question`, com o alvo em `question_type`

Antes do treinamento, será necessário realizar o pré-processamento dos textos, incluindo normalização, avaliação de valores ausentes e definição da estratégia de representação textual.

Também será importante verificar o desbalanceamento das classes, já que categorias como Tratamento e Diagnóstico aparecem com frequência muito superior a outras categorias.

Em seguida, os dados poderão ser separados em conjuntos de treino e teste para comparar modelos de classificação e avaliar métricas como precisão, recall, F1-score e matriz de confusão.

Essa etapa permitirá transformar os padrões identificados durante a EDA em um componente funcional da HealthAssist, capaz de receber uma pergunta em linguagem natural e estimar a intenção do usuário antes das próximas etapas da triagem.