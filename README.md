# LABORATÓRIO DE EXPERIMENTAÇÃO DE SOFTWARE do curso de Engenharia de Software da PUC Minas <img align="center" alt="Victor-Python" height="40" width="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">

### Hi there ! 👋🏽

Neste repositorio apresentamos as principais características de sistemas populares open-source. Dessa forma, vamos analisar como eles são desenvolvidos, com que frequência recebem contribuição externa, com qual frequência lançam releases, entre outras características. Para tanto, foram coletados os dados indicados a seguir para os 1.000 repositórios com maior número de estrelas no GitHub.

Questões de Pesquisa: 

* RQ 01. Sistemas populares são maduros/antigos?
* RQ 02. Sistemas populares recebem muita contribuição externa?
* RQ 03. Sistemas populares lançam releases com frequência?
* RQ 04. Sistemas populares são atualizados com frequência?
* RQ 05. Sistemas populares são escritos nas linguagens mais populares (Links para um site externo.)?
* RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?

### Processo de Desenvolvimento

Para realização do desafio foi utilizando a metodologia agil com os seguintes backlog para sprints:

* SP 01. Consulta graphql para 100 repositórios (com todos os dados/métricas necessários para responder as RQs) + requisição automática
* SP 02. Paginação (consulta 1000 repositórios) + dados em arquivo .csv
* SP 03. Análise e visualização de dados + elaboração do relatório final

### Requisitos

* Para utilizar o codigo acima é necessário na variavel api_token substituir a string 'place_your_token_here' pelo seu token disponibilizado  pelo github. Ex:
 
      api_token = 'seu_token_do_github'

* Para utilização dos import utilizar o interpretador python 3.9.7 
