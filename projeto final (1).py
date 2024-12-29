import sqlite3
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename

# Classe para gerenciar o banco de dados
class BancoDeDados:
    def __init__(self, nome_banco="tarefas.db"):
        self.nome_banco = nome_banco
        self.conectar()
        self.criar_tabela()

    def conectar(self):
        self.conexao = sqlite3.connect(self.nome_banco)
        self.cursor = self.conexao.cursor()

    def criar_tabela(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            prazo TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
            comentarios TEXT DEFAULT ''
        )
        """)
        self.conexao.commit()

    def adicionar_tarefa(self, tarefa):
        self.cursor.execute("""
        INSERT INTO tarefas (descricao, data_inicio, prazo, responsavel)
        VALUES (?, ?, ?, ?)
        """, (tarefa.descricao, tarefa.data_inicio, tarefa.prazo, tarefa.responsavel))
        self.conexao.commit()

    def listar_tarefas(self):
        self.cursor.execute("SELECT * FROM tarefas")
        return self.cursor.fetchall()

    def atualizar_status(self, id_tarefa, novo_status, comentario=""):
        self.cursor.execute("UPDATE tarefas SET status = ?, comentarios = ? WHERE id = ?", (novo_status, comentario, id_tarefa))
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()

# Classe para representar uma tarefa
class Tarefa:
    def __init__(self, descricao, data_inicio, prazo, responsavel, status="Pendente"):
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.prazo = prazo
        self.responsavel = responsavel
        self.status = status

    @staticmethod
    def validar_datas(data_inicio, prazo):
        try:
            datetime.strptime(data_inicio, "%d/%m/%Y")
            datetime.strptime(prazo, "%d/%m/%Y")
            return True
        except ValueError:
            return False

# Classe para gerenciar a interface gráfica
class Interface:
    def __init__(self, banco):
        self.banco = banco
        self.root = tk.Tk()
        self.root.title("Gerenciamento de Tarefas")

        tk.Button(self.root, text="Adicionar Tarefa", command=self.adicionar_tarefa_gui).pack(pady=10)
        tk.Button(self.root, text="Exibir Tarefas", command=self.exibir_tarefas_gui).pack(pady=10)
        tk.Button(self.root, text="Atualizar Status", command=self.atualizar_status_gui).pack(pady=10)
        tk.Button(self.root, text="Gerar Relatório CSV", command=self.gerar_relatorio_csv).pack(pady=10)
        tk.Button(self.root, text="Verificar Prazos", command=self.verificar_prazos).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.root.destroy).pack(pady=10)

        self.root.mainloop()

    def adicionar_tarefa_gui(self):
        def salvar_tarefa():
            descricao = descricao_entry.get()
            data_inicio = data_inicio_entry.get()
            prazo = prazo_entry.get()
            responsavel = responsavel_entry.get()

            if not all([descricao, data_inicio, prazo, responsavel]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
                return

            if not Tarefa.validar_datas(data_inicio, prazo):
                messagebox.showerror("Erro", "Datas devem estar no formato dd/mm/aaaa!")
                return

            tarefa = Tarefa(descricao, data_inicio, prazo, responsavel)
            self.banco.adicionar_tarefa(tarefa)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            janela.destroy()

        janela = tk.Toplevel()
        janela.title("Adicionar Tarefa")

        tk.Label(janela, text="Descrição").grid(row=0, column=0, padx=5, pady=5)
        descricao_entry = tk.Entry(janela, width=30)
        descricao_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(janela, text="Data Início (dd/mm/aaaa)").grid(row=1, column=0, padx=5, pady=5)
        data_inicio_entry = tk.Entry(janela, width=30)
        data_inicio_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(janela, text="Prazo (dd/mm/aaaa)").grid(row=2, column=0, padx=5, pady=5)
        prazo_entry = tk.Entry(janela, width=30)
        prazo_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(janela, text="Responsável").grid(row=3, column=0, padx=5, pady=5)
        responsavel_entry = tk.Entry(janela, width=30)
        responsavel_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(janela, text="Salvar", command=salvar_tarefa).grid(row=4, column=0, columnspan=2, pady=10)

    def atualizar_status_gui(self):
        def atualizar():
            id_tarefa = id_entry.get()
            status = status_var.get()
            comentario = comentario_entry.get() if status == "Em andamento" else ""

            if not id_tarefa.isdigit():
                messagebox.showerror("Erro", "ID da tarefa deve ser um número!")
                return

            self.banco.atualizar_status(int(id_tarefa), status, comentario)
            messagebox.showinfo("Sucesso", f"Status da tarefa {id_tarefa} atualizado para {status}!")
            janela.destroy()

        janela = tk.Toplevel()
        janela.title("Atualizar Status da Tarefa")

        tk.Label(janela, text="ID da Tarefa").grid(row=0, column=0, padx=5, pady=5)
        id_entry = tk.Entry(janela)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(janela, text="Novo Status").grid(row=1, column=0, padx=5, pady=5)
        status_var = tk.StringVar(value="Pendente")
        status_menu = ttk.Combobox(janela, textvariable=status_var, values=["Pendente", "Em andamento", "Concluído"])
        status_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(janela, text="Comentário").grid(row=2, column=0, padx=5, pady=5)
        comentario_entry = tk.Entry(janela)
        comentario_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(janela, text="Atualizar", command=atualizar).grid(row=3, column=0, columnspan=2, pady=10)

    def exibir_tarefas_gui(self):
        tarefas = self.banco.listar_tarefas()
        janela = tk.Toplevel()
        janela.title("Tarefas")

        tree = ttk.Treeview(janela, columns=("ID", "Descrição", "Data Início", "Prazo", "Responsável", "Status", "Comentários"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Data Início", text="Data Início")
        tree.heading("Prazo", text="Prazo")
        tree.heading("Responsável", text="Responsável")
        tree.heading("Status", text="Status")
        tree.heading("Comentários", text="Comentários")
        tree.pack(fill="both", expand=True)

        for tarefa in tarefas:
            tree.insert("", "end", values=tarefa)

    def gerar_relatorio_csv(self):
        tarefas = self.banco.listar_tarefas()
        if not tarefas:
            messagebox.showinfo("Relatório", "Nenhuma tarefa cadastrada para gerar relatório.")
            return

        df = pd.DataFrame(tarefas, columns=["ID", "Descrição", "Data Início", "Prazo", "Responsável", "Status", "Comentários"])
        caminho = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if caminho:
            df.to_csv(caminho, index=False, encoding="utf-8")
            messagebox.showinfo("Relatório", f"Relatório salvo em {caminho}")

    def verificar_prazos(self):
        tarefas = self.banco.listar_tarefas()
        mensagens = []
        hoje = datetime.now()

        for tarefa in tarefas:
            prazo = datetime.strptime(tarefa[3], "%d/%m/%Y")
            dias_restantes = (prazo - hoje).days
            if dias_restantes < 0 and tarefa[5] != "Concluído":
                mensagens.append(f"Tarefa {tarefa[0]} ('{tarefa[1]}') está ATRASADA!")
            elif 0 <= dias_restantes <= 2 and tarefa[5] != "Concluído":
                mensagens.append(f"Tarefa {tarefa[0]} ('{tarefa[1]}') está com prazo próximo: {dias_restantes} dias restantes.")

        if mensagens:
            messagebox.showwarning("Atenção! Prazos", "\n".join(mensagens))
        else:
            messagebox.showinfo("Prazos", "Nenhuma tarefa com problemas de prazo.")

# Inicialização
if __name__ == "__main__":
    banco = BancoDeDados()
    Interface(banco)
    banco.fechar()
