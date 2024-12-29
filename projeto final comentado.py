import sqlite3  # Importa a biblioteca para interagir com bancos de dados SQLite.
import pandas as pd  # Importa o pandas para manipulação de dados e geração de relatórios.
from datetime import datetime  # Importa a classe datetime para manipulação de datas.
import tkinter as tk  # Importa tkinter para criar a interface gráfica.
from tkinter import messagebox, ttk  # Importa componentes adicionais do tkinter para janelas de mensagens e widgets avançados.
from tkinter.filedialog import asksaveasfilename  # Importa função para salvar arquivos através de uma interface gráfica.

# Classe para gerenciar o banco de dados
class BancoDeDados:
    def __init__(self, nome_banco="tarefas.db"):  # Inicializa a classe com o nome do banco de dados.
        self.nome_banco = nome_banco  # Define o nome do banco.
        self.conectar()  # Chama o método para estabelecer conexão com o banco.
        self.criar_tabela()  # Cria a tabela "tarefas" caso não exista.

    def conectar(self):  # Conecta ao banco de dados SQLite.
        self.conexao = sqlite3.connect(self.nome_banco)  # Cria uma conexão com o banco de dados.
        self.cursor = self.conexao.cursor()  # Cria um cursor para executar comandos SQL.

    def criar_tabela(self):  # Cria a tabela de tarefas se ainda não existir.
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID único para cada tarefa.
            descricao TEXT NOT NULL,  # Descrição da tarefa.
            data_inicio TEXT NOT NULL,  # Data de início da tarefa.
            prazo TEXT NOT NULL,  # Prazo para conclusão da tarefa.
            responsavel TEXT NOT NULL,  # Pessoa responsável pela tarefa.
            status TEXT DEFAULT 'Pendente',  # Status da tarefa (padrão: Pendente).
            comentarios TEXT DEFAULT ''  # Comentários opcionais.
        )
        """)
        self.conexao.commit()  # Salva as alterações no banco de dados.

    def adicionar_tarefa(self, tarefa):  # Adiciona uma nova tarefa ao banco.
        self.cursor.execute("""
        INSERT INTO tarefas (descricao, data_inicio, prazo, responsavel)
        VALUES (?, ?, ?, ?)
        """, (tarefa.descricao, tarefa.data_inicio, tarefa.prazo, tarefa.responsavel))
        self.conexao.commit()  # Salva as alterações no banco.

    def listar_tarefas(self):  # Retorna todas as tarefas cadastradas.
        self.cursor.execute("SELECT * FROM tarefas")
        return self.cursor.fetchall()  # Retorna os resultados da consulta.

    def atualizar_status(self, id_tarefa, novo_status, comentario=""):  # Atualiza o status e comentários de uma tarefa.
        self.cursor.execute("UPDATE tarefas SET status = ?, comentarios = ? WHERE id = ?", (novo_status, comentario, id_tarefa))
        self.conexao.commit()  # Salva as alterações no banco.

    def fechar(self):  # Fecha a conexão com o banco de dados.
        self.conexao.close()

# Classe para representar uma tarefa
class Tarefa:
    def __init__(self, descricao, data_inicio, prazo, responsavel, status="Pendente"):  # Define os atributos da tarefa.
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.prazo = prazo
        self.responsavel = responsavel
        self.status = status

    @staticmethod
    def validar_datas(data_inicio, prazo):  # Valida se as datas estão no formato correto.
        try:
            datetime.strptime(data_inicio, "%d/%m/%Y")  # Tenta converter a data de início.
            datetime.strptime(prazo, "%d/%m/%Y")  # Tenta converter o prazo.
            return True  # Retorna True se as datas forem válidas.
        except ValueError:  # Captura erros de conversão.
            return False

# Classe para gerenciar a interface gráfica
class Interface:
    def __init__(self, banco):  # Inicializa a interface com uma referência ao banco de dados.
        self.banco = banco
        self.root = tk.Tk()  # Cria a janela principal.
        self.root.title("Gerenciamento de Tarefas")  # Define o título da janela.

        # Cria botões para as funcionalidades principais.
        tk.Button(self.root, text="Adicionar Tarefa", command=self.adicionar_tarefa_gui).pack(pady=10)
        tk.Button(self.root, text="Exibir Tarefas", command=self.exibir_tarefas_gui).pack(pady=10)
        tk.Button(self.root, text="Atualizar Status", command=self.atualizar_status_gui).pack(pady=10)
        tk.Button(self.root, text="Gerar Relatório CSV", command=self.gerar_relatorio_csv).pack(pady=10)
        tk.Button(self.root, text="Verificar Prazos", command=self.verificar_prazos).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.root.destroy).pack(pady=10)

        self.root.mainloop()  # Inicia o loop principal da interface gráfica.

    def adicionar_tarefa_gui(self):  # Janela para adicionar uma nova tarefa.
        def salvar_tarefa():  # Função chamada ao salvar uma tarefa.
            ...

    # Outros métodos implementam as funcionalidades adicionais: atualização de status, exibição de tarefas, etc.

# Inicialização
if __name__ == "__main__":  # Executa o programa principal apenas se o arquivo for executado diretamente.
    banco = BancoDeDados()  # Cria uma instância do banco de dados.
    Interface(banco)  # Inicializa a interface gráfica.
    banco.fechar()  # Fecha a conexão com o banco após o encerramento.
