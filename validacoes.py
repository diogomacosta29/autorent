"""
validacoes.py - Módulo de validação de inputs do utilizador
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

import re
from datetime import datetime


# ------------------------------------------------------------------
# TEXTOS GERAIS
# ------------------------------------------------------------------

def validar_texto(valor: str, nome_campo: str, min_chars: int = 2, max_chars: int = 100) -> bool:
    """
    Valida que um campo de texto não está vazio e tem um comprimento aceitável.
    Parâmetros:
        valor      (str): Texto introduzido pelo utilizador.
        nome_campo (str): Nome do campo (para mensagem de erro).
        min_chars  (int): Comprimento mínimo permitido (padrão: 2).
        max_chars  (int): Comprimento máximo permitido (padrão: 100).
    Retorna: True se válido, False caso contrário.
    """
    valor = valor.strip()
    if len(valor) < min_chars:
        print(f"[ERRO] O campo '{nome_campo}' deve ter pelo menos {min_chars} caracteres.")
        return False
    if len(valor) > max_chars:
        print(f"[ERRO] O campo '{nome_campo}' não pode ter mais de {max_chars} caracteres.")
        return False
    return True


# ------------------------------------------------------------------
# NIF
# ------------------------------------------------------------------

def validar_nif(nif: str) -> bool:
    """
    Valida o NIF português.
    Regras: 9 dígitos, começa por 1, 2, 3, 5, 6, 7, 8 ou 9.
    Parâmetros:
        nif (str): NIF introduzido pelo utilizador.
    Retorna: True se válido, False caso contrário.
    """
    nif = nif.strip()

    # Verificar se tem exatamente 9 dígitos
    if not re.fullmatch(r"\d{9}", nif):
        print("[ERRO] O NIF deve ter exatamente 9 dígitos numéricos.")
        return False

    # Verificar se começa por um dígito válido
    primeiro_digito = int(nif[0])
    if primeiro_digito not in [1, 2, 3, 5, 6, 7, 8, 9]:
        print("[ERRO] NIF inválido. O primeiro dígito não é permitido.")
        return False

    # Validar dígito de controlo
    total = sum(int(nif[i]) * (9 - i) for i in range(8))
    resto = total % 11
    digito_controlo = 0 if resto < 2 else 11 - resto

    if digito_controlo != int(nif[8]):
        print("[ERRO] NIF inválido. Dígito de controlo incorreto.")
        return False

    return True


# ------------------------------------------------------------------
# EMAIL
# ------------------------------------------------------------------

def validar_email(email: str) -> bool:
    """
    Valida o formato de um endereço de email.
    Parâmetros:
        email (str): Email introduzido pelo utilizador.
    Retorna: True se válido, False caso contrário.
    """
    email = email.strip()
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"

    if not re.fullmatch(padrao, email):
        print("[ERRO] Email inválido. Formato esperado: exemplo@dominio.com")
        return False

    return True


# ------------------------------------------------------------------
# TELEMÓVEL
# ------------------------------------------------------------------

def validar_telemovel(telemovel: str) -> bool:
    """
    Valida número de telemóvel português.
    Aceita números com 9 dígitos, começando por 9 (móvel) ou 2/3 (fixo).
    Parâmetros:
        telemovel (str): Número introduzido pelo utilizador.
    Retorna: True se válido, False caso contrário.
    """
    # Remover espaços e hífenes para facilitar validação
    telemovel = telemovel.strip().replace(" ", "").replace("-", "")

    if not re.fullmatch(r"[923]\d{8}", telemovel):
        print("[ERRO] Telemóvel inválido. Deve ter 9 dígitos e começar por 9, 2 ou 3.")
        return False

    return True


# ------------------------------------------------------------------
# MATRÍCULA
# ------------------------------------------------------------------

def validar_matricula(matricula: str) -> bool:
    """
    Valida matrícula portuguesa.
    Formatos aceites:
        - Novo formato: AA-00-AA (letras-números-letras)
        - Intermédio:   00-AA-00 (números-letras-números)
        - Antigo:       00-00-AA (números-números-letras)
    Parâmetros:
        matricula (str): Matrícula introduzida pelo utilizador.
    Retorna: True se válida, False caso contrário.
    """
    matricula = matricula.strip().upper()

    padroes = [
        r"^[A-Z]{2}-\d{2}-[A-Z]{2}$",   # Novo:       AA-00-AA
        r"^\d{2}-[A-Z]{2}-\d{2}$",        # Intermédio: 00-AA-00
        r"^\d{2}-\d{2}-[A-Z]{2}$",        # Antigo:     00-00-AA
    ]

    for padrao in padroes:
        if re.fullmatch(padrao, matricula):
            return True

    print("[ERRO] Matrícula inválida. Formatos aceites: AA-00-AA, 00-AA-00 ou 00-00-AA")
    return False


# ------------------------------------------------------------------
# DATAS
# ------------------------------------------------------------------

def validar_data(data: str, nome_campo: str = "data") -> bool:
    """
    Valida que uma data está no formato DD-MM-AAAA e é uma data real.
    Parâmetros:
        data       (str): Data introduzida pelo utilizador.
        nome_campo (str): Nome do campo para mensagem de erro.
    Retorna: True se válida, False caso contrário.
    """
    data = data.strip()
    try:
        datetime.strptime(data, "%d-%m-%Y")
        return True
    except ValueError:
        print(f"[ERRO] {nome_campo} inválida. Formato esperado: DD-MM-AAAA (ex: 25-12-1990)")
        return False


def validar_periodo_aluguer(data_inicio: str, data_fim: str) -> bool:
    """
    Valida que o período de aluguer é coerente:
        - Ambas as datas no formato DD-MM-AAAA
        - A data de fim é posterior à data de início
        - A data de início não é anterior a hoje
    Parâmetros:
        data_inicio (str): Data de início do aluguer.
        data_fim    (str): Data de fim do aluguer.
    Retorna: True se válido, False caso contrário.
    """
    # Validar formato de ambas as datas
    if not validar_data(data_inicio, "Data de início"):
        return False
    if not validar_data(data_fim, "Data de fim"):
        return False

    inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
    fim    = datetime.strptime(data_fim,    "%d-%m-%Y")
    hoje   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # A data de início não pode ser no passado
    if inicio < hoje:
        print("[ERRO] A data de início não pode ser anterior a hoje.")
        return False

    # A data de fim deve ser posterior à data de início
    if fim <= inicio:
        print("[ERRO] A data de fim deve ser posterior à data de início.")
        return False

    return True


def validar_data_nascimento(data: str) -> bool:
    """
    Valida a data de nascimento:
        - Formato DD-MM-AAAA
        - Não pode ser no futuro
        - Idade mínima de 18 anos (para poder alugar)
    Parâmetros:
        data (str): Data de nascimento introduzida pelo utilizador.
    Retorna: True se válida, False caso contrário.
    """
    if not validar_data(data, "Data de nascimento"):
        return False

    nascimento = datetime.strptime(data, "%d-%m-%Y")
    hoje = datetime.now()

    if nascimento > hoje:
        print("[ERRO] A data de nascimento não pode ser no futuro.")
        return False

    # Calcular idade
    idade = hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )

    if idade < 18:
        print(f"[ERRO] O cliente deve ter pelo menos 18 anos (idade introduzida: {idade}).")
        return False

    return True


# ------------------------------------------------------------------
# VALORES NUMÉRICOS
# ------------------------------------------------------------------

def validar_valor_positivo(valor: str, nome_campo: str) -> bool:
    """
    Valida que um valor numérico é positivo (maior que zero).
    Parâmetros:
        valor      (str): Valor introduzido pelo utilizador (como texto).
        nome_campo (str): Nome do campo para mensagem de erro.
    Retorna: True se válido, False caso contrário.
    """
    try:
        numero = float(valor.strip().replace(",", "."))
        if numero <= 0:
            print(f"[ERRO] O campo '{nome_campo}' deve ser maior que zero.")
            return False
        return True
    except ValueError:
        print(f"[ERRO] O campo '{nome_campo}' deve ser um número válido.")
        return False


def validar_inteiro_positivo(valor: str, nome_campo: str) -> bool:
    """
    Valida que um valor é um número inteiro positivo.
    Parâmetros:
        valor      (str): Valor introduzido pelo utilizador (como texto).
        nome_campo (str): Nome do campo para mensagem de erro.
    Retorna: True se válido, False caso contrário.
    """
    try:
        numero = int(valor.strip())
        if numero <= 0:
            print(f"[ERRO] O campo '{nome_campo}' deve ser um número inteiro maior que zero.")
            return False
        return True
    except ValueError:
        print(f"[ERRO] O campo '{nome_campo}' deve ser um número inteiro válido.")
        return False


# ------------------------------------------------------------------
# OPÇÕES DE MENU
# ------------------------------------------------------------------

def validar_opcao_menu(opcao: str, opcoes_validas: list) -> bool:
    """
    Valida que a opção introduzida pelo utilizador é uma das opções válidas do menu.
    Parâmetros:
        opcao         (str):  Opção introduzida pelo utilizador.
        opcoes_validas (list): Lista de opções válidas (ex: ['1','2','3','0']).
    Retorna: True se válida, False caso contrário.
    """
    if opcao.strip() not in opcoes_validas:
        print(f"[ERRO] Opção inválida. Escolha entre: {', '.join(opcoes_validas)}")
        return False
    return True