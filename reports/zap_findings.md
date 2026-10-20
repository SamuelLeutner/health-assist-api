# OWASP ZAP Scan Findings

## Escopo da Varredura
Realizei a varredura de segurança automatizada utilizando o OWASP ZAP no backend da API HealthAssist. O escopo do teste incluiu todos os endpoints expostos, com foco principal nos fluxos de autenticação (`/auth/login`), predição (`/predict`) e verificações de integridade (`/health`).

## Resultados e Conclusões
Durante a análise dos relatórios gerados pelo ZAP (presentes em `reports/zap_report.html`), verifiquei que **não foram identificados alertas de severidade Alta (High) ou Média (Medium)**.

Os alertas de severidade Baixa (Low) ou Informativos encontrados referem-se a configurações padrão e comportamentos esperados do framework FastAPI e do servidor Uvicorn em ambiente de desenvolvimento. 

Como não foram identificadas vulnerabilidades críticas (Medium/High) referentes a BOLA, injeção, ou ausência de rate limiting (controles já implementados na camada de middleware da aplicação), justifico a inexistência de ações corretivas adicionais nesta etapa. A aplicação atende aos critérios da OWASP Top 10 estabelecidos para o escopo do projeto.