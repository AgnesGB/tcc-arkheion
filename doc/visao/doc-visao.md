# Documento de visão

## Histórico da revisão

| Data | Versão | Descrição | Autor(es) |
| :---: | :---- | :---- | :---- |
| 04/11/2024 | 1.0 | Versão inicial do documento. | Agnes Barbosa, Nathan Cavalcante, Wellington Coutinho e Wilson Aguiar. |
| 05/12/2024 | 1.1 | Edição de dados do 4º tópico, Descrição do Ambiente dos Usuário . | Agnes Barbosa. |
| 12/12/2024 | 1.2 | Ajustes de requisitos funcionais e não funcionais | Agnes Barbosa e Nathan Cavalcante |
| 23/04/2025 | 2.0 | Revisão do documento de visão e adaptação para o projeto de desenvolvimento de sistema distribuído | Agnes Barbosa, João Victor da Fonseca, Lucas Pinheiro, Nathan Cavalcante e Wilson Aguiar |

---

<br>

## 1\. Nome do projeto: <b>Arkheion</b>

<br>

## 2\. Descrição do problema

| Tópico | Descrição |
| :---: | :---- |
| **O problema** | Falta de opções de fichas online para o sistema de RPG Tormenta 20 que seja fácil, prático e intuitivo para novos jogadores. |
| **Afeta** | Jogadores de RPG de mesa. |
| **Cujo impacto é** | Evasão de novos jogadores por não entender alguma regra ou até mesmo não saber como preencher uma ficha física, além de dificultar o processo do jogo que muitas vezes é interrompido por informações perdidas da “campanha” ou pela demora de obter informações no livro guia. |
| **Uma boa solução seria** | Uma plataforma única de forma resumida, clara e de fácil acesso, permitindo que jogadores consigam gerenciar seus recursos da melhor forma possível. |

<br>

## 3\. Glossário

| Termo | Definição | Observação complementar |
| ----- | ----- | ----- |
| RPG | Jogo de interpretação de personagens em que os participantes criam narrativas colaborativas. | Sigla de *Role-Playing Game*. |
| Jogador | Participante que controla um personagem e interage com o mundo do jogo. | Também chamado de “player”. |
| Mestre de Jogo (Mestre) | Responsável por narrar a história, representar NPCs e arbitrar as regras. | Também chamado de *GM* (Game Master) ou narrador. |
| Mesa | Grupo de jogadores e mestre que se reúnem para jogar. | Pode também se referir ao local físico ou à mesa virtual. |
| Sessão | Um encontro de jogo com duração variável (horas ou mais). | Parte de uma aventura ou campanha. |
| Campanha | Série contínua de aventuras interligadas que contam uma grande história. | Pode durar meses ou anos. |
| Aventura | Um arco narrativo com início, meio e fim, podendo durar uma ou mais sessões. | Parte de uma campanha. |
| Personagem | Entidade fictícia do jogo, podendo ser PJ ou NPC. | Representa as ações dos jogadores ou do mestre. |
| Personagem Jogador (PJ) | Personagem controlado por um jogador. | Tem ficha própria e papel ativo na narrativa. |
| Personagem Não Jogável (NPC) | Personagem controlado pelo mestre. | Pode ser aliado, inimigo ou figurante. |
| Ficha de Personagem | Documento com todas as informações do personagem: atributos, perícias, equipamentos, etc. | Pode ser digital ou impressa. |
| Dado | Ferramenta usada para determinar aleatoriedade nas ações, geralmente com formatos como d4, d6, d8, d10, d12 e d20. | A notação “dX” indica o número de lados do dado. |
| Sistema de Jogo | Conjunto de regras e mecânicas que define como o RPG é jogado. | Exemplos: Tormenta20, D\&D, Pathfinder, etc. |

<br>

## 4\. Descrição dos usuários

| Nome | Descrição | Responsabilidades |
| :---: | :---- | :---- |
| Jogadores de RPG de mesa. | Utilizam o produto para organizar e gerenciar as fichas dos personagens de RPG de mesa | • Preencher e atualizar fichas de personagens. <br> • Consultar regras e informações do jogo. <br> • Coordenar ações durante as sessões de jogo.  |

<br>

## 5\. Descrição do ambiente dos usuários

O número de pessoas envolvidas na execução da tarefa varia normalmente entre 3 a 7 jogadores, incluindo o mestre do jogo. Esse número pode mudar dependendo do grupo. As sessões de jogo têm duração entre 2 e 6 horas, com ciclos de tarefas que variam conforme a complexidade das ações dos personagens e a narrativa conduzida pelo mestre.

Os jogadores costumam se reunir em ambientes internos, como salas de estar ou salas de jogos, e também online, utilizando plataformas de videoconferência (Meet, Discord). O espaço deve ser confortável e permitir fácil comunicação entre os participantes.

Atualmente, são usadas plataformas como Owlbear Rodeo, Roll20, Discord e Fantasy Grounds para jogos de RPG de forma online ou não, que oferecem ferramentas para gerenciar fichas de personagens, mapas e outros elementos essenciais. Outros aplicativos, como Fichas de Nimb e Tormenta 20, também são utilizados, mas não é necessário que a plataforma desenvolvida interaja diretamente com eles, sendo apenas adições para o estilo de jogo de casa "mesa".

O principal problema enfrentado pelos usuários é a ausência de uma plataforma que simplifique a criação de fichas de personagens e organize informações de forma acessível para mestres e jogadores. Atualmente, isso está sendo resolvido com o uso de plataformas únicas e integradas que permitam a criação e gestão de fichas de personagens e mesas de jogo. Para os mestres, essas ferramentas incluem funcionalidades como visualização e edição de fichas dos jogadores.

Portanto é necessário um sistema que facilite o acesso a informações sobre seus personagens, como magias, habilidades e poderes, ajudando-os a relembrar e utilizar recursos úteis durante a aventura.

<br>

## 6\. Alternativas concorrentes

1. Fichas de Nimb  
2. Tormenta20 (Aplicativo mobile)

<br>

## 7\. Visão geral do produto

O usuário precisará já ter um conhecimento prévio das regras presente no livro de regras de Tormenta 20, a edição mais atualizada(Jogo do Ano).

Por se tratar de um produto web, não é necessária a instalação. Os usuários apenas precisam acessar a plataforma por meio de um navegador compatível.

* **Desempenho**: deve fornecer uma experiência ágil.

* **Robustez**: deve ser capaz de lidar com interrupções de rede sem causar perda de dados.

* **Tolerância a Erros**: deve fornecer mensagens de erro claras e úteis para o usuário em casos de falhas.

* **Usabilidade**: A interface do usuário deve ser intuitiva e fácil de usar, com uma navegação simples entre as diferentes seções.

<br>

## 8\. Requisitos FUNCIONAIS

| Código | Nome | Descrição |
| :---: | :---: | :---- |
| **F01** | Autenticação | O usuário autentica-se no sistema. |
| **F02** | Gerenciamento de conta | O sistema deve permitir que novos usuários se cadastrem na plataforma, visualizem e editem suas informações, e excluam suas contas. |
| **F03** | Gerenciamento de ficha | O usuário será capaz de cria uma nova ficha do personagem contendo seus atributos. Também poderá editar, visualizar e excluir a ficha. |
| **F04** | Gerenciamento de mesa | O sistema deve permitir que o usuário crie uma nova mesa de jogo, definindo nome, participantes e configurações iniciais. Também poderá alterar as configurações e participantes existentes, ou ainda remover uma mesa e todos os dados associados. |
| **F05** | Informações relevantes | A ficha precisa conter todas as informações relevantes para o jogo em fácil acesso. |
| **F06** | Cálculos Automáticos | O sistema deve calcular automaticamente alguns atributos da ficha do personagem conforme ele os modifica temporária ou permanentemente |
| **F06.1** | Perícias | Com base nos atributos e modificadores, o sistema deve recalcular as perícias conforme o jogador faz alterações. |
| **F06.2** | Habilidades | Habilidades que dependem dos atributos ou modificadores também devem ser recalculadas automaticamente. |
| **F06.3** | CD de Magias | O sistema deve recalcular o CD de magias automaticamente com base nas alterações de habilidades e atributos do personagem. |
| **F06.4** | Classe de Armadura (CA) | A CA deve ser atualizada automaticamente quando o personagem modifica equipamentos, como armaduras. |
| **F06.5** | Equipamentos | Armas, armaduras, itens mágicos, etc. e os efeitos desses equipamentos devem alterar as características da ficha (ex: CA, resistência, modificadores de perícias). Sobrecarga, o sistema deve calcular e aplicar automaticamente as penalidades e condições relacionadas à sobrecarga devido ao equipamento, como penalidades em movimentação. Armadura Pesada deve identificar se o personagem está usando uma armadura pesada e aplicar automaticamente as penalidades relacionadas, como redução de deslocamento. |
| **F06.6** | Perícia treinada | Permitir ao usuário indicar que certa perícia recebeu treinamento, ajustando bônus adequado. |
| **F07** | Controle de Mana e Vida | O usuário poderá atualizar valores de pontos de mana e vida conforme uso ou restauração |
| **F08** | Mudança de nível | O usuário poderá incrementar o nível do seu(s) personagem(ns), atribuir pontos de atributo e desbloquear novas habilidades |
<!-- O RNF abaixo talvez se configure como RF:

| NF05 | Anotação de aventura | O jogador precisa ter um espaço para anotar informações relevantes para o andamento da aventura | Usabilidade | Desejável | -->

<br>

## 9\. Requisitos NÃO-FUNCIONAIS

| Código | Nome | Descrição | Categoria | Classificação |
| :---: | :---: | :---- | :---: | :---: |
| **NF01** | Controle de acesso | Só usuários autenticados podem ter acesso ao sistema | Segurança | Obrigatório |
| **NF02** | Tempo de resposta | A comunicação entre o servidor e o cliente não deve ultrapassar o tempo limite para a jogada, entorno de 300ms | Performance | Obrigatório |
| **NF03** | Interface responsiva | Layout deve adaptar-se corretamente a desktops, tablets e celulares | Usabilidade | Desejável |
| **NF04** | Clareza e navegabilidade | Organização visual clara em todas as telas do sistema, com fluxos de navegação intuitivos e feedback para o usuário | Usabilidade | Desejável |
| **NF05** | Tolerância a falhas | Em caso de perda de conexão, o sistema deve tentar reconectar e não perder dados em edição | Confiabilidade | Obrigatório |
| **NF06** | Disponibilidade | Sistema disponível no mínimo 99% do tempo, com janelas de manutenção agendadas | Operacional | Obrigatório |
| **NF07** | Escalabilidade | Arquitetura capaz de suportar aumento de carga conforme mais mesas e jogadores forem adicionados | Performance | Desejável |

<br>

## 10\. Lista de Riscos

| **Identificador** | **Título** | **Descrição do risco** | **Indicador** | **Gravidade** | **Estratégia de mitigação** | **Plano de contingência** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| R01 | Atraso no desenvolvimento | Desenvolvimento das funcionalidades principais não é concluído no prazo estimado. | Marcos não atingidos, features não implementadas na data prevista, burndown do sprint não cumprido. | Alta | Quebrar funcionalidades em tarefas menores, definir MVP claro, usar metodologias ágeis com sprints curtos. | Redefinir escopo priorizando funcionalidades core, realocação de recursos, extensão de prazos. |
| R02 | Problemas de integração entre frontend e backend | Dificuldades na comunicação entre as camadas da aplicação causando atrasos. | Falhas nos testes de integração, APIs não funcionando conforme esperado, inconsistência de dados. | Alta | Definir contratos de API claros desde o início, implementar testes automatizados de integração, comunicação constante entre equipes. | Revisão dos contratos de API, refatoração de endpoints, testes manuais intensivos. |
| R03 | Mudanças de requisitos durante desenvolvimento | Alterações nos requisitos funcionais impactando o cronograma de desenvolvimento. | Solicitações de mudanças frequentes, retrabalho em funcionalidades já implementadas. | Média | Documentação clara de requisitos, validação constante com stakeholders, processo formal de mudanças. | Congelar escopo temporariamente, avaliar impacto de mudanças, negociar prazos adicionais. |
| R04 | Dependências externas indisponíveis | Bibliotecas, APIs ou serviços externos necessários não estão disponíveis ou são descontinuados. | Bibliotecas não mantidas, APIs com instabilidade, documentação inadequada de terceiros. | Média | Pesquisar alternativas para dependências críticas, manter versões locais de bibliotecas essenciais. | Implementar soluções alternativas, desenvolver funcionalidades internas equivalentes. |
| R05 | Problemas de performance não identificados | Performance inadequada só descoberta em fases tardias do desenvolvimento. | Testes de carga falhando, lentidão reportada em ambiente de homologação, tempo de resposta acima do esperado. | Média | Implementar testes de performance desde o início, monitoramento contínuo, otimização preventiva. | Refatoração de código crítico, otimização de consultas de banco, implementação de cache. |
| R06 | Complexidade do domínio subestimada | A complexidade das regras de negócio de RPG é maior que o inicialmente estimado. | Dificuldade em implementar cálculos automáticos, regras conflitantes, casos edge não previstos. | Alta | Estudo aprofundado das regras do Tormenta 20, consulta com especialistas do domínio, prototipagem de funcionalidades complexas. | Simplificação de regras, implementação incremental de funcionalidades, consultoria externa. |
| R07 | Problemas de compatibilidade entre tecnologias | Incompatibilidade entre versões de frameworks ou tecnologias escolhidas. | Erros de build, conflitos de dependências, funcionalidades não funcionando em conjunto. | Média | Validação prévia de compatibilidade, uso de versões estáveis, documentação de versões utilizadas. | Downgrade/upgrade de versões, refatoração para tecnologias compatíveis. |
| R08 | Dificuldade em testes de sistema distribuído | Testar a comunicação e sincronização entre componentes distribuídos é complexo. | Bugs descobertos apenas em produção, falhas intermitentes em ambiente de desenvolvimento. | Média | Configurar ambientes de teste que simulem a distribuição, testes automatizados de integração, uso de containers. | Intensificar testes manuais, implementar logs detalhados, ferramentas de debugging distribuído. |
| R09 | Escassez de conhecimento técnico especializado | Falta de expertise em tecnologias específicas necessárias para o projeto. | Implementações incorretas, código de baixa qualidade, soluções sub-ótimas. | Média | Capacitação da equipe, mentoria, estudo prévio das tecnologias, documentação técnica detalhada. | Buscar consultoria externa, realocação de tarefas, simplificação de soluções técnicas. |
| R10 | Sobrecarga da equipe de desenvolvimento | Burnout da equipe devido a prazos apertados ou excesso de trabalho. | Queda na produtividade, aumento de bugs, turnover de membros da equipe. | Alta | Distribuição equilibrada de tarefas, definição realista de prazos, pausas regulares entre sprints. | Renegociação de prazos, contratação de recursos adicionais, redefinição de prioridades. |
| R11 | Mudanças na arquitetura durante desenvolvimento | Necessidade de refatorar a arquitetura em fases avançadas do projeto. | Retrabalho extensivo, atraso significativo, código legado difícil de manter. | Alta | Prototipagem da arquitetura, validação early com POCs, revisões arquiteturais periódicas. | Refatoração incremental, manutenção de duas versões temporariamente, extensão de cronograma. |
| R12 | Indisponibilidade de material base oficial | Perda de acesso aos livros e regras oficiais do Tormenta 20 durante desenvolvimento. | Impossibilidade de consultar regras, interrupção no desenvolvimento de funcionalidades específicas. | Média | Adquirir múltiplas cópias físicas e digitais, criar documentação interna resumida das regras essenciais. | Usar versões de backup, consultar comunidade RPG, desenvolvimento baseado em conhecimento prévio da equipe. |
| R13 | Mudanças no material base oficial | Lançamento de erratas, atualizações ou novas edições que alteram regras já implementadas. | Funcionalidades desatualizadas, cálculos incorretos, usuários reportando inconsistências com regras atuais. | Alta | Monitoramento constante de atualizações oficiais, sistema flexível para mudanças de regras, versionamento de regras no sistema. | Implementação rápida de patches, comunicação aos usuários sobre mudanças, manutenção de versões antigas como opção. |
| R14 | Atualização de regras durante desenvolvimento | Mudanças nas regras oficiais do Tormenta 20 que impactam funcionalidades em desenvolvimento. | Retrabalho em cálculos automáticos, invalidação de funcionalidades prontas, conflitos entre versões de regras. | Média | Definir versão base das regras para desenvolvimento, sistema modular para adaptação de regras. | Congelar versão das regras temporariamente, planejar migração gradual, manter compatibilidade com versões anteriores. |
| R15 | Interpretação incorreta de regras complexas | Má compreensão ou implementação errada de regras específicas do Tormenta 20. | Cálculos automáticos incorretos, funcionalidades que não refletem as regras reais, reclamações de usuários experientes. | Alta | Consultoria com especialistas em Tormenta 20, testes com jogadores experientes, validação constante com material oficial. | Correção rápida de implementações, criação de sistema de override para regras especiais, documentação clara das interpretações adotadas. |
| R16 | Falta de feedback dos usuários finais | Desenvolvimento de funcionalidades que não atendem às necessidades reais dos usuários RPG. | Baixa adoção do produto, funcionalidades não utilizadas, interface não intuitiva para jogadores. | Média | Testes de usabilidade com jogadores de RPG, protótipos interativos, envolvimento de mesas de RPG na validação. | Ciclos rápidos de feedback pós-lançamento, programa beta com grupos de RPG, ajustes baseados em analytics de uso. |
| R17 | Problemas de direitos autorais | Uso inadequado de conteúdo protegido por direitos autorais do Tormenta 20. | Processos legais, necessidade de remover funcionalidades, impedimento de lançamento. | Alta | Consulta jurídica prévia, uso apenas de regras públicas, criação de conteúdo próprio quando necessário. | Remoção imediata de conteúdo problemático, negociação de licenças, redesign de funcionalidades conflitantes. |
| R18 | Problemas de versionamento e deploy | Dificuldades na implantação e controle de versões entre diferentes ambientes. | Deploy falhou, inconsistências entre ambientes, rollback problemático. | Média | CI/CD bem configurado, ambiente de staging similar à produção, testes automatizados de deploy. | Deploy manual supervisionado, rollback automático, hotfixes direcionados. |