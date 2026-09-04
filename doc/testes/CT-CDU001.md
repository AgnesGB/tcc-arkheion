# Caso de Teste - CDU001. Criar Ficha de Personagem

- **Resumo**: O usuário faz a sua ficha de personagem.

## Histórico da Alteração

|    Data    | Versão | Descrição                    | Autor(es)      |
| :--------: | ------ | ---------------------------- | -------------- |
| 04/11/2024 | 1.0    | Versão inicial do documento. | Agnes Barbosa. |

## Testes Funcionais

### Fluxo Principal

| Nome    | Homebrew | Divindade | Raça                | Origem  | Classe   | Atributos         | Resultado Esperado                                         | Resultado Obtido                   | Situação |
| ------- | -------- | --------- | ------------------- | ------- | -------- | ----------------- | ---------------------------------------------------------- | ---------------------------------- | -------- |
| Hadriel | False    | Azgher    | Suraggel            | Eremita | Paladino | 3, 2, 4, 0, 1, 4  | Ficha criada                                               | Ficha criada com sucesso           | Aprovado |
| -       | False    | Azgher    | Suraggel            | Eremita | Paladino | 3, 2, 4, 0, 1, 4  | Erro ao criar a ficha, preencha o nome do personagem       | Campo nome é obrigatório           | Aprovado |
| Hadriel | False    | Azgher    | Suraggel            | Eremita | Paladino | -2, 2, 4, 0, 1, 4 | Erro ao criar a ficha, atributo não pode ser menor que -2. | Sistema aceita valores válidos     | Aprovado |
| Hadriel | True     | Azgher    | Tiefling (Homebrew) | Eremita | Paladino | 3, 2, 4, 0, 1, 4  | Ficha criada                                               | Ficha criada com homebrew          | Aprovado |
| Hadriel | True     | Azgher    | Suraggel            | Eremita | Paladino | 3, 2, 4, 0, 1, 4  | Ficha criada                                               | Ficha criada com sucesso           | Aprovado |
| Hadriel | False    | Azgher    | Suraggel            | Eremita | Paladino | 0, 0, 0, 0, 0, 0  | Ficha criada                                               | Ficha criada com atributos zerados | Aprovado |
| Hadriel | False    | Azgher    | Suraggel            | Eremita | Paladino | -, -, -, -, -, -  | Erro ao criar a ficha, preencha os atributos               | Validação de atributos funcionando | Aprovado |
