# Sistema de Gerenciamento de Tarefas

Este é um sistema simples de gerenciamento de tarefas desenvolvido em Python, utilizando o SQLite como banco de dados e Tkinter para a interface gráfica. O sistema permite que os usuários se registrem, façam login, adicionem, visualizem, editem e excluam tarefas.

## Funcionalidades

- Cadastro de novos usuários
- Login de usuários registrados
- Adição de novas tarefas
- Visualização de tarefas
- Edição de tarefas existentes
- Exclusão de tarefas
- Visualização do log de login
- Limpeza automática do log de login a cada 30 dias

## Como Utilizar

### Tela de Login

1. **Login:** Insira seu nome de usuário e senha para fazer login.
2. **Cadastrar:** Clique no botão "Cadastrar" para criar um novo usuário.
3. **Ver Log de Login:** Clique para visualizar o histórico de logins.

### Tela de Cadastro

1. **Usuário:** Insira um nome de usuário único.
2. **Senha:** Insira uma senha.
3. **Registrar:** Clique para criar uma nova conta.
4. **Voltar:** Clique para retornar à tela de login.

### Tela de Gerenciamento de Tarefas

1. **Adicionar Tarefa:** Clique para adicionar uma nova tarefa.
2. **Visualizar Tarefas:** Clique para visualizar suas tarefas.
3. **Sair:** Clique para sair da sessão atual e retornar à tela de login.

### Tela de Adicionar Tarefa

1. **Título:** Insira o título da tarefa.
2. **Descrição:** Insira a descrição da tarefa.
3. **Salvar:** Clique para salvar a nova tarefa.
4. **Voltar:** Clique para retornar à tela de gerenciamento de tarefas.

### Tela de Visualização de Tarefas

1. **Editar:** Clique para editar uma tarefa existente.
2. **Excluir:** Clique para excluir uma tarefa existente.
3. **Voltar:** Clique para retornar à tela de gerenciamento de tarefas.

### Tela de Editar Tarefa

1. **Título:** Edite o título da tarefa.
2. **Descrição:** Edite a descrição da tarefa.
3. **Salvar:** Clique para salvar as alterações na tarefa.
4. **Voltar:** Clique para retornar à tela de visualização de tarefas.

### Tela de Log de Login

1. **Visualização:** Exibe o conteúdo do log de login.
2. **Voltar:** Clique para retornar à tela de login.

## Requisitos

- Python 3.x
- Bibliotecas `tkinter`, `sqlite3`, `datetime`, `os`

## Instruções de Execução

1. Certifique-se de ter o Python instalado em seu sistema.
2. Clone este repositório ou baixe os arquivos.
3. Execute o script principal `tarefas.py`:
   ```bash
   python tarefas.py
   ```

## Estrutura do Projeto

```
|-- tarefas.py
|-- tarefas.db (será gerado automaticamente)
|-- login_log.txt (será gerado automaticamente)
```

## Observações

- O banco de dados `tarefas.db` e o arquivo de log `login_log.txt` serão gerados automaticamente na primeira execução do programa.
- O log de login é automaticamente limpo a cada 30 dias para evitar acúmulo excessivo de dados.

## Contato

Para dúvidas ou sugestões, entre em contato com o desenvolvedor: [brennodeabreu@gmail.com]

---

Esperamos que este sistema seja útil para suas necessidades de gerenciamento de tarefas. Divirta-se utilizando-o!