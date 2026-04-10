"""
database.py - Módulo de gestão da base de dados SQLite
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

import sqlite3
import os
from logger import registar_log

# Caminho para o ficheiro da base de dados
CAMINHO_BD = "autorent.db"


def criar_tabelas():
    """
    Cria todas as tabelas da base de dados caso ainda não existam.
    Tabelas: Viaturas, Clientes, Alugueres.
    """
    try:
        # Ligar à base de dados (cria o ficheiro se não existir)
        con = sqlite3.connect(CAMINHO_BD)
        cur = con.cursor()

        # ------------------------------------------------------------------
        # Tabela VIATURAS
        # Guarda toda a informação sobre as viaturas disponíveis para aluguer
        # ------------------------------------------------------------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS viaturas (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                marca           TEXT    NOT NULL,
                modelo          TEXT    NOT NULL,
                matricula       TEXT    NOT NULL UNIQUE,
                num_assentos    INTEGER NOT NULL,
                valor_dia       REAL    NOT NULL,
                estado          TEXT    NOT NULL CHECK(estado IN ('Nova', 'Seminova', 'Usada', 'Em mau estado')),
                disponibilidade TEXT    NOT NULL DEFAULT 'Disponível' CHECK(disponibilidade IN ('Disponível', 'Alugada'))
            )
        """)

        # ------------------------------------------------------------------
        # Tabela CLIENTES
        # Guarda os dados pessoais e financeiros de cada cliente
        # ------------------------------------------------------------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                nome            TEXT    NOT NULL,
                data_nascimento TEXT    NOT NULL,
                sexo            TEXT    NOT NULL CHECK(sexo IN ('M', 'F', 'Outro')),
                nif             TEXT    NOT NULL UNIQUE,
                telemovel       TEXT    NOT NULL,
                email           TEXT    NOT NULL UNIQUE,
                cota_mensal     REAL    NOT NULL
            )
        """)

        # ------------------------------------------------------------------
        # Tabela ALUGUERES
        # Regista cada contrato de aluguer, ligando viatura a cliente
        # ------------------------------------------------------------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alugueres (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                viatura_id  INTEGER NOT NULL,
                cliente_id  INTEGER NOT NULL,
                data_inicio TEXT    NOT NULL,
                data_fim    TEXT    NOT NULL,
                valor_total REAL    NOT NULL,
                estado      TEXT    NOT NULL DEFAULT 'Previsto' CHECK(estado IN ('Previsto', 'Em curso', 'Terminado', 'Cancelado')),
                FOREIGN KEY (viatura_id) REFERENCES viaturas(id),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)

        con.commit()  # Guardar as alterações
        con.close()   # Fechar a ligação
        return True

    except sqlite3.Error as e:
        registar_log("ERRO", f"Erro ao criar tabelas: {e}")
        print(f"[ERRO] Erro ao criar tabelas: {e}")
        return False


def inicializar_bd():
    """
    Ponto de entrada para inicializar a base de dados.
    Chamado no arranque da aplicação em main.py.
    """
    criado = not os.path.exists(CAMINHO_BD)  # Verificar se é a primeira execução
    sucesso = criar_tabelas()

    if sucesso and criado:
        print("[OK] Base de dados criada com sucesso.")
    elif not sucesso:
        print("[ERRO] Falha ao inicializar a base de dados.")

    return sucesso
