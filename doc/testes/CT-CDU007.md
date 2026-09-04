# Caso de Teste - CDU007. Criar conta

- **Resumo**: O usuário cria uma conta no sistema para poder acessar as funcionalidades do Arkheion.

## Histórico da Alteração

|    Data    | Versão | Descrição                    | Autor(es)          |
| :--------: | ------ | ---------------------------- | ------------------ |
| 02/10/2025 | 1.0    | Versão inicial do documento. | Nathan Cavalcante. |

## Testes Funcionais

### Fluxo Principal

| Nome de Usuário   | Email               | Senha         | Confirmação Senha | Resultado Esperado                         | Resultado Obtido                | Situação |
| ----------------- | ------------------- | ------------- | ----------------- | ------------------------------------------ | ------------------------------- | -------- |
| usuario_teste     | usuario@teste.com   | MinhaSenh@123 | MinhaSenh@123     | Conta criada com sucesso                   | Conta criada, token retornado   | Aprovado |
| novo_usuario      | novo@email.com      | Senha@456     | Senha@456         | Conta criada via fluxo alternativo         | Conta criada com sucesso        | Aprovado |
| (vazio)           | teste@email.com     | Senha@789     | Senha@789         | Erro: "Este campo é obrigatório"           | Erro 400 - username obrigatório | Aprovado |
| usuario_valido    | (vazio)             | Senha@789     | Senha@789         | Erro: "Este campo é obrigatório"           | Erro 400 - email obrigatório    | Aprovado |
| usuario_teste     | email_invalido      | Senha@789     | Senha@789         | Erro: "Insira um endereço de email válido" | Erro 400 - email inválido       | Aprovado |
| usuario_teste     | teste@email.com     | 123           | 123               | Aviso de senha inválida                    | Erro 400 - senha muito curta    | Aprovado |
| usuario_teste     | teste@email.com     | MinhaSenh@123 | SenhasDiferentes  | Erro: "As senhas não coincidem"            | Erro 400 - senhas não coincidem | Aprovado |
| usuario_existente | novo@email.com      | Senha@789     | Senha@789         | Erro: "Um usuário com esse nome já existe" | Erro 400 - username duplicado   | Aprovado |
| novo_usuario      | email@existente.com | Senha@789     | Senha@789         | Erro: "Este email já está em uso"          | Erro 400 - email duplicado      | Aprovado |
| usuário@inválido  | teste@email.com     | Senha@789     | Senha@789         | Erro de validação de caracteres            | Erro 400 - caracteres inválidos | Aprovado |
| usuario_teste     | teste@email.com     | MinhaSenh@123 | MinhaSenh@123     | Conta criada após correção                 | Conta criada com sucesso        | Aprovado |
