"""
main.py - Ponto de entrada da aplicação AutoRent
AutoRent, Lda. - Sistema de gestão de aluguer de viaturas
"""

from database import inicializar_bd
from viaturas import (adicionar_viatura, listar_viaturas,
                      listar_viaturas_disponiveis, editar_viatura)
from clientes import adicionar_cliente, listar_clientes, editar_cliente
from alugueres import (criar_aluguer, listar_alugueres,
                       listar_viaturas_alugadas, encerrar_aluguer,
                       cancelar_aluguer)


# ------------------------------------------------------------------
# UTILITÁRIO DE ECRÃ
# ------------------------------------------------------------------

def limpar_ecra():
    """Limpa o terminal para melhorar a legibilidade dos menus."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa a execução até o utilizador carregar Enter."""
    input("\nCarregue Enter para continuar...")


# ------------------------------------------------------------------
# MENU VIATURAS
# ------------------------------------------------------------------

def menu_viaturas():
    """Menu de gestão de viaturas com as operações disponíveis."""
    while True:
        limpar_ecra()
        print("=" * 45)
        print("        GESTÃO DE VIATURAS")
        print("=" * 45)
        print("  1. Adicionar viatura")
        print("  2. Listar todas as viaturas")
        print("  3. Viaturas disponíveis")
        print("  4. Editar viatura")
        print("-" * 45)
        print("  0. Voltar ao menu principal")
        print("=" * 45)

        opcao = input("Opção: ").strip()

        if opcao == "1":
            adicionar_viatura()
            pausar()
        elif opcao == "2":
            listar_viaturas()
            pausar()
        elif opcao == "3":
            listar_viaturas_disponiveis()
            pausar()
        elif opcao == "4":
            editar_viatura()
            pausar()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida.")
            pausar()


# ------------------------------------------------------------------
# MENU CLIENTES
# ------------------------------------------------------------------

def menu_clientes():
    """Menu de gestão de clientes com as operações disponíveis."""
    while True:
        limpar_ecra()
        print("=" * 45)
        print("        GESTÃO DE CLIENTES")
        print("=" * 45)
        print("  1. Adicionar cliente")
        print("  2. Listar todos os clientes")
        print("  3. Editar cliente")
        print("-" * 45)
        print("  0. Voltar ao menu principal")
        print("=" * 45)

        opcao = input("Opção: ").strip()

        if opcao == "1":
            adicionar_cliente()
            pausar()
        elif opcao == "2":
            listar_clientes()
            pausar()
        elif opcao == "3":
            editar_cliente()
            pausar()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida.")
            pausar()


# ------------------------------------------------------------------
# MENU ALUGUERES
# ------------------------------------------------------------------

def menu_alugueres():
    """Menu de gestão de alugueres com as operações disponíveis."""
    while True:
        limpar_ecra()
        print("=" * 45)
        print("        GESTÃO DE ALUGUERES")
        print("=" * 45)
        print("  1. Novo aluguer")
        print("  2. Listar todos os alugueres")
        print("  3. Viaturas atualmente alugadas")
        print("  4. Encerrar aluguer")
        print("  5. Cancelar aluguer")
        print("-" * 45)
        print("  0. Voltar ao menu principal")
        print("=" * 45)

        opcao = input("Opção: ").strip()

        if opcao == "1":
            criar_aluguer()
            pausar()
        elif opcao == "2":
            listar_alugueres()
            pausar()
        elif opcao == "3":
            listar_viaturas_alugadas()
            pausar()
        elif opcao == "4":
            encerrar_aluguer()
            pausar()
        elif opcao == "5":
            cancelar_aluguer()
            pausar()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida.")
            pausar()


# ------------------------------------------------------------------
# MENU PRINCIPAL
# ------------------------------------------------------------------

def menu_principal():
    """Menu principal da aplicação. Ponto de entrada após inicialização."""
    while True:
        limpar_ecra()
        print("=" * 45)
        print("     AUTORENT, LDA. - GESTÃO DE ALUGUERES")
        print("=" * 45)
        print("  1. Viaturas")
        print("  2. Clientes")
        print("  3. Alugueres")
        print("-" * 45)
        print("  0. Sair")
        print("=" * 45)

        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_viaturas()
        elif opcao == "2":
            menu_clientes()
        elif opcao == "3":
            menu_alugueres()
        elif opcao == "0":
            print("\nAté logo!")
            break
        else:
            print("[ERRO] Opção inválida.")
            pausar()


# ------------------------------------------------------------------
# ARRANQUE DA APLICAÇÃO
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Inicializar a base de dados antes de abrir os menus
    if inicializar_bd():
        menu_principal()
    else:
        print("[ERRO CRÍTICO] Não foi possível inicializar a base de dados. A aplicação vai encerrar.")