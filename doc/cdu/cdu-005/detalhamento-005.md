# CDU005. Alterar Mana ou Vida.

- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário usa uma ficha de personagem.
- **Pré-condição**: Estar logado; ter uma ficha já feita e editada.
- **Pós-Condição**: ---

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: |
| 1 - Entra na tela de personagem. | 2 - Exibe a tela de  Personagem. |  
| 3 - Clica na opção de vizualização de ficha de personagem. | 4 - Exibe a tela de ficha já devidamente preenchida. |
| 5 - Aperta na seta menor para alterar os pontos de mana/vida do personagem. | 6 - Altera, de um em um, a quantidade de mana/vida atual. |

## Fluxo Alternativo I - Botão maior.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: | 
| 5.1 - Aperta na seta maior para alterar os pontos de mana/vida do personagem. | 6.1 - Altera, de cinco em cinco, a quantidade de mana/vida atual. | 

## Fluxo Alternativo II - Alterar manualmente.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: | 
| 5.2 - Aperta em cima do número para alterar os pontos de mana/vida do personagem, e informa a quantidade de pontos que deseja soomar ou subtrair. | 6.2 - Altera, de acordo com a quantidade informada, a quantidade de mana/vida atual. | 

## Diagrama de Comunicação

![Diagrama de comunicação](cdu005-comunicação.png)

## Diagrama de Sequência

```mermaid
sequenceDiagram
    participant Usuario
    participant PersonagensView
    participant FichaCombateView
    participant Ficha
    participant AtualizarFichaView

    Usuario ->> PersonagensView: GET /personagens
    PersonagensView -->> Usuario: render('personagens.html')

    Usuario ->> FichaCombateView: GET /ficha_combate/{ficha_id}
    FichaCombateView ->> Ficha: Ficha.objects.get(pk=ficha_id)
    Ficha -->> FichaCombateView: Retorna ficha
    FichaCombateView -->> Usuario: render('ficha_combate.html')

    alt Fluxo Principal - Alteração unitária
        Usuario ->> AtualizarFichaView: POST /atualizar_ficha/{ficha_id} (delta=1)
        AtualizarFichaView ->> Ficha: get_object_or_404()
        Ficha -->> AtualizarFichaView: ficha
        AtualizarFichaView ->> Ficha: vida_atual += delta
        Ficha -->> AtualizarFichaView: save()
        AtualizarFichaView -->> Usuario: JsonResponse({status: "success", vida_atual: novo_valor})
    end

    alt Fluxo Alternativo I - Alteração múltipla
        Usuario ->> AtualizarFichaView: POST /atualizar_ficha/{ficha_id} (delta=5)
        AtualizarFichaView ->> Ficha: get_object_or_404()
        Ficha -->> AtualizarFichaView: ficha
        AtualizarFichaView ->> Ficha: vida_atual += delta
        Ficha -->> AtualizarFichaView: save()
        AtualizarFichaView -->> Usuario: JsonResponse({status: "success", vida_atual: novo_valor})
    end

    alt Fluxo Alternativo II - Alteração manual
        Usuario ->> AtualizarFichaView: POST /atualizar_ficha/{ficha_id} (valor_absoluto=X)
        AtualizarFichaView ->> Ficha: get_object_or_404()
        Ficha -->> AtualizarFichaView: ficha
        AtualizarFichaView ->> Ficha: vida_atual = X
        Ficha -->> AtualizarFichaView: save()
        AtualizarFichaView -->> Usuario: JsonResponse({status: "success", vida_atual: novo_valor})
    end
```

## Diagrama de Classes de Projeto

```mermaid
classDiagram
    class PersonagensView {
        +get(request, *args, **kwargs): HttpResponse
    }

    class FichaCombateView {
        +get(request, ficha_id, *args, **kwargs): HttpResponse
    }

    class AtualizarFichaView {
        +post(request, ficha_id, *args, **kwargs): JsonResponse
    }

    class Ficha {
        <<Django Model>>
        +id: Integer
        +nome: CharField
        +nivel: Integer
        +divindade: CharField
        +cd: CharField
        +ca: CharField
        +vida_atual: Integer
        +vida_max: Integer
        +mana_atual: Integer
        +mana_max: Integer
        +exp: Integer
        +deslocamento: CharField
        +tamanho: CharField
        +calcularVida(): Integer
        +calcularMana(): Integer
        +setarNivel(args): void
        +subirUmNivel(): void
        +calcular_todas_pericias(): dict
    }

    class User {
        <<Django Model>>
        +id: Integer
        +username: CharField
        +email: CharField
        +password: CharField
        +get_full_name(): str
        +get_short_name(): str
        +set_password(raw_password): void
        +check_password(raw_password): bool
    }

    User "1" *--> "*" PersonagensView
    User "1" *--> "*" FichaCombateView
    User "1" *--> "*" AtualizarFichaView
    
    PersonagensView "*" *--> "1" Ficha
    FichaCombateView "*" *--> "1" Ficha
    AtualizarFichaView "*" *--> "1" Ficha
```