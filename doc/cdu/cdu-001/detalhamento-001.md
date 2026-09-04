# CDU001. Criar Ficha de Personagem
- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário faz a sua ficha de personagem.
- **Pré-condição**: Estar logado
- **Pós-Condição**: A ficha é criada e salva na conta do jogador.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Entra na tela de personagem. | 2 - Mostra a tela de  Personagem. |  
| 3 - Clica na opção de "Criar personagem". | 4 - Mostra a tela de escolha de Nome, Divindade, Raça, Classe, Origem, e Atributos. | 
| 5 - Preenche Nome e Atributos e escolhe dentre as opções oferecidas Divindade, Raça, Classe e Origem. | 6 - Mostra a tela de ficha preenchida com as pericias, vida e mana já devidamente calculadas. |

## Fluxo Alternativo I - Usuário não logado.
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 3.1 - Clica na opção de "Criar personagem". | 4.1 - Mostra a mensagem de erro, informando que é necessário estar logado para criar uma ficha.|
| 5.1 - Decide logar para continuar o processo de criação de ficha. | 6.1 - Redireciona para o caso de uso de logar usuário. | 

## Diagrama de Sequência

```mermaid
sequenceDiagram
    actor Usuário
    participant CriarFichaView

    Usuário->>+CriarFichaView: 1: CriarFichaView(request):httpResponse
    CriarFichaView->>Usuário: "editar/criar_ficha.html"

    Usuário->>CriarFichaView: 2: CriarFichaView(request):httpResponse
    create participant Ficha
    CriarFichaView->>+Ficha: 2.1: <<create>> Ficha.objects.create(nome=nome, nivel=nivel, divindade=divindade)

    loop 
        create participant AtributoFicha
        CriarFichaView->>+AtributoFicha: 2.3: <<create>> AtributoFicha.objects.create(ficha=ficha, atributo=atributo, valor=int(valor))
        AtributoFicha->>+Atributo: 2.3.1: Associa o atributo correspondente (for atributo in Atributo.objects.all())
        Atributo-->>-AtributoFicha: 2.3.2: Salva o relacionamento (save())
        AtributoFicha-->>-CriarFichaView: 2.4: save()
    end

    loop
        create participant PericiaTreinada
        CriarFichaView->>+PericiaTreinada: 2.5: <<create>> PericiaTreinada.objects.create(ficha=ficha, pericia=pericia, treinado=False)
        PericiaTreinada->>Pericia: 2.5.1: for pericia in Pericia.objects.all()
        Pericia ->> PericiaTreinada: 2.5.2: save()
        PericiaTreinada->>+AtributoFicha: 2.5.3: atributo_ch = AtributoFicha.objects.get(ficha=ficha, atributo__nome=atributo_nome)
        AtributoFicha-->>-PericiaTreinada: 2.5.4: Devolve atributo associado
        PericiaTreinada-->>-CriarFichaView: 2.6: pericia_treinada.atributo_chave.set([atributo_ch])
        CriarFichaView->>+Ficha: 2.7: Ficha.PericiaTreinada.calcularValor()
        Ficha-->>-CriarFichaView: 2.8: Retorna valores calculados 
    end

    CriarFichaView->>+Ataque: 2.9: Ataque.objects.get_or_create(nome="Ataque desarmado", defaults={"dano": "1d4","pericia": pericia_luta,"tipo_dano": "imp"})
    Ataque-->>-CriarFichaView: 2.10: ficha.ataques.set([ataque_desarmado])

    CriarFichaView->>+Habilidade: 2.11: habilidades_classe = Habilidade.objects.filter(classe_pers=classe, origem='cl', nivel_habilidade=1)
    Habilidade-->>-CriarFichaView: 2.12: for habilidade in habilidades_classe: ficha.habilidades.add(habilidade)

    CriarFichaView->>+Habilidade: 2.11: habilidades_origem = Habilidade.objects.filter(origem_pers=origem, origem='or')
    Habilidade-->>-CriarFichaView: 2.12: for habilidade in habilidades_origem: ficha.habilidades.add(habilidade)

    CriarFichaView->>+Habilidade: 2.11: habilidades_raca = Habilidade.objects.filter(raca_pers=raca, origem='rc')
    Habilidade-->>-CriarFichaView: 2.12: for habilidade in habilidades_raca: ficha.habilidades.add(habilidade)

    CriarFichaView->>Ficha: 2.13: ficha.vida_max = ficha.calcularVida()
    Ficha-->>CriarFichaView: 2.14: Retorna valores calculados
    CriarFichaView->>Ficha: 2.15: ficha.mana_max = ficha.calcularMana()
    Ficha-->>CriarFichaView: 2.16: Retorna valores calculados

    Ficha-->>-CriarFichaView: 2.17: ficha.save()
    CriarFichaView->>-Usuário: 2.18: redirect("personagens")
```

## Diagrama de Comunicação

```mermaid
sequenceDiagram
    actor Usuário
    participant CriarFichaView

    Usuário->>+CriarFichaView: 1: Acessa a tela de criação de ficha (GET /criar_ficha/)
    Note over CriarFichaView: O usuário solicita a tela de criação de ficha.
    CriarFichaView->>Usuário: 2: Renderiza a tela de criação de ficha ("editar/criar_ficha.html")
    Note over Usuário: O usuário vê o formulário de criação de ficha.

    Usuário->>CriarFichaView: 3: Envia o formulário de criação de ficha (POST /criar_ficha/)
    Note over CriarFichaView: O usuário envia os dados da ficha.
    create participant Ficha
    CriarFichaView->>+Ficha: 3.1: Cria uma nova ficha (Ficha.objects.create(nome=nome, nivel=nivel, divindade=divindade))
    Ficha-->>CriarFichaView: 3.2: Retorna a ficha criada

    loop Para cada atributo
        create participant AtributoFicha
        CriarFichaView->>+AtributoFicha: 3.3: Cria um atributo para a ficha (AtributoFicha.objects.create(ficha=ficha, atributo=atributo, valor=int(valor)))
        AtributoFicha->>+Atributo: 3.3.1: Associa o atributo correspondente (for atributo in Atributo.objects.all())
        Atributo-->>-AtributoFicha: 3.3.2: Salva o relacionamento (save())
        AtributoFicha-->>-CriarFichaView: 3.4: Salva o atributo (save())
    end

    loop Para cada perícia
        create participant PericiaTreinada
        CriarFichaView->>+PericiaTreinada: 3.5: Cria uma perícia treinada (PericiaTreinada.objects.create(ficha=ficha, pericia=pericia, treinado=False))
        PericiaTreinada->>+Pericia: 3.5.1: Associa a perícia correspondente (Pericia.objects.all())
        Pericia-->>-PericiaTreinada: 3.5.2: Salva a perícia treinada (save())
        PericiaTreinada->>+AtributoFicha: 3.5.3: Associa o atributo chave (AtributoFicha.objects.get(ficha=ficha, atributo__nome=atributo_nome))
        AtributoFicha-->>-PericiaTreinada: 3.5.4: Devolve atributo associado
        PericiaTreinada-->>-CriarFichaView: 3.6: Define o atributo chave (pericia_treinada.atributo_chave.set([atributo_ch]))
        CriarFichaView->>+Ficha: 3.7: Calcula o valor da perícia (Ficha.PericiaTreinada.calcularValor())
        Ficha-->>-CriarFichaView: 3.8: Retorna o valor calculado
    end

    CriarFichaView->>+Ataque: 3.9: Cria ou obtém o ataque desarmado (Ataque.objects.get_or_create(nome="Ataque desarmado", defaults={"dano": "1d4","pericia": pericia_luta,"tipo_dano": "imp"}))
    Ataque-->>-CriarFichaView: 3.10: Associa o ataque à ficha (ficha.ataques.set([ataque_desarmado]))

    CriarFichaView->>+Habilidade: 3.11: Filtra habilidades da classe (Habilidade.objects.filter(classe_pers=classe, origem='cl', nivel_habilidade=1))
    Habilidade-->>-CriarFichaView: 3.12: Associa habilidades da classe à ficha (ficha.habilidades.add(habilidade))

    CriarFichaView->>+Habilidade: 3.13: Filtra habilidades da origem (Habilidade.objects.filter(origem_pers=origem, origem='or'))
    Habilidade-->>-CriarFichaView: 3.14: Associa habilidades da origem à ficha (ficha.habilidades.add(habilidade))

    CriarFichaView->>+Habilidade: 3.15: Filtra habilidades da raça (Habilidade.objects.filter(raca_pers=raca, origem='rc'))
    Habilidade-->>-CriarFichaView: 3.16: Associa habilidades da raça à ficha (ficha.habilidades.add(habilidade))

    CriarFichaView->>+Ficha: 3.17: Calcula a vida máxima da ficha (ficha.vida_max = ficha.calcularVida())
    Ficha-->>-CriarFichaView: 3.18: Retorna o valor calculado
    CriarFichaView->>+Ficha: 3.19: Calcula a mana máxima da ficha (ficha.mana_max = ficha.calcularMana())
    Ficha-->>-CriarFichaView: 3.20: Retorna o valor calculado

    Ficha-->>-CriarFichaView: 3.21: Salva a ficha (ficha.save())
    CriarFichaView->>-Usuário: 4: Redireciona para a tela de personagens (redirect("personagens"))
    Note over Usuário: O usuário é redirecionado para a lista de personagens.
```

## Diagrama de Classes de Projeto

```mermaid
classDiagram
    class CriarFichaView {
        +get()
        +post()
    }

    namespace django.contrib.auth{
        class User {
            <<Django Model>>
        }
    }

    class Ficha {
        +id: Integer
        +nome: CharField
        +nivel: Integer
        +calcularVida()
        +calcularMana()
    }

    class Classe {
        +id: Integer
        +nome: CharField
        +vida_base: Integer
        +vida_por_nivel: Integer
        +mana_base =  Integer
        +mana_por_nivel: Integer
    }

    class Origem {
        +id: Integer
        +nome: CharField
    }

    class Raca {
        +id: Integer
        +nome: CharField
    }

    class Atributo{
        + id: Interger
        + nome: CharField
        + ordem: Interger
    }

    class AtributoFicha{
        + id: Interger
        + valor: Interger

    }

    class Pericia{
        + id: Interger
        + nome: CharField
        + requer_treino: Boolean
    }

    class PericiaTreinada{
        + id: Interger
        + treinado: Boolean
        + calcularValor()
        + verificarTreino()
    }

    class Ataque {
        +id: Integer
        +nome: CharField
        +dano: CharField
        +tipo_dano: CharField
        +Ataque.objects.getbo(nome="Ataque desarmado")
    }

    User "1" *--> "*"  CriarFichaView 
    CriarFichaView "1" * --> "1" Ficha 
    Ficha "*" o--> "*" Classe 
    Ficha "1" o--> "*" Origem 
    Ficha "*" o--> "*" Raca 
    Ficha "*" o--> "*" Ataque
    Ficha "1" *--> "*" AtributoFicha
    AtributoFicha "*" *--> "1" Atributo
    Ficha "1" *--> "*" PericiaTreinada
    PericiaTreinada "*" *--> "1" Pericia
    PericiaTreinada "*" *--> "1" AtributoFicha
```
