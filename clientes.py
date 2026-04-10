"""
clientes.py - Módulo de gestão de clientes
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

import sqlite3
from database import CAMINHO_BD
from logger import registar_log
from validacoes import (validar_texto, validar_nif, validar_email,
                        validar_telemovel, validar_data_nascimento,
                        validar_valor_positivo)

# Opções de sexo disponíveis
OPCOES_SEXO = ["M", "F", "Outro"]


# ------------------------------------------------------------------
# ADICIONAR CLIENTE
# ------------------------------------------------------------------

def adicionar_cliente():
    """
    Pede os dados de um novo cliente ao utilizador, valida-os
    e insere o registo na tabela clientes.
    """
    print("\n--- Adicionar Cliente ---")

    # Nome completo
    nome = input("Nome completo: ").strip()
    if not validar_texto(nome, "Nome", min_chars=3):
        return

    # Data de nascimento
    data_nascimento = input("Data de nascimento (DD-MM-AAAA): ").strip()
    if not validar_data_nascimento(data_nascimento):
        return

    # Sexo
    print("Sexo:")
    print("  1. Masculino")
    print("  2. Feminino")
    print("  3. Outro")
    opcao_sexo = input("Escolha (1-3): ").strip()
    if opcao_sexo not in ["1", "2", "3"]:
        print("[ERRO] Opção de sexo inválida.")
        return
    sexo = OPCOES_SEXO[int(opcao_sexo) - 1]

    # NIF
    nif = input("NIF: ").strip()
    if not validar_nif(nif):
        return

    # Telemóvel
    telemovel = input("Nº de telemóvel: ").strip()
    if not validar_telemovel(telemovel):
        return

    # Email
    email = input("Email: ").strip()
    if not validar_email(email):
        return

    # Cota mensal
    cota = input("Cota mensal (€): ").strip()
    if not validar_valor_positivo(cota, "Cota mensal"):
        return

    # Inserir na base de dados
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            INSERT INTO clientes (nome, data_nascimento, sexo, nif, telemovel, email, cota_mensal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, data_nascimento, sexo, nif, telemovel, email,
              float(cota.replace(",", "."))))

        con.commit()
        con.close()

        print(f"\n[OK] Cliente '{nome}' registado com sucesso!")
        registar_log("CLIENTE", f"Novo cliente registado: {nome} - NIF {nif}")

    except sqlite3.IntegrityError as e:
        # NIF ou email duplicado (campos UNIQUE na BD)
        if "nif" in str(e):
            print(f"[ERRO] Já existe um cliente com o NIF {nif}.")
        elif "email" in str(e):
            print(f"[ERRO] Já existe um cliente com o email {email}.")
        else:
            print(f"[ERRO] Dados duplicados: {e}")
        registar_log("ERRO", f"Tentativa de registo duplicado - NIF: {nif} / Email: {email}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao guardar cliente: {e}")
        registar_log("ERRO", f"Erro ao adicionar cliente: {e}")


# ------------------------------------------------------------------
# LISTAR CLIENTES
# ------------------------------------------------------------------

def listar_clientes():
    """
    Mostra todos os clientes registados na base de dados.
    """
    print("\n--- Lista de Clientes ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("SELECT * FROM clientes ORDER BY nome")
        clientes = cur.fetchall()
        con.close()

        if not clientes:
            print("Não existem clientes registados.")
            return

        # Cabeçalho da tabela
        print(f"\n{'ID':<4} {'Nome':<25} {'Data Nasc.':<12} {'Sexo':<6} {'NIF':<11} {'Telemóvel':<11} {'Email':<25} {'Cota (€)'}")
        print("-" * 105)

        for c in clientes:
            print(f"{c[0]:<4} {c[1]:<25} {c[2]:<12} {c[3]:<6} {c[4]:<11} {c[5]:<11} {c[6]:<25} {c[7]:.2f}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar clientes: {e}")
        registar_log("ERRO", f"Erro ao listar clientes: {e}")


# ------------------------------------------------------------------
# EDITAR CLIENTE
# ------------------------------------------------------------------

def editar_cliente():
    """
    Permite alterar os dados de um cliente existente.
    O utilizador escolhe o campo a alterar.
    """
    print("\n--- Editar Cliente ---")
    listar_clientes()

    id_cliente = input("\nID do cliente a editar (0 para cancelar): ").strip()
    if id_cliente == "0":
        return

    # Verificar se o cliente existe
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = ?", (int(id_cliente),))
        cliente = cur.fetchone()
        con.close()
    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao procurar cliente: {e}")
        registar_log("ERRO", f"Erro ao procurar cliente ID {id_cliente}: {e}")
        return

    if not cliente:
        print("[ERRO] Cliente não encontrado.")
        return

    print(f"\nCliente selecionado: {cliente[1]} (NIF: {cliente[4]})")
    print("\nO que pretende alterar?")
    print("  1. Nome")
    print("  2. Telemóvel")
    print("  3. Email")
    print("  4. Cota mensal")
    print("  0. Cancelar")

    opcao = input("Opção: ").strip()

    campo = None
    valor = None

    if opcao == "0":
        return

    elif opcao == "1":
        valor = input("Novo nome: ").strip()
        if not validar_texto(valor, "Nome", min_chars=3):
            return
        campo = "nome"

    elif opcao == "2":
        valor = input("Novo telemóvel: ").strip()
        if not validar_telemovel(valor):
            return
        campo = "telemovel"

    elif opcao == "3":
        valor = input("Novo email: ").strip()
        if not validar_email(valor):
            return
        campo = "email"

    elif opcao == "4":
        valor = input("Nova cota mensal (€): ").strip()
        if not validar_valor_positivo(valor, "Cota mensal"):
            return
        campo = "cota_mensal"
        valor = float(valor.replace(",", "."))

    else:
        print("[ERRO] Opção inválida.")
        return

    # Atualizar na base de dados
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute(f"UPDATE clientes SET {campo} = ? WHERE id = ?",
                    (valor, int(id_cliente)))

        con.commit()
        con.close()

        print(f"\n[OK] Cliente atualizado com sucesso!")
        registar_log("CLIENTE", f"Cliente ID {id_cliente} atualizado: campo '{campo}' alterado para '{valor}'")

    except sqlite3.IntegrityError:
        print(f"[ERRO] O valor introduzido já existe noutro registo.")
        registar_log("ERRO", f"Conflito ao atualizar cliente ID {id_cliente}: valor duplicado em '{campo}'")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao atualizar cliente: {e}")
        registar_log("ERRO", f"Erro ao atualizar cliente ID {id_cliente}: {e}")


# ------------------------------------------------------------------
# CONSULTAR CLIENTE POR ID (usado internamente pelos alugueres)
# ------------------------------------------------------------------

def obter_cliente_por_id(id_cliente: int):
    """
    Retorna os dados de um cliente dado o seu ID.
    Usado internamente por outros módulos (ex: alugueres).
    Parâmetros:
        id_cliente (int): ID do cliente a procurar.
    Retorna: tuplo com os dados do cliente ou None se não existir.
    """
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
        cliente = cur.fetchone()
        con.close()
        return cliente

    except sqlite3.Error as e:
        registar_log("ERRO", f"Erro ao obter cliente ID {id_cliente}: {e}")
        return None