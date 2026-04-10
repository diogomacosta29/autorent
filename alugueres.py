"""
alugueres.py - Módulo de gestão de alugueres
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

import sqlite3
from datetime import datetime
from database import CAMINHO_BD
from logger import registar_log
from validacoes import validar_periodo_aluguer, validar_inteiro_positivo
from viaturas import listar_viaturas_disponiveis, atualizar_disponibilidade, obter_viatura_por_id
from clientes import listar_clientes, obter_cliente_por_id


# ------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------------------------------------------

def calcular_valor_total(valor_dia: float, data_inicio: str, data_fim: str) -> float:
    """
    Calcula o valor total do aluguer com base no valor diário e no período.
    Parâmetros:
        valor_dia   (float): Preço por dia da viatura.
        data_inicio (str):   Data de início no formato DD-MM-AAAA.
        data_fim    (str):   Data de fim no formato DD-MM-AAAA.
    Retorna: valor total (float).
    """
    inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
    fim    = datetime.strptime(data_fim,    "%d-%m-%Y")
    num_dias = (fim - inicio).days
    return round(valor_dia * num_dias, 2)


def verificar_cota_cliente(cliente, viatura) -> bool:
    """
    Verifica se o valor mensal da viatura não excede a cota mensal do cliente.
    Regra: valor_dia × 30 <= cota_mensal do cliente.
    Parâmetros:
        cliente: tuplo com os dados do cliente.
        viatura: tuplo com os dados da viatura.
    Retorna: True se dentro da cota, False caso contrário.
    """
    # índice 7 = cota_mensal no cliente | índice 5 = valor_dia na viatura
    cota_mensal  = cliente[7]
    valor_mensal = viatura[5] * 30

    if valor_mensal > cota_mensal:
        print(f"\n[AVISO] Esta viatura custa {valor_mensal:.2f}€/mês ({viatura[5]:.2f}€/dia × 30 dias).")
        print(f"        A cota mensal do cliente é de {cota_mensal:.2f}€.")
        print(f"        O aluguer não pode ser efetuado.")
        return False

    return True


def listar_viaturas_compativeis(cliente):
    """
    Mostra apenas as viaturas disponíveis cuja mensalidade
    não ultrapassa a cota do cliente.
    Parâmetros:
        cliente: tuplo com os dados do cliente.
    """
    cota_mensal = cliente[7]
    valor_dia_max = cota_mensal / 30  # Valor máximo diário compatível com a cota

    print(f"\n--- Viaturas compatíveis com a cota de {cota_mensal:.2f}€/mês ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            SELECT * FROM viaturas
            WHERE disponibilidade = 'Disponível'
            AND valor_dia <= ?
            ORDER BY valor_dia
        """, (valor_dia_max,))

        viaturas = cur.fetchall()
        con.close()

        if not viaturas:
            print("Não existem viaturas disponíveis compatíveis com a cota deste cliente.")
            return

        print(f"\n{'ID':<4} {'Marca':<12} {'Modelo':<15} {'Matrícula':<10} {'Assentos':<9} {'€/Dia':<8} {'€/Mês':<10} {'Estado'}")
        print("-" * 85)

        for v in viaturas:
            valor_mes = v[5] * 30
            print(f"{v[0]:<4} {v[1]:<12} {v[2]:<15} {v[3]:<10} {v[4]:<9} {v[5]:<8.2f} {valor_mes:<10.2f} {v[6]}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar viaturas compatíveis: {e}")
        registar_log("ERRO", f"Erro ao listar viaturas compatíveis: {e}")


# ------------------------------------------------------------------
# CRIAR ALUGUER
# ------------------------------------------------------------------

def criar_aluguer():
    """
    Cria um novo registo de aluguer.
    Valida a disponibilidade da viatura, a cota do cliente
    e calcula automaticamente o valor total.
    """
    print("\n--- Novo Aluguer ---")

    # Mostrar clientes disponíveis e pedir escolha
    listar_clientes()
    id_cliente = input("\nID do cliente (0 para cancelar): ").strip()
    if id_cliente == "0":
        return
    if not validar_inteiro_positivo(id_cliente, "ID do cliente"):
        return

    cliente = obter_cliente_por_id(int(id_cliente))
    if not cliente:
        print("[ERRO] Cliente não encontrado.")
        return

    print(f"\nCliente: {cliente[1]} | Cota mensal: {cliente[7]:.2f}€")

    # Mostrar viaturas disponíveis e verificar compatibilidade com cota
    listar_viaturas_disponiveis()
    id_viatura = input("\nID da viatura (0 para cancelar): ").strip()
    if id_viatura == "0":
        return
    if not validar_inteiro_positivo(id_viatura, "ID da viatura"):
        return

    viatura = obter_viatura_por_id(int(id_viatura))
    if not viatura:
        print("[ERRO] Viatura não encontrada.")
        return

    # Verificar se a viatura está disponível
    if viatura[7] != "Disponível":
        print(f"[ERRO] A viatura {viatura[1]} {viatura[2]} não está disponível.")
        return

    # Verificar se a viatura é compatível com a cota do cliente
    if not verificar_cota_cliente(cliente, viatura):
        print("\nViaturas compatíveis com a sua cota:")
        listar_viaturas_compativeis(cliente)
        return

    # Datas do aluguer
    data_inicio = input("\nData de início (DD-MM-AAAA): ").strip()
    data_fim    = input("Data de fim    (DD-MM-AAAA): ").strip()

    if not validar_periodo_aluguer(data_inicio, data_fim):
        return

    # Calcular valor total automaticamente
    valor_total = calcular_valor_total(viatura[5], data_inicio, data_fim)
    num_dias    = (datetime.strptime(data_fim, "%d-%m-%Y") - datetime.strptime(data_inicio, "%d-%m-%Y")).days

    # Determinar estado inicial: Em curso se começa hoje, Previsto se é futuro
    hoje        = datetime.now().strftime("%d-%m-%Y")
    estado      = "Em curso" if data_inicio == hoje else "Previsto"

    # Confirmar com o utilizador antes de registar
    print(f"\n--- Resumo do Aluguer ---")
    print(f"  Cliente : {cliente[1]}")
    print(f"  Viatura : {viatura[1]} {viatura[2]} ({viatura[3]})")
    print(f"  Período : {data_inicio} → {data_fim} ({num_dias} dias)")
    print(f"  Total   : {valor_total:.2f}€")
    print(f"  Estado  : {estado}")

    confirmacao = input("\nConfirmar aluguer? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Aluguer cancelado.")
        return

    # Inserir na base de dados e marcar viatura como alugada
    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            INSERT INTO alugueres (viatura_id, cliente_id, data_inicio, data_fim, valor_total, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (int(id_viatura), int(id_cliente), data_inicio, data_fim, valor_total, estado))

        con.commit()
        con.close()

        # Atualizar disponibilidade da viatura para 'Alugada'
        atualizar_disponibilidade(int(id_viatura), "Alugada")

        print(f"\n[OK] Aluguer registado com sucesso! Total: {valor_total:.2f}€")
        registar_log("ALUGUER", f"Novo aluguer: {viatura[1]} {viatura[2]} ({viatura[3]}) -> {cliente[1]} | {data_inicio} a {data_fim} | {valor_total:.2f}€")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao registar aluguer: {e}")
        registar_log("ERRO", f"Erro ao criar aluguer: {e}")


# ------------------------------------------------------------------
# LISTAR ALUGUERES
# ------------------------------------------------------------------

def listar_alugueres():
    """
    Mostra todos os alugueres registados com informação
    do cliente e da viatura associados.
    """
    print("\n--- Lista de Alugueres ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        # JOIN para mostrar nomes em vez de IDs
        cur.execute("""
            SELECT a.id, c.nome, v.marca || ' ' || v.modelo, v.matricula,
                   a.data_inicio, a.data_fim, a.valor_total, a.estado
            FROM alugueres a
            JOIN clientes  c ON a.cliente_id = c.id
            JOIN viaturas  v ON a.viatura_id = v.id
            ORDER BY a.id DESC
        """)

        alugueres = cur.fetchall()
        con.close()

        if not alugueres:
            print("Não existem alugueres registados.")
            return

        print(f"\n{'ID':<4} {'Cliente':<22} {'Viatura':<20} {'Matrícula':<10} {'Início':<12} {'Fim':<12} {'Total (€)':<10} {'Estado'}")
        print("-" * 105)

        for a in alugueres:
            print(f"{a[0]:<4} {a[1]:<22} {a[2]:<20} {a[3]:<10} {a[4]:<12} {a[5]:<12} {a[6]:<10.2f} {a[7]}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar alugueres: {e}")
        registar_log("ERRO", f"Erro ao listar alugueres: {e}")


# ------------------------------------------------------------------
# LISTAR VIATURAS ATUALMENTE ALUGADAS
# ------------------------------------------------------------------

def listar_viaturas_alugadas():
    """
    Mostra as viaturas com estado 'Em curso' e o cliente associado.
    """
    print("\n--- Viaturas Atualmente Alugadas ---")

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("""
            SELECT a.id, v.marca || ' ' || v.modelo, v.matricula,
                   c.nome, c.telemovel, a.data_inicio, a.data_fim, a.valor_total
            FROM alugueres a
            JOIN viaturas v ON a.viatura_id = v.id
            JOIN clientes c ON a.cliente_id = c.id
            WHERE a.estado = 'Em curso'
            ORDER BY a.data_fim
        """)

        alugueres = cur.fetchall()
        con.close()

        if not alugueres:
            print("Não existem viaturas alugadas neste momento.")
            return

        print(f"\n{'ID':<4} {'Viatura':<22} {'Matrícula':<10} {'Cliente':<22} {'Telemóvel':<12} {'Início':<12} {'Fim':<12} {'Total (€)'}")
        print("-" * 110)

        for a in alugueres:
            print(f"{a[0]:<4} {a[1]:<22} {a[2]:<10} {a[3]:<22} {a[4]:<12} {a[5]:<12} {a[6]:<12} {a[7]:.2f}")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao listar viaturas alugadas: {e}")
        registar_log("ERRO", f"Erro ao listar viaturas alugadas: {e}")


# ------------------------------------------------------------------
# ENCERRAR ALUGUER
# ------------------------------------------------------------------

def encerrar_aluguer():
    """
    Marca um aluguer como 'Terminado' e liberta a viatura,
    colocando-a novamente como 'Disponível'.
    """
    print("\n--- Encerrar Aluguer ---")
    listar_viaturas_alugadas()

    id_aluguer = input("\nID do aluguer a encerrar (0 para cancelar): ").strip()
    if id_aluguer == "0":
        return
    if not validar_inteiro_positivo(id_aluguer, "ID do aluguer"):
        return

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        # Verificar se o aluguer existe e está em curso
        cur.execute("SELECT * FROM alugueres WHERE id = ?", (int(id_aluguer),))
        aluguer = cur.fetchone()
        con.close()

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao procurar aluguer: {e}")
        registar_log("ERRO", f"Erro ao procurar aluguer ID {id_aluguer}: {e}")
        return

    if not aluguer:
        print("[ERRO] Aluguer não encontrado.")
        return

    if aluguer[6] not in ("Em curso", "Previsto"):
        print(f"[ERRO] Este aluguer não pode ser encerrado (estado atual: {aluguer[6]}).")
        return

    # Confirmar encerramento
    confirmacao = input("Confirmar encerramento? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("UPDATE alugueres SET estado = 'Terminado' WHERE id = ?", (int(id_aluguer),))

        con.commit()
        con.close()

        # Libertar a viatura
        atualizar_disponibilidade(aluguer[1], "Disponível")

        print(f"\n[OK] Aluguer encerrado. Viatura devolvida e disponível.")
        registar_log("ALUGUER", f"Aluguer ID {id_aluguer} encerrado. Viatura ID {aluguer[1]} libertada.")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao encerrar aluguer: {e}")
        registar_log("ERRO", f"Erro ao encerrar aluguer ID {id_aluguer}: {e}")


# ------------------------------------------------------------------
# CANCELAR ALUGUER
# ------------------------------------------------------------------

def cancelar_aluguer():
    """
    Cancela um aluguer com estado 'Previsto' ou 'Em curso'
    e liberta a viatura associada.
    """
    print("\n--- Cancelar Aluguer ---")
    listar_alugueres()

    id_aluguer = input("\nID do aluguer a cancelar (0 para cancelar operação): ").strip()
    if id_aluguer == "0":
        return
    if not validar_inteiro_positivo(id_aluguer, "ID do aluguer"):
        return

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()
        cur.execute("SELECT * FROM alugueres WHERE id = ?", (int(id_aluguer),))
        aluguer = cur.fetchone()
        con.close()

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao procurar aluguer: {e}")
        registar_log("ERRO", f"Erro ao procurar aluguer ID {id_aluguer}: {e}")
        return

    if not aluguer:
        print("[ERRO] Aluguer não encontrado.")
        return

    if aluguer[6] in ("Terminado", "Cancelado"):
        print(f"[ERRO] Este aluguer já está {aluguer[6]} e não pode ser cancelado.")
        return

    # Confirmar cancelamento
    confirmacao = input(f"Tem a certeza que quer cancelar o aluguer ID {id_aluguer}? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    try:
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        cur.execute("UPDATE alugueres SET estado = 'Cancelado' WHERE id = ?", (int(id_aluguer),))

        con.commit()
        con.close()

        # Libertar a viatura
        atualizar_disponibilidade(aluguer[1], "Disponível")

        print(f"\n[OK] Aluguer ID {id_aluguer} cancelado. Viatura disponível novamente.")
        registar_log("ALUGUER", f"Aluguer ID {id_aluguer} cancelado. Viatura ID {aluguer[1]} libertada.")

    except sqlite3.Error as e:
        print(f"[ERRO] Erro ao cancelar aluguer: {e}")
        registar_log("ERRO", f"Erro ao cancelar aluguer ID {id_aluguer}: {e}")