# Diagrama de Classes de Projeto

```mermaid
classDiagram
    class Pericia {
        +CharField nome (choices)
        +BooleanField requer_treino
        +__str__()
    }

    class Atributo {
        +CharField nome (choices)
        +IntegerField ordem
        +__str__()
    }

    class PericiaTreinada {
        +ForeignKey ficha
        +ForeignKey pericia
        +ManyToManyField atributo_chave
        +BooleanField treinado
        +IntegerField bonus_adicional
        +verificarTreino()
        +calcularValor()
        +adicionarBonus()
        +__str__()
    }

    class AtributoFicha {
        +ForeignKey atributo
        +ForeignKey ficha
        +IntegerField valor
        +__str__()
    }

    class Ataque {
        +CharField nome
        +TextField descricao
        +CharField dano
        +CharField tipo_dano (choices)
        +ForeignKey pericia
        +CharField resistencia
        +BooleanField homebrew
        +__str__()
    }

    class Classe {
        +CharField nome
        +TextField descricao
        +TextField proficiencia
        +IntegerField vida_base
        +IntegerField vida_por_nivel
        +IntegerField mana_base
        +IntegerField mana_por_nivel
        +TextField pericias_treinadas
        +TextField pericias_para_escolher
        +BooleanField homebrew
        +__str__()
    }

    class NivelClasseFicha {
        +ForeignKey classe
        +ForeignKey ficha
        +IntegerField nivel
        +__str__()
    }

    class Origem {
        +CharField nome
        +TextField descricao
        +BooleanField homebrew
        +__str__()
    }

    class Raca {
        +CharField nome
        +TextField descricao
        +BooleanField homebrew
        +__str__()
    }

    class Habilidade {
        +CharField nome
        +TextField descricao
        +CharField origem (choices)
        +BooleanField ativo
        +IntegerField nivel_habilidade
        +ForeignKey raca_pers
        +ForeignKey origem_pers
        +ForeignKey classe_pers
        +ForeignKey divindade_pers
        +BooleanField homebrew
        +__str__()
    }

    class Divindade {
        +CharField nome
        +TextField descricao
        +CharField simbolo
        +TextField obrigacoes
        +TextField restrições
        +BooleanField homebrew
        +__str__()
    }

    class Ficha {
        +ForeignKey dono
        +CharField nome
        +IntegerField nivel
        +CharField cd
        +CharField ca
        +IntegerField vida_atual
        +IntegerField mana_atual
        +IntegerField exp
        +CharField deslocamento
        +CharField tamanho
        +ForeignKey divindade
        +ManyToManyField atributos
        +ManyToManyField habilidades
        +ManyToManyField racas
        +ManyToManyField origens
        +ManyToManyField classes
        +ManyToManyField ataques
        +ManyToManyField pericias
        +calcularVida()
        +calcularMana()
        +setarNivel()
        +subirUmNivel()
        +calcular_todas_pericias()
        +__str__()
    }

    class MonstroPericia {
        +ForeignKey monstro
        +ForeignKey pericia
        +ManyToManyField atributo_chave
        +__str__()
    }

    class AtributoMonstro {
        +ForeignKey atributo
        +ForeignKey monstro
        +IntegerField valor
        +__str__()
    }

    class Monstro {
        +ForeignKey dono
        +CharField nome
        +IntegerField nivel
        +IntegerField nd
        +CharField cd
        +CharField ca
        +IntegerField vida
        +IntegerField mana
        +CharField deslocamento
        +CharField tamanho
        +ManyToManyField atributos
        +ManyToManyField habilidades
        +ManyToManyField ataques
        +ManyToManyField pericias
        +calcular_todas_pericias()
        +__str__()
    }

    class Mesa {
        +ForeignKey dono
        +ManyToManyField participante
        +CharField nome
        +TextField descricao
        +DateTimeField data_criacao
        +__str__()
    }

    class MesaParticipante {
        +ForeignKey mesa
        +ForeignKey jogador
        +CharField tipo (choices)
        +DateTimeField data_entrada
        +DateTimeField data_saida
        +IntegerField iniciativa
        +ForeignKey ficha
        +__str__()
    }

    class MesaCombate {
        +ForeignKey mesa
        +IntegerField turno_atual
        +ManyToManyField monstros
        +__str__()
    }

    class User {
        <<Django Model>>
    }

    User "1" *--> "*" Ficha
    User "1" *--> "*" Monstro
    User "1" *--> "*" Mesa
    PericiaTreinada "1" -- "0..*" AtributoFicha
    Atributo "1" -- "0..*" AtributoFicha
    Pericia "1" -- "0..*" PericiaTreinada 
    Ficha "1" -- "0..*" PericiaTreinada 
    Ficha "1" -- "0..*" AtributoFicha 
    Ficha "1" -- "0..*" Habilidade 
    Ficha "1" -- "0..*" Ataque 
    Ficha "1" -- "0..*" Raca 
    Ficha "1" -- "0..*" Origem 
    Classe "1" -- "0..*" NivelClasseFicha 
    Ficha "1" -- "0..*" NivelClasseFicha 
    Raca "1" -- "0..*" Habilidade 
    Origem "1" -- "0..*" Habilidade 
    Classe "1" -- "0..*" Habilidade
    Divindade "1" -- "0..*" Habilidade
    Divindade "1" -- "0..*" Ficha
    MonstroPericia "1" -- "0..*" AtributoMonstro
    Atributo "1" -- "0..*" AtributoMonstro
    Monstro "1" -- "0..*" MonstroPericia
    Monstro "1" -- "0..*" AtributoMonstro
    Monstro "1" -- "0..*" Habilidade
    Monstro "1" -- "0..*" Ataque
    Mesa "1" -- "0..*" MesaParticipante
    User "1" -- "0..*" MesaParticipante
    Ficha "1" -- "0..*" MesaParticipante
    Mesa "1" -- "0..1" MesaCombate
    Monstro "0..*" -- "0..1" MesaCombate
```

## Glossário

|  Termo            |  Explicação                                        |
| ----------------- | -------------------------------------------------- |
| **Ficha**          | Representa o conjunto de informações de um personagem, como nome, nível, atributos, classe, origem, raça, ataques, perícias, etc.  |
| **Classe**         | Define a classe do personagem, determinando suas características como vida base, mana, e o quanto esses atributos aumentam com o nível. |
| **Origem**         | Representa a origem do personagem, como seu passado ou linhagem, que pode influenciar suas habilidades e poderes. |
| **Raça**           | Define a espécie ou grupo étnico do personagem, com características e habilidades próprias. |
| **Atributo**       | Características que determinam a força, agilidade, inteligência e outros aspectos do personagem. |
| **AtributoFicha**  | Relaciona os atributos ao personagem, armazenando o valor de cada atributo específico na ficha do personagem. |
| **Perícia**        | Habilidade ou competência específica que o personagem pode ter, como usar armas, alquimia, etc. |
| **PeríciaTreinada**| Indica se o personagem treinou ou não uma determinada perícia, afetando o valor de sua habilidade nessa área. |
| **Ataque**         | Define os ataques do personagem, incluindo seu nome, dano e tipo de dano. |
| **User**           | Representa o usuário no sistema, que pode criar e gerenciar as fichas dos personagens. |

