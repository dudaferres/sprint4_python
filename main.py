# Responsáveis pelo Projeto:

# NOME                         RM

# Gabriela Queiroga          560035
# Julia Sayuri Yokoo         560541
# Maria Eduarda Ferrés       560418

########################################################################################################################

import json
from typing import List, Dict

print("Seja bem-vindo ao NutriKids!!!")  # Exibe a mensagem de boas-vindas

# Dicionário de login
login = {
    "status": "",  # Armazena o status do usuário (funcionário ou responsável)
    "email": "admin@admin.com",  # Email do usuário para login
    "senha": "1234",  # Senha do usuário para login
}

# Dicionário de permissões
permissions = {
    "funcionario": ["criar", "editar", "visualizar"],  # Permissões para o funcionário
    "responsavel": ["visualizar"]  # Permissões para o responsável
}

# Lista para armazenar os pacientes
pacientes: List[Dict] = []

def carregar_pacientes():
    try:
        with open('pacientes.json', 'r') as arquivo:
            return json.load(arquivo)['pacientes']
    except FileNotFoundError:
        return []

def salvar_pacientes():
    try:
        with open('pacientes.json', 'w') as arquivo:
            json.dump({'pacientes': pacientes}, arquivo, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def ordenar_pacientes_por_nome():
    # Bubble Sort para ordenar pacientes por nome
    n = len(pacientes)
    for i in range(n):
        for j in range(0, n-i-1):
            if pacientes[j]['nome_da_crianca'] > pacientes[j+1]['nome_da_crianca']:
                pacientes[j], pacientes[j+1] = pacientes[j+1], pacientes[j]

def employ_client():
    while True:
        try:
            print("\nEscolha seu tipo de usuário:")
            print("(1) Funcionário")
            print("(2) Responsável")
            stats = input("Digite 1 ou 2: ").strip()
            
            if stats == "1":
                print("\nSeja bem-vindo(a), funcionário!\n")
                login['status'] = "funcionario"
                break
            elif stats == "2":
                print("\nSeja bem-vindo(a), responsável!\n")
                login['status'] = "responsavel"
                break
            else:
                print("Por favor, digite apenas 1 ou 2.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

def log_email():
    while True:
        try:
            print("\nEmail padrão: admin@admin.com")
            email = input("Digite o email: ").strip()
            if email == login["email"]:
                print("\nEmail correto! Por favor, prossiga.\n")
                break
            else:
                print("\nO email que você digitou está incorreto. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

def pass_word():
    while True:
        try:
            print("\nSenha padrão: 1234")
            password = input("Digite a senha: ").strip()
            if not password.isnumeric():
                print("Por favor, digite apenas números!")
            elif password == login["senha"]:
                print("Senha correta! Seja bem-vindo!!!")
                break
            else:
                print("Senha incorreta! Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

def log_in():
    employ_client()
    log_email()
    pass_word()
    return permissions.get(login["status"], [])

def logout():
    print(f"\n{login['status'].capitalize()} desconectado com sucesso!\n")
    login['status'] = ""

# Lista do questionário
quiz_lac = [
    ['Nome', ''],
    ['Idade', 0],
    ['Peso', 0.0],
    ['Sexo', ''],
    ['Restrição alimentar', ''],
    ['Fórmula ( se aplicável )', ''],
    ['Frequência de mamadas ( por dia )', 0],
    ['observações Clínicas', '']
]

def quiz():
    for i in range(len(quiz_lac)):
        while True:
            try:
                resposta = input(f"{quiz_lac[i][0]}: ").strip()
                if resposta:
                    if quiz_lac[i][0] == 'Idade':
                        quiz_lac[i][1] = int(resposta)
                    elif quiz_lac[i][0] == 'Peso':
                        quiz_lac[i][1] = float(resposta)
                    elif quiz_lac[i][0] == 'Frequência de mamadas ( por dia )':
                        quiz_lac[i][1] = int(resposta)
                    else:
                        quiz_lac[i][1] = resposta
                    break
                else:
                    print("Por favor, preencha este campo corretamente.")
            except ValueError:
                print("Por favor, digite um valor válido.")
            except Exception as e:
                print(f"Erro inesperado: {e}")

def choose_unit():
    while True:
        try:
            print("\nComo você gostaria de ver o resultado?")
            print("(1) Mililitros (ml)")
            print("(2) Litros (L)")
            choice = input("Digite 1 ou 2: ")
            if choice in ["1", "2"]:
                return choice
            else:
                print("Opção inválida. Por favor, digite 1 ou 2.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

def calculate_lactary(unit_choice):
    try:
        print("\n=== Cálculo de Volume para Lactário ===\n")
        idade = quiz_lac[1][1]
        peso = quiz_lac[2][1]
        mamadas = quiz_lac[6][1]
        fator_ml_kg = 130 if idade <= 1 else 150
        volume_diario = peso * fator_ml_kg
        volume_por_mamada = volume_diario / mamadas

        if unit_choice == "2":
            volume_diario /= 1000
            volume_por_mamada /= 1000
            unidade = "L"
        else:
            unidade = "ml"

        print("\n=== Resultado do Cálculo ===")
        print(f"Tipo de alimentação: {quiz_lac[4][1]}")
        print(f"Peso: {peso:.2f} kg")
        print(f"Idade: {idade} meses")
        print(f"Volume total por dia: {volume_diario:.2f} {unidade}")
        print(f"Volume por mamada: {volume_por_mamada:.2f} {unidade}")

        if quiz_lac[7][1].strip():
            print(f"Observações clínicas: {quiz_lac[7][1]}")
        else:
            print("Sem observações clínicas.")

        # Salvar dados do paciente
        paciente = {
            "nome_da_crianca": quiz_lac[0][1],
            "recomendacao": f"{quiz_lac[4][1]} / Fórmula: {quiz_lac[5][1]}",
            "volume_prescrito": f"{volume_por_mamada:.2f} {unidade} por mamada / {volume_diario:.2f} {unidade} por dia",
            "observacoes": quiz_lac[7][1]
        }
        pacientes.append(paciente)
        ordenar_pacientes_por_nome()
        salvar_pacientes()

    except Exception as e:
        print(f"Erro durante o cálculo: {e}")

def main_lac():
    quiz()
    unit_choice = choose_unit()
    calculate_lactary(unit_choice)

def view_res():
    print("\n=== VISUALIZAÇÃO DO RESPONSÁVEL ===\n")
    if pacientes:
        for paciente in pacientes:
            print(f"\nCriança: {paciente['nome_da_crianca']}")
            print(f"Recomendação: {paciente['recomendacao']}")
            print(f"Volume prescrito: {paciente['volume_prescrito']}")
            if paciente['observacoes']:
                print(f"Observações clínicas: {paciente['observacoes']}")
            else:
                print("Sem observações clínicas.")
            print("-" * 50)
    else:
        print("Nenhuma recomendação disponível ainda. Aguarde o profissional preencher os dados.")

def choose_path(user_permissions):
    while True:
        try:
            print("\n=== MENU ===")
            if 'criar' in user_permissions or 'editar' in user_permissions:
                print("(1) Preencher questionário e calcular volume")
            if 'visualizar' in user_permissions:
                print("(2) Visualizar recomendações")
            print("(3) Logout")

            opcao = input("Escolha uma opção: ")

            if opcao == "1" and ('criar' in user_permissions or 'editar' in user_permissions):
                main_lac()
            elif opcao == "2" and 'visualizar' in user_permissions:
                view_res()
            elif opcao == "3":
                logout()
                break
            else:
                print("Opção inválida ou não permitida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

def main():
    global pacientes
    pacientes = carregar_pacientes()
    
    while True:
        try:
            permissoes = log_in()
            choose_path(permissoes)

            sair = input("Deseja sair do sistema? (s/n): ").strip().lower()
            if sair == "s":
                print("Encerrando o sistema... Até logo!")
                break
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()