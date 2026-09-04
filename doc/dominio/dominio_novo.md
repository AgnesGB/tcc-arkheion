# Modelo de Domínio

![Diagrama de classes de domínio](<20250430_Arkheion_Diagrama de Domínio.jpg>)

<br>

## Glossário

| Termo | Definição | Observação complementar |
| ----- | --------- | ------------------------ |
| **Alcance** | Distância máxima que um ataque ou efeito pode atingir. | Pode ser corpo a corpo, curto, médio, longo ou extremo. |
| **Alinhamento** | Orientação moral e ética do personagem (Leal, Neutro, Caótico; Bom, Neutro, Mau). | Influencia comportamento e algumas magias/habilidades. |
| **Arma (Divindade)** | A arma preferida de uma divindade, frequentemente associada a simbolismos ou usos sagrados. | Pode influenciar habilidades ou deveres religiosos. |
| **Ataque** | Define os ataques do personagem, incluindo seu nome, dano, tipo de dano e propriedades especiais. | Pode ser corpo a corpo, à distância ou mágico. |
| **Ativo/Passivo** | Algo é considerado "ativo" quando depende de uma escolha ou ação do jogador para ser utilizado; é "passivo" quando está sempre em efeito, sem exigir ação direta. | Aplica-se especialmente a habilidades e efeitos contínuos. |
| **Atributo** | Valor numérico que representa características essenciais de um personagem: Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma. | Esses atributos influenciam diversas ações e resultados no jogo. |
| **AtributoFicha** | Relaciona os atributos ao personagem, armazenando o valor de cada atributo específico na ficha do personagem. | Classe intermediária entre Atributo e Ficha no sistema. |
| **Aventura** | Um arco narrativo com início, meio e fim, podendo durar uma ou mais sessões. | Parte integrante de uma campanha. |
| **CA (Classe de Armadura)** | Valor que representa quão difícil é acertar um ataque no personagem. | Influenciada por armadura, destreza e outras modificações. |
| **Campanha** | Série contínua de aventuras interligadas que compõem uma grande narrativa. | Pode durar meses ou anos. |
| **CD (Classe de Dificuldade)** | Valor que os oponentes devem superar para resistir a magias ou habilidades especiais. | Calculado com base nos atributos e nível do personagem. |
| **Classe** | A "profissão" ou "função" do personagem no jogo, definindo habilidades, estilo de jogo, progressão, vida base e mana. | Ex.: guerreiro, mago, ladino, clérigo. |
| **Crítico** | Resultado excepcional em uma jogada de ataque, geralmente causando dano extra. | Normalmente ocorre quando se tira 20 no dado de ataque. |
| **Dado** | Ferramenta usada para determinar aleatoriedade nas ações. | Usualmente expressos em notações como d4, d6, d8, d10, d12 e d20. |
| **Dano** | Quantidade de ferimento ou prejuízo causado por um ataque ou efeito. | Pode ser de diferentes tipos: físico, elemental, mental, etc. |
| **Deslocamento** | Distância que um personagem pode se mover em uma rodada de combate. | Medido em metros ou quadrados no mapa. |
| **Deveres e Restrições** | Conjunto de dogmas, códigos ou limitações (geralmente religiosas) que um personagem segue. | Podem influenciar o comportamento e as escolhas do personagem. |
| **Divindade** | Entidade divina que pode ser venerada pelos personagens, oferecendo poderes e orientações espirituais. | Cada divindade possui domínios, símbolos e ensinamentos específicos. |
| **Domínio** | Área de influência ou especialização de uma divindade. | Ex.: Guerra, Vida, Conhecimento, Natureza. |
| **Equipamento** | Itens que o personagem possui, como armas, armaduras, ferramentas e objetos diversos. | Podem oferecer bônus ou penalidades às características. |
| **Experiência (XP)** | Pontos acumulados pelo personagem através de suas aventuras, usados para subir de nível. | Representa o crescimento e aprendizado do personagem. |
| **Ficha** | Documento com todas as informações relevantes sobre um personagem: atributos, perícias, equipamentos, histórico e habilidades. | Pode ser física (papel) ou digital. |
| **Graduação** | Nível de maestria em uma perícia ou habilidade. | Influencia bônus e capacidades especiais. |
| **Habilidade** | Poder especial ou capacidade única que um personagem possui, podendo ser ativa ou passiva. | Determinada pela classe, origem, raça ou divindade. |
| **Homebrew** | Conteúdo criado pelos jogadores ou mestre, não oficial do sistema. | Permite personalização e expansão das regras básicas. |
| **Iniciativa** | Valor que determina a ordem de ação dos personagens em combate. | Calculado com base na Destreza e modificadores. |
| **Jogador** | Participante que controla um personagem e interage com o mundo do jogo. | Também chamado de *player*. |
| **Magia** | Efeito sobrenatural ativado através de conjuração, componentes ou rituais. | Consome pontos de mana e possui diferentes escolas. |
| **Mana (PM - Pontos de Mana)** | Recurso usado para ativar magias e habilidades especiais. | Regenera com descanso ou itens específicos. |
| **Mesa** | Grupo de jogadores e mestre que se reúne para jogar uma sessão de RPG. | Pode se referir ao local físico ou à plataforma virtual usada. |
| **MesaCombate** | Sistema que gerencia o combate em uma mesa, controlando turnos e iniciativa. | Parte do sistema de mesas no Arkheion. |
| **MesaParticipante** | Relação entre um usuário e uma mesa, definindo seu papel (jogador, mestre, observador). | Inclui informações como data de entrada e personagem usado. |
| **Mestre de Jogo (Mestre)** | Pessoa responsável por narrar a história, interpretar personagens não jogáveis (NPCs) e aplicar as regras do sistema. | Também chamado de *GM* (Game Master) ou narrador. |
| **Modificador** | Bônus ou penalidade aplicado a jogadas de dados baseado nos atributos. | Calculado como (Atributo - 10) / 2, arredondado para baixo. |
| **Monstro** | Criatura controlada pelo mestre, geralmente hostil aos personagens jogadores. | Possui suas próprias estatísticas e habilidades. |
| **Multiclasse** | Sistema que permite ao personagem ter níveis em múltiplas classes. | Oferece versatilidade mas pode diluir especializações. |
| **ND (Nível de Dificuldade)** | Medida da dificuldade de um encontro ou monstro em relação ao nível dos personagens. | Usado para balancear combates e desafios. |
| **Nível** | Medida da experiência e poder de um personagem, determinando suas capacidades. | Aumenta conforme o personagem ganha experiência. |
| **NivelClasseFicha** | Relação que armazena quantos níveis um personagem possui em cada classe. | Permite multiclasse e controle de progressão. |
| **NPC (Personagem Não Jogável)** | Personagem controlado pelo mestre, podendo interagir com os jogadores de diversas formas. | Pode ser aliado, inimigo ou figurante. |
| **Origem** | Descreve a ocupação, os conhecimentos prévios e a formação cultural de um personagem antes de se tornar aventureiro. | Pode conceder habilidades e perícias específicas. |
| **Penalidade** | Redução temporária ou permanente em atributos, perícias ou outras características. | Causada por ferimentos, maldições ou condições adversas. |
| **Perícia** | Valor numérico que representa o grau de habilidade de um personagem em determinada área de conhecimento ou ação. | Ex.: acrobacia, furtividade, diplomacia, atletismo. |
| **PeríciaTreinada** | Indica se o personagem treinou uma determinada perícia, recebendo bônus adicional. | Afeta significativamente o valor final da perícia. |
| **Personagem** | Entidade fictícia representada no jogo, podendo ser controlada por um jogador (PJ) ou pelo mestre (NPC). | Representa as ações e decisões dentro da narrativa. |
| **Personagem Jogador (PJ)** | Personagem controlado por um jogador. | Tem ficha própria e participa ativamente da narrativa. |
| **Pontos de Vida (PV)** | Representam a resistência física e vitalidade do personagem. | Quando chegam a zero, o personagem pode morrer ou ficar inconsciente. |
| **Proficiência** | Conhecimento ou habilidade para usar determinados equipamentos ou realizar ações específicas. | Ex.: proficiência com armas leves, armaduras pesadas. |
| **Raça** | Determina a ascendência biológica do personagem, como humano, elfo, anão, etc. | Afeta atributos, habilidades e vantagens iniciais. |
| **Resistência** | Capacidade de reduzir ou anular danos de tipos específicos. | Pode ser natural da raça ou adquirida por equipamentos/magias. |
| **Rodada** | Período de tempo no combate durante o qual todos os participantes têm a chance de agir. | Normalmente dura cerca de 6 segundos no tempo do jogo. |
| **Rolagem** | Ato de jogar dados para determinar o resultado de uma ação. | Base fundamental das mecânicas de RPG. |
| **RPG** | Jogo de interpretação de personagens em que os participantes constroem narrativas colaborativas. | Sigla de *Role-Playing Game*. |
| **Sessão** | Encontro de jogo com duração variável (geralmente horas). | É uma parte da aventura ou campanha. |
| **Sistema de Jogo** | Conjunto de regras e mecânicas que define como o RPG é jogado. | Exemplos: Tormenta20, D&D, Pathfinder. |
| **Talento** | Habilidade especial adquirida conforme o personagem evolui. | Oferece novas capacidades ou melhora as existentes. |
| **Tamanho** | Categoria que define o espaço ocupado por uma criatura (Minúsculo, Pequeno, Médio, Grande, Enorme, Colossal). | Afeta alcance, combate e movimentação. |
| **Teste de Resistência** | Rolagem feita para resistir a efeitos nocivos como venenos, maldições ou magias. | Baseado nos atributos do personagem. |
| **Tormenta 20** | Sistema de RPG brasileiro, ambientado no mundo de Arton. | Sistema base usado pelo projeto Arkheion. |
| **Turno** | Período de tempo durante o qual um personagem pode realizar suas ações em combate. | Parte de uma rodada de combate. |
| **User** | Representa o usuário no sistema, que pode criar e gerenciar fichas de personagens e participar de mesas. | Classe base do sistema de autenticação. |
| **Versatilidade** | Capacidade de um item ou habilidade ter múltiplos usos ou efeitos. | Comum em armas e magias do Tormenta 20. |
