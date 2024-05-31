import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os

# Configuração do banco de dados SQLite
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Criação da tabela de usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')

# Criação da tabela de tarefas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
''')
conn.commit()

# Função para registrar o login no arquivo de log
def registrar_login(usuario):
    with open('login_log.txt', 'a') as arquivo:
        arquivo.write(f'{datetime.now()}: {usuario} fez login.\n')

# Função para apagar o log mensalmente
def limpar_log_mensal():
    if os.path.exists('login_log.txt'):
        tempo_modificacao = datetime.fromtimestamp(os.path.getmtime('login_log.txt'))
        if datetime.now() - tempo_modificacao > timedelta(days=30):
            os.remove('login_log.txt')

# Função para carregar e mostrar o log de login
def mostrar_log():
    if os.path.exists('login_log.txt'):
        with open('login_log.txt', 'r') as arquivo:
            return arquivo.read()
    else:
        return "Nenhum log de login disponível."

# Limpar o log mensalmente ao iniciar o programa
limpar_log_mensal()

# Classe principal da aplicação
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Gerenciamento de Tarefas')
        self.geometry('400x300')
        self.usuario_atual = None
        self.criar_tela_login()

    # Criar tela de login
    def criar_tela_login(self):
        self.limpar_tela()

        tk.Label(self, text='Login', font=('Arial', 14)).pack(pady=10)
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text='Usuário').grid(row=0, column=0, padx=5, pady=5)
        self.login_usuario = ttk.Entry(frame)
        self.login_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text='Senha').grid(row=1, column=0, padx=5, pady=5)
        self.login_senha = ttk.Entry(frame, show='*')
        self.login_senha.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text='Login', command=self.login).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame, text='Cadastrar', command=self.criar_tela_cadastro).grid(row=3, columnspan=2, pady=5)
        tk.Button(frame, text='Ver Log de Login', command=self.ver_log_login).grid(row=4, columnspan=2, pady=5)

    # Criar tela de cadastro
    def criar_tela_cadastro(self):
        self.limpar_tela()

        tk.Label(self, text='Cadastro', font=('Arial', 14)).pack(pady=10)
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text='Usuário').grid(row=0, column=0, padx=5, pady=5)
        self.cadastro_usuario = ttk.Entry(frame)
        self.cadastro_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text='Senha').grid(row=1, column=0, padx=5, pady=5)
        self.cadastro_senha = ttk.Entry(frame, show='*')
        self.cadastro_senha.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text='Registrar', command=self.cadastrar).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame, text='Voltar', command=self.criar_tela_login).grid(row=3, columnspan=2, pady=5)

    # Função para limpar a tela atual
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Função de login
    def login(self):
        usuario = self.login_usuario.get()
        senha = self.login_senha.get()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
        usuario_bd = cursor.fetchone()
        if usuario_bd:
            self.usuario_atual = usuario_bd
            registrar_login(usuario)
            self.criar_tela_tarefas()
        else:
            messagebox.showerror('Erro', 'Usuário ou senha incorretos')

    # Função de cadastro de novo usuário
    def cadastrar(self):
        usuario = self.cadastro_usuario.get()
        senha = self.cadastro_senha.get()
        try:
            cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso')
            self.criar_tela_login()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'Usuário já existe')

    # Criar tela de gerenciamento de tarefas
    def criar_tela_tarefas(self):
        self.limpar_tela()

        tk.Label(self, text='Gerenciamento de Tarefas', font=('Arial', 14)).pack(pady=20)
        tk.Button(self, text='Adicionar Tarefa', command=self.criar_tela_adicionar_tarefa).pack(pady=5)
        tk.Button(self, text='Visualizar Tarefas', command=self.visualizar_tarefas).pack(pady=5)
        tk.Button(self, text='Sair', command=self.criar_tela_login).pack(pady=5)

    # Criar tela para adicionar nova tarefa
    def criar_tela_adicionar_tarefa(self):
        self.limpar_tela()

        tk.Label(self, text='Adicionar Tarefa', font=('Arial', 14)).pack(pady=20)
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text='Título').grid(row=0, column=0, padx=5, pady=5)
        self.tarefa_titulo = ttk.Entry(frame)
        self.tarefa_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text='Descrição').grid(row=1, column=0, padx=5, pady=5)
        self.tarefa_descricao = ttk.Entry(frame)
        self.tarefa_descricao.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text='Salvar', command=self.adicionar_tarefa).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame, text='Voltar', command=self.criar_tela_tarefas).grid(row=3, columnspan=2, pady=5)

    # Função para adicionar nova tarefa
    def adicionar_tarefa(self):
        titulo = self.tarefa_titulo.get()
        descricao = self.tarefa_descricao.get()
        cursor.execute('INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)', (self.usuario_atual[0], titulo, descricao))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Tarefa adicionada com sucesso')
        self.criar_tela_tarefas()

    # Criar tela para visualizar as tarefas
    def visualizar_tarefas(self):
        self.limpar_tela()

        tk.Label(self, text='Suas Tarefas', font=('Arial', 14)).pack(pady=20)
        tarefas = cursor.execute('SELECT * FROM tarefas WHERE usuario_id = ?', (self.usuario_atual[0],)).fetchall()
        for tarefa in tarefas:
            frame_tarefa = ttk.Frame(self)
            frame_tarefa.pack(pady=5, fill='x')
            ttk.Label(frame_tarefa, text=f'Título: {tarefa[2]}').pack(side='left')
            ttk.Button(frame_tarefa, text='Editar', command=lambda t=tarefa: self.criar_tela_editar_tarefa(t)).pack(side='left')
            ttk.Button(frame_tarefa, text='Excluir', command=lambda t=tarefa: self.excluir_tarefa(t)).pack(side='left')
        tk.Button(self, text='Voltar', command=self.criar_tela_tarefas).pack(pady=10)

    # Criar tela para editar tarefa
    def criar_tela_editar_tarefa(self, tarefa):
        self.limpar_tela()

        tk.Label(self, text='Editar Tarefa', font=('Arial', 14)).pack(pady=20)
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text='Título').grid(row=0, column=0, padx=5, pady=5)
        self.editar_tarefa_titulo = ttk.Entry(frame)
        self.editar_tarefa_titulo.grid(row=0, column=1, padx=5, pady=5)
        self.editar_tarefa_titulo.insert(0, tarefa[2])

        tk.Label(frame, text='Descrição').grid(row=1, column=0, padx=5, pady=5)
        self.editar_tarefa_descricao = ttk.Entry(frame)
        self.editar_tarefa_descricao.grid(row=1, column=1, padx=5, pady=5)
        self.editar_tarefa_descricao.insert(0, tarefa[3])

        tk.Button(frame, text='Salvar', command=lambda: self.atualizar_tarefa(tarefa[0])).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame, text='Voltar', command=self.visualizar_tarefas).grid(row=3, columnspan=2, pady=5)

    # Função para atualizar tarefa
    def atualizar_tarefa(self, tarefa_id):
        titulo = self.editar_tarefa_titulo.get()
        descricao = self.editar_tarefa_descricao.get()
        cursor.execute('UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ?', (titulo, descricao, tarefa_id))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Tarefa atualizada com sucesso')
        self.visualizar_tarefas()

    # Função para excluir tarefa
    def excluir_tarefa(self, tarefa):
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa[0],))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Tarefa excluída com sucesso')
        self.visualizar_tarefas()

    # Função para visualizar o log de login
    def ver_log_login(self):
        self.limpar_tela()

        tk.Label(self, text='Log de Login', font=('Arial', 14)).pack(pady=20)
        log_conteudo = mostrar_log()
        log_text = tk.Text(self, wrap='word', height=15, width=50)
        log_text.insert('1.0', log_conteudo)
        log_text.config(state='disabled')
        log_text.pack(pady=10)
        tk.Button(self, text='Voltar', command=self.criar_tela_login).pack(pady=10)

# Executar a aplicação
if __name__ == '__main__':
    app = App()
    app.mainloop()
