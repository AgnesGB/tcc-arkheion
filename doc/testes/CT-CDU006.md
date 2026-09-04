# Caso de Teste - CDU006. Logar Usuário

- **Resumo**: O usuário insere suas credenciais para acessar sua conta no sistema Arkheion.
- **Pré-condição**: Usuário `teste_jv` com senha `SenhaValida123!` deve estar previamente cadastrado e ativo no sistema.

## Histórico da Alteração

|    Data    | Versão | Descrição                                             | Autor(es)                       |
| :--------: | :----- | :---------------------------------------------------- | :------------------------------ |
| 25/10/2025 | 1.0    | Versão inicial do documento, elaborada para o CDU006. | João Victor da fonseca Dionisio |

## Testes Funcionais

### Fluxo Principal e Fluxos Alternativos

| ID do Teste   | Cenário de Teste                               | Nome/Email (Entrada 1)                     | Senha (Entrada 2)                | Resultado Esperado                                                                                           | Resultado Obtido                 | Situação |
| :------------ | :--------------------------------------------- | :----------------------------------------- | :------------------------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------- | :------- |
| **CT-LOG-01** | **Sucesso - Fluxo Principal**                  | `teste_jv` (Usuário Válido)                | `SenhaValida123!` (Senha Válida) | Sucesso no login, carregamento da tela de perfil do usuário.                                                 | Login com sucesso, token gerado  | Aprovado |
| **CT-LOG-02** | **Sucesso - Login com Email**                  | `teste_jv@arkheion.com` (Email Válido)     | `SenhaValida123!`                | Sucesso no login, carregamento da tela de perfil do usuário.                                                 | Login com email funciona         | Aprovado |
| **CT-LOG-03** | **Limite Inferior (Vazio) - Usuário/Email**    | (Vazio)                                    | `SenhaValida123!`                | Erro de validação no formulário: "Este campo é obrigatório".                                                 | Erro 400 - campo obrigatório     | Aprovado |
| **CT-LOG-04** | **Limite Inferior (Vazio) - Senha**            | `teste_jv`                                 | (Vazio)                          | Erro de validação no formulário: "Este campo é obrigatório".                                                 | Erro 400 - campo obrigatório     | Aprovado |
| **CT-LOG-05** | **Conta Inexistente/Usuário Inválido (FA II)** | `usuario_nao_existe`                       | `SenhaValida123!`                | Aviso de "Usuário não cadastrado" ou "Nome de usuário ou senha inválidos".                                   | Erro 400 - credenciais inválidas | Aprovado |
| **CT-LOG-06** | **Conta Inexistente/Email Inválido (FA II)**   | `nao_existe@email.com`                     | `SenhaValida123!`                | Aviso de "Usuário não cadastrado" ou "Nome de usuário ou senha inválidos".                                   | Erro 400 - credenciais inválidas | Aprovado |
| **CT-LOG-07** | **Senha Incorreta (FA I)**                     | `teste_jv`                                 | `SenhaErrada123`                 | Aviso de "Senha incorreta. Tente novamente" ou "Nome de usuário ou senha inválidos".                         | Erro 400 - senha incorreta       | Aprovado |
| **CT-LOG-08** | **C. Limite Superior - Usuário**               | `A` x 150 (Tamanho Máximo Aceito)          | `SenhaValida123!`                | Sucesso no login (Assumindo que 150 é o limite do campo username).                                           | Login com sucesso no limite      | Aprovado |
| **CT-LOG-09** | **C. Limite Superior + 1 - Usuário**           | `A` x 151 (Acima do Limite)                | `SenhaValida123!`                | Erro de validação: "O nome de usuário excede o limite de caracteres".                                        | Erro 400 - limite excedido       | Aprovado |
| **CT-LOG-10** | **Caracteres Inválidos (Sanitização)**         | `teste_jv' OR 1=1;` (Tentativa de injeção) | `SenhaValida123!`                | Erro de autenticação. A view deve tratar a string como literal e falhar a busca.                             | SQL injection bloqueado          | Aprovado |
| **CT-LOG-11** | **Redirecionamento Pós-Login**                 | `teste_jv`                                 | `SenhaValida123!`                | Login bem-sucedido e redirecionamento para o URL anterior (se aplicável), ou para a página inicial (`home`). | Token retornado com sucesso      | Aprovado |
