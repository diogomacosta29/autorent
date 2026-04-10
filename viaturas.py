"""
viaturas.py - Módulo de gestão de viaturas
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

import sqlite3
from database import CAMINHO_BD
from logger import registar_log
from validacoes import (validar_texto, validar_matricula,
                        validar_valor_positivo, validar_inteiro_positivo)

# Estados possíveis de uma viatura
ESTADOS_VIATURA = ["Nova", "Seminova", "Usada", "Em mau estado"]


# ------------------------------------------------------------------
# ADICIONAR VIATURA
# ------------------------------------------------------------------

def adicionar_viatura():
    """
    Pede os dados de uma nova viatura ao utilizador, valida-os
    e insere o registo na tabela viaturas.
    """
    print("\n--- Adicionar Viatura ---")

    # Marca
    marca = input("Marca: ").strip()
    if not validar_texto(marca, "Marca"):
        return

    # Modelo
    modelo = input("Modelo: ").strip()
    if not validar_texto(modelo, "Modelo"):
        return

    # Matrícula
    matricula = input("Matrícula (ex: AA-00-AA): ").strip().upper()
    if not validar_matricula(matricula):
        return

    # Número de assentos
    assentos = input("Número de assentos: ").strip()
    if not validar_inteiro_positivo(assentos, "Número de assentos"):
        return

    # Valor por dia
    valor_dia = input("Valor por dia (€): ").strip()
    if not validar_valor_positivo(valor_dia, "Valor por dia"):
        return

    # Estado da viatura
    print("Estado da viatura:")
    for i, estado in enumerate(ESTADOS_VIATURA, 1):
        print(f"  {i}. {estado}")
    opcao_estado = input("Escolha (1-4): ").strip()
    if opcao_estado not in ["1", "2", "3", "4"]:
        print("[ERRO] Opção de estado inválida.")
        return
    estado = ESTADOS_VIATURA[int(opcao_estado) - 1]

    # Inserir na base de dados
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            INSERT INTO viaturas (marca, modelo, matricula, num_assentos, valor_dia, estado, disponibilidade)
            VALUES (?, ?, ?, ?, ?, ?, 'Disponível')
        """, (marca, modelo, matricula, int(assentos), float(valor_dia.replace(",", ".")), estado))

        con.commit()
        con.close()

        print(f"\n[OK] Viatura {marca} {modelo} ({matricula}) adicionada com sucesso!")
        registar_log("VIATURA", f"Nova viatura adicionada: {marca} {modelo} - {matricula}")

    except sqlite3.IntegrityError:
        # Matrícula duplicada (campo UNIQUE na BD)
        print(f"[ERRO] Já existe uma viatura com a matrícula {matricula}.")
        registar_log("ERRO", f"Tentativa de adicionar matrícula duplicada: {matricula}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao guardar viatura: {e}")
        registar_log("ERRO", f"Erro ao adicionar viatura: {e}")


# ------------------------------------------------------------------
# LISTAR VIATURAS
# ------------------------------------------------------------------

def listar_viaturas():
    """
    Mostra todas as viaturas registadas na base de dados.
    """
    print("\n--- Lista de Viaturas ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("SELECT * FROM viaturas ORDER BY marca, modelo")
        viaturas = cur.fetchall()
        con.close()

        if not viaturas:
            print("Não existem viaturas registadas.")
            return

        # Cabeçalho da tabela
        print(f"\n{'ID':<4} {'Marca':<12} {'Modelo':<15} {'Matrícula':<10} {'Assentos':<9} {'€/Dia':<8} {'Estado':<15} {'Disponib.'}")
        print("-" * 90)

        for v in viaturas:
            print(f"{v[0]:<4} {v[1]:<12} {v[2]:<15} {v[3]:<10} {v[4]:<9} {v[5]:<8.2f} {v[6]:<15} {v[7]}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar viaturas: {e}")
        registar_log("ERRO", f"Erro ao listar viaturas: {e}")


# ------------------------------------------------------------------
# LISTAR VIATURAS DISPONÍVEIS
# ------------------------------------------------------------------

def listar_viaturas_disponiveis():
    """
    Mostra apenas as viaturas com disponibilidade = 'Disponível'.
    """
    print("\n--- Viaturas Disponíveis ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            SELECT * FROM viaturas
            WHERE disponibilidade = 'Disponível'
            ORDER BY valor_dia
        """)
        viaturas = cur.fetchall()
        con.close()

        if not viaturas:
            print("Não existem viaturas disponíveis de momento.")
            return

        print(f"\n{'ID':<4} {'Marca':<12} {'Modelo':<15} {'Matrícula':<10} {'Assentos':<9} {'€/Dia':<8} {'Estado'}")
        print("-" * 75)

        for v in viaturas:
            print(f"{v[0]:<4} {v[1]:<12} {v[2]:<15} {v[3]:<10} {v[4]:<9} {v[5]:<8.2f} {v[6]}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar viaturas disponíveis: {e}")
        registar_log("ERRO", f"Erro ao listar viaturas disponíveis: {e}")


# ------------------------------------------------------------------
# EDITAR VIATURA
# ------------------------------------------------------------------

def editar_viatura():
    """
    Permite alterar os dados de uma viatura existente.
    O utilizador escolhe o campo a alterar.
    """
    print("\n--- Editar Viatura ---")
    listar_viaturas()

    id_viatura = input("\nID da viatura a editar (0 para cancelar): ").strip()
    if id_viatura == "0":
        return
    if not validar_inteiro_positivo(id_viatura, "ID"):
        return

    # Verificar se a viatura existe
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()
        cur.execute("SELECT * FROM viaturas WHERE id = ?", (int(id_viatura),))
        viatura = cur.fetchone()
        con.close()
    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao procurar viatura: {e}")
        registar_log("ERRO", f"Erro ao procurar viatura ID {id_viatura}: {e}")
        return

    if not viatura:
        print("[ERRO] Viatura não encontrada.")
        return

    print(f"\nViatura selecionada: {viatura[1]} {viatura[2]} ({viatura[3]})")
    print("\nO que pretende alterar?")
    print("  1. Marca")
    print("  2. Modelo")
    print("  3. Número de assentos")
    print("  4. Valor por dia")
    print("  5. Estado")
    print("  0. Cancelar")

    opcao = input("Opção: ").strip()

    # Determinar o campo e novo valor consoante a opção
    campo   = None
    valor   = None

    if opcao == "0":
        return

    elif opcao == "1":
        valor = input("Nova marca: ").strip()
        if not validar_texto(valor, "Marca"):
            return
        campo = "marca"

    elif opcao == "2":
        valor = input("Novo modelo: ").strip()
        if not validar_texto(valor, "Modelo"):
            return
        campo = "modelo"

    elif opcao == "3":
        valor = input("Novo número de assentos: ").strip()
        if not validar_inteiro_positivo(valor, "Número de assentos"):
            return
        campo = "num_assentos"
        valor = int(valor)

    elif opcao == "4":
        valor = input("Novo valor por dia (€): ").strip()
        if not validar_valor_positivo(valor, "Valor por dia"):
            return
        campo = "valor_dia"
        valor = float(valor.replace(",", "."))

    elif opcao == "5":
        print("Novo estado:")
        for i, estado in enumerate(ESTADOS_VIATURA, 1):
            print(f"  {i}. {estado}")
        opcao_estado = input("Escolha (1-4): ").strip()
        if opcao_estado not in ["1", "2", "3", "4"]:
            print("[ERRO] Opção inválida.")
            return
        campo = "estado"
        valor = ESTADOS_VIATURA[int(opcao_estado) - 1]

    else:
        print("[ERRO] Opção inválida.")
        return

    # Atualizar na base de dados
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute(f"UPDATE viaturas SET {campo} = ? WHERE id = ?", (valor, int(id_viatura)))

        con.commit()
        con.close()

        print(f"\n[OK] Viatura atualizada com sucesso!")
        registar_log("VIATURA", f"Viatura ID {id_viatura} atualizada: campo '{campo}' alterado para '{valor}'")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao atualizar viatura: {e}")
        registar_log("ERRO", f"Erro ao atualizar viatura ID {id_viatura}: {e}")


# ------------------------------------------------------------------
# CONSULTAR VIATURA POR ID
# ------------------------------------------------------------------

def obter_viatura_por_id(id_viatura: int):
    """
    Retorna os dados de uma viatura dado o seu ID.
    Usado internamente por outros módulos (ex: alugueres).
    Parâmetros:
        id_viatura (int): ID da viatura a procurar.
    Retorna: tuplo com os dados da viatura ou None se não existir.
    """
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()
        cur.execute("SELECT * FROM viaturas WHERE id = ?", (id_viatura,))
        viatura = cur.fetchone()
        con.close()
        return viatura

    except sqlite3.Error as e:
        registar_log("ERRO", f"Erro ao obter viatura ID {id_viatura}: {e}")
        return None


# ------------------------------------------------------------------
# ATUALIZAR DISPONIBILIDADE (usado pelo módulo de alugueres)
# ------------------------------------------------------------------

def atualizar_disponibilidade(id_viatura: int, disponibilidade: str):
    """
    Atualiza o estado de disponibilidade de uma viatura.
    Chamado pelo módulo de alugueres ao criar ou encerrar um aluguer.
    Parâmetros:
        id_viatura      (int): ID da viatura.
        disponibilidade (str): 'Disponível' ou 'Alugada'.
    """
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("UPDATE viaturas SET disponibilidade = ? WHERE id = ?",
                    (disponibilidade, id_viatura))

        con.commit()
        con.close()

    except sqlite3.Error as e:
        registar_log("ERRO", f"Erro ao atualizar disponibilidade da viatura ID {id_viatura}: {e}")