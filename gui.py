import tkinter as tk
from tkinter import ttk, messagebox
import json
from typing import List, Dict
import os

# Tentar importar PIL, mas não é obrigatório
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class NutriKidsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriKids")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar ícone da janela (apenas se PIL estiver disponível)
        if PIL_AVAILABLE:
            try:
                self.root.iconbitmap("icon.ico")
            except:
                pass
        
        # Configurações de estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar cores e estilos
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure("Title.TLabel", background="#f0f0f0", font=('Helvetica', 32, 'bold'), foreground="#2c3e50")
        self.style.configure("Subtitle.TLabel", background="#f0f0f0", font=('Helvetica', 18, 'bold'), foreground="#34495e")
        self.style.configure("Info.TLabel", background="#f0f0f0", font=('Helvetica', 12), foreground="#7f8c8d")
        
        # Estilo para botões
        self.style.configure("Primary.TButton", 
                           font=('Helvetica', 12, 'bold'),
                           padding=15,
                           background="#3498db",
                           foreground="white")
        self.style.map("Primary.TButton",
                      background=[('active', '#2980b9')],
                      foreground=[('active', 'white')])
        
        self.style.configure("Secondary.TButton", 
                           font=('Helvetica', 12),
                           padding=15,
                           background="#95a5a6",
                           foreground="white")
        self.style.map("Secondary.TButton",
                      background=[('active', '#7f8c8d')],
                      foreground=[('active', 'white')])
        
        # Estilo para campos de entrada
        self.style.configure("TEntry", 
                           padding=10,
                           fieldbackground="white",
                           font=('Helvetica', 12))
        
        # Estilo para radiobuttons
        self.style.configure("TRadiobutton", 
                           background="#f0f0f0",
                           font=('Helvetica', 12))
        
        # Variáveis
        self.login = {
            "status": "",
            "email": "admin@admin.com",
            "senha": "1234"
        }
        
        self.permissions = {
            "funcionario": ["criar", "editar", "visualizar"],
            "responsavel": ["visualizar"]
        }
        
        self.pacientes = self.carregar_pacientes()
        
        # Iniciar com a tela de login
        self.mostrar_tela_login()
    
    def criar_frame_centralizado(self):
        frame = ttk.Frame(self.root, padding="40", style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame
    
    def criar_botao(self, parent, text, command, style="Primary.TButton", width=25):
        return ttk.Button(parent, text=text, command=command, width=width, style=style)
    
    def criar_campo_entrada(self, parent, textvariable, width=30):
        frame = ttk.Frame(parent, style="TFrame")
        entry = ttk.Entry(frame, textvariable=textvariable, width=width, style="TEntry")
        entry.pack(fill=tk.X, pady=5)
        return frame
    
    def carregar_pacientes(self):
        try:
            with open('pacientes.json', 'r') as arquivo:
                return json.load(arquivo)['pacientes']
        except FileNotFoundError:
            return []
    
    def salvar_pacientes(self):
        try:
            with open('pacientes.json', 'w') as arquivo:
                json.dump({'pacientes': self.pacientes}, arquivo, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")
    
    def mostrar_tela_login(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal centralizado
        main_frame = self.criar_frame_centralizado()
        
        # Título com subtítulo
        ttk.Label(main_frame, text="NutriKids", style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(main_frame, text="Sistema de Nutrição Infantil", style="Info.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Frame para o formulário com borda
        form_frame = ttk.Frame(main_frame, style="TFrame")
        form_frame.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
        
        # Tipo de usuário
        ttk.Label(form_frame, text="Tipo de Usuário:", style="TLabel").grid(row=0, column=0, pady=10, sticky=tk.W)
        self.tipo_usuario = tk.StringVar(value="funcionario")
        ttk.Radiobutton(form_frame, text="Funcionário", variable=self.tipo_usuario, 
                       value="funcionario", style="TRadiobutton").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Responsável", variable=self.tipo_usuario, 
                       value="responsavel", style="TRadiobutton").grid(row=1, column=1, sticky=tk.W)
        
        # Email
        ttk.Label(form_frame, text="Email:", style="TLabel").grid(row=2, column=0, pady=10, sticky=tk.W)
        self.email_var = tk.StringVar(value="admin@admin.com")
        self.criar_campo_entrada(form_frame, self.email_var).grid(row=2, column=1, pady=10)
        
        # Senha
        ttk.Label(form_frame, text="Senha:", style="TLabel").grid(row=3, column=0, pady=10, sticky=tk.W)
        self.senha_var = tk.StringVar(value="1234")
        self.criar_campo_entrada(form_frame, self.senha_var).grid(row=3, column=1, pady=10)
        
        # Botão de login
        self.criar_botao(main_frame, "Entrar", self.fazer_login).grid(row=3, column=0, columnspan=2, pady=20)
    
    def fazer_login(self):
        if (self.email_var.get() == self.login["email"] and 
            self.senha_var.get() == self.login["senha"]):
            self.login["status"] = self.tipo_usuario.get()
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")
    
    def mostrar_menu_principal(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal centralizado
        main_frame = self.criar_frame_centralizado()
        
        # Título com subtítulo
        ttk.Label(main_frame, 
                 text=f"Bem-vindo(a), {self.login['status'].capitalize()}!", 
                 style="Subtitle.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(main_frame, 
                 text="Escolha uma opção abaixo", 
                 style="Info.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Botões do menu
        if 'criar' in self.permissions[self.login["status"]]:
            self.criar_botao(button_frame, "Preencher Questionário", 
                           self.mostrar_questionario).pack(pady=15)
        
        if 'visualizar' in self.permissions[self.login["status"]]:
            self.criar_botao(button_frame, "Visualizar Recomendações", 
                           self.mostrar_recomendacoes).pack(pady=15)
        
        self.criar_botao(button_frame, "Logout", 
                        self.logout, style="Secondary.TButton").pack(pady=15)
    
    def mostrar_questionario(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal com scroll
        canvas = tk.Canvas(self.root, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título com subtítulo
        ttk.Label(scrollable_frame, text="Questionário", 
                 style="Subtitle.TLabel").grid(row=0, column=0, columnspan=2, pady=(20, 10))
        ttk.Label(scrollable_frame, text="Preencha os dados da criança", 
                 style="Info.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Campos do questionário
        self.campos = {}
        campos_info = [
            ('nome', 'Nome da Criança:', 'str'),
            ('idade', 'Idade (meses):', 'int'),
            ('peso', 'Peso (kg):', 'float'),
            ('sexo', 'Sexo:', 'str'),
            ('restricao', 'Restrição Alimentar:', 'str'),
            ('formula', 'Fórmula (se aplicável):', 'str'),
            ('frequencia', 'Frequência de Mamadas (por dia):', 'int'),
            ('observacoes', 'Observações Clínicas:', 'str')
        ]
        
        for i, (campo, label, tipo) in enumerate(campos_info):
            ttk.Label(scrollable_frame, text=label, style="TLabel").grid(row=i+2, column=0, pady=15, sticky=tk.W)
            self.campos[campo] = tk.StringVar()
            self.criar_campo_entrada(scrollable_frame, self.campos[campo], width=40).grid(row=i+2, column=1, pady=15)
        
        # Frame para botões
        button_frame = ttk.Frame(scrollable_frame, style="TFrame")
        button_frame.grid(row=len(campos_info)+2, column=0, columnspan=2, pady=30)
        
        self.criar_botao(button_frame, "Calcular", 
                        self.calcular_volume).pack(side=tk.LEFT, padx=10)
        self.criar_botao(button_frame, "Voltar", 
                        self.mostrar_menu_principal, style="Secondary.TButton").pack(side=tk.LEFT, padx=10)
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def calcular_volume(self):
        try:
            # Validar e converter campos
            dados = {}
            for campo, tipo in [('idade', int), ('peso', float), ('frequencia', int)]:
                try:
                    dados[campo] = tipo(self.campos[campo].get())
                except ValueError:
                    messagebox.showerror("Erro", f"O campo {campo} deve ser um número válido!")
                    return
            
            # Calcular volume
            idade = dados['idade']
            peso = dados['peso']
            mamadas = dados['frequencia']
            fator_ml_kg = 130 if idade <= 1 else 150
            volume_diario = peso * fator_ml_kg
            volume_por_mamada = volume_diario / mamadas
            
            # Criar paciente
            paciente = {
                "nome_da_crianca": self.campos['nome'].get(),
                "recomendacao": f"{self.campos['restricao'].get()} / Fórmula: {self.campos['formula'].get()}",
                "volume_prescrito": f"{volume_por_mamada:.2f} ml por mamada / {volume_diario:.2f} ml por dia",
                "observacoes": self.campos['observacoes'].get()
            }
            
            # Adicionar à lista e salvar
            self.pacientes.append(paciente)
            self.salvar_pacientes()
            
            # Mostrar resultado
            mensagem = f"""
            Cálculo realizado com sucesso!
            
            Volume diário: {volume_diario:.2f} ml
            Volume por mamada: {volume_por_mamada:.2f} ml
            """
            messagebox.showinfo("Resultado", mensagem)
            
            # Voltar ao menu principal
            self.mostrar_menu_principal()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular volume: {str(e)}")
    
    def mostrar_recomendacoes(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = self.criar_frame_centralizado()
        
        # Título com subtítulo
        ttk.Label(main_frame, text="Recomendações", 
                 style="Subtitle.TLabel").grid(row=0, column=0, pady=(0, 10))
        ttk.Label(main_frame, text="Histórico de recomendações nutricionais", 
                 style="Info.TLabel").grid(row=1, column=0, pady=(0, 20))
        
        # Criar área de texto com scrollbar
        text_frame = ttk.Frame(main_frame, style="TFrame")
        text_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        text_area = tk.Text(text_frame, height=20, width=80, 
                           font=('Helvetica', 12),
                           wrap=tk.WORD,
                           bg="white",
                           relief="solid",
                           borderwidth=1)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        # Preencher com as recomendações
        if self.pacientes:
            for paciente in self.pacientes:
                text_area.insert(tk.END, f"\nCriança: {paciente['nome_da_crianca']}\n")
                text_area.insert(tk.END, f"Recomendação: {paciente['recomendacao']}\n")
                text_area.insert(tk.END, f"Volume prescrito: {paciente['volume_prescrito']}\n")
                if paciente['observacoes']:
                    text_area.insert(tk.END, f"Observações clínicas: {paciente['observacoes']}\n")
                text_area.insert(tk.END, "-" * 50 + "\n")
        else:
            text_area.insert(tk.END, "Nenhuma recomendação disponível ainda.")
        
        text_area.config(state=tk.DISABLED)
        
        # Botão voltar
        self.criar_botao(main_frame, "Voltar", 
                        self.mostrar_menu_principal, style="Secondary.TButton").grid(row=3, column=0, pady=20)
    
    def logout(self):
        self.login["status"] = ""
        self.mostrar_tela_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = NutriKidsApp(root)
    root.mainloop() 