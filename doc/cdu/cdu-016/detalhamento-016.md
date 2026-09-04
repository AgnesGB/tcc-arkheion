# CDU016. Editar conta de usuário

- **Ator principal**: Usuário  
- **Atores secundários**: ---  
- **Resumo**: O usuário edita as informações da sua conta, como nome de usuário, email e senha.  
- **Pré-condição**: O usuário deve estar logado no sistema.  
- **Pós-condição**: As informações da conta são atualizadas.  

## Fluxo Principal  
| **Ações do Ator** | **Ações do Sistema** |  
|------------------|------------------|  
| 1 - O usuário acessa a página de perfil e seleciona "Editar Conta". | 2 - Exibe a tela de edição de conta. |  
| 3 - O usuário preenche os novos dados e confirma. | 4 - Valida os dados e salva as alterações. |  
| 5 - O sistema exibe uma mensagem de sucesso. | 6 - Redireciona para a tela de perfil com os dados atualizados. |  

## Fluxo Alternativo I - Senha incorreta  
| **Ações do Ator** | **Ações do Sistema** |  
|------------------|------------------|  
| 3.1 - O usuário insere uma senha atual incorreta. | 4.1 - O sistema exibe um erro informando que a senha está incorreta. |  
| 3.2 - O usuário tenta novamente. | 4.2 - Se a senha for correta, continua para o passo 5 do fluxo principal. |  

## Fluxo Alternativo II - Email ou Nome de Usuário já em uso  
| **Ações do Ator** | **Ações do Sistema** |  
|------------------|------------------|  
| 3.3 - O usuário insere um email ou nome de usuário já registrado no sistema. | 4.3 - O sistema exibe uma mensagem informando que o email/nome de usuário já está em uso. |  
| 3.4 - O usuário tenta novamente com novos dados. | 4.4 - Se os dados forem válidos, continua para o passo 5 do fluxo principal. |  

## Diagrama de Interação (Comunicação)

```mermaid

sequenceDiagram
    actor Usuário
    participant EditarUsuarioView
    participant FormularioEdicaoUsuario
    participant UserModel
    participant BancoDeDados

    Usuário->>EditarUsuarioView: Acessa a página de edição
    EditarUsuarioView->>Usuário: Exibe formulário preenchido

    Usuário->>EditarUsuarioView: Preenche e envia formulário (POST)
    EditarUsuarioView->>FormularioEdicaoUsuario: Valida dados
    FormularioEdicaoUsuario->>UserModel: Verifica senha atual

    alt Senha correta
        UserModel->>BancoDeDados: Atualiza dados do usuário
        BancoDeDados-->>UserModel: Confirmação de salvamento
        UserModel-->>EditarUsuarioView: Retorna sucesso
        EditarUsuarioView->>Usuário: Exibe mensagem de sucesso e redireciona
    else Senha incorreta
        EditarUsuarioView->>Usuário: Exibe erro: "Senha atual incorreta"
    end
```

## Diagrama de Interação (Sequência)

```mermaid

sequenceDiagram
  actor Usuário
  participant EditarUsuarioView as EditarUsuarioView
  participant FormularioEdicaoUsuario as FormularioEdicaoUsuario
  participant UserModel as UserModel
  participant BancoDeDados as BancoDeDados

  Usuário ->> EditarUsuarioView: GET /editar-perfil
  EditarUsuarioView ->> Usuário: Exibe formulário preenchido (render_template)

  Usuário ->> EditarUsuarioView: POST /editar-perfil (dados do formulário)
  EditarUsuarioView ->> FormularioEdicaoUsuario: valida_dados()
  FormularioEdicaoUsuario ->> UserModel: verificar_senha_atual()

  alt Senha correta
    UserModel ->> BancoDeDados: update_usuario()
    BancoDeDados -->> UserModel: Retorna sucesso
    UserModel -->> EditarUsuarioView: Retorna sucesso
    EditarUsuarioView ->> Usuário: Exibe mensagem de sucesso e redireciona (redirect)
  else Senha incorreta
    EditarUsuarioView ->> Usuário: Exibe erro "Senha atual incorreta"
  end

```

## Diagrama de Classes de Projeto

```mermaid

classDiagram
   class Usuario {
        +id: int
        +username: str
        +email: str
        +senha: str
        +editar_perfil(novo_username: str, novo_email: str, senha_atual: str, nova_senha: str)
    }

    class EditarUsuarioView {
        +get(request): HttpResponse
        +post(request): HttpResponse
    }

    class FormularioEdicaoUsuario {
        +username: str
        +email: str
        +senha_atual: str
        +nova_senha: str
        +is_valid(): bool
    }

    class UserModel {
        +check_password(senha: str): bool
        +set_password(nova_senha: str)
        +save()
    }

    class BancoDeDados {
        +atualizar_usuario(usuario: Usuario)
    }

    Usuario --|> UserModel : "Herança"
    EditarUsuarioView --> FormularioEdicaoUsuario : "Usa"
    FormularioEdicaoUsuario --> UserModel : "Valida senha"
    UserModel --> BancoDeDados : "Salva alterações"

```