"""Parte 2: interface simples de cadastro da estrutura de OKRs."""

import sqlite3
from pathlib import Path
from okr_core import OKRCore

BASE = Path(__file__).resolve().parent
ARQUIVO = BASE / "dados" / "axes_okr.db"


def inteiro(mensagem):
    return int(input(mensagem).strip())


def mostrar_registros(sistema, tabela):
    registros = sistema.listar(tabela)
    if not registros:
        print("Nenhum registro cadastrado.")
    for registro in registros:
        print(registro)


def executar():
    sistema = OKRCore(ARQUIVO)
    print("\n=== AXES OKR CORE — PARTE 2 ===")
    print("Utilize apenas dados fictícios nesta versão de estudos.")

    while True:
        print("\n1. Área  2. Colaborador  3. Ciclo  4. Objetivo  5. KR  6. Consultar  0. Sair")
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "1":
                numero = sistema.cadastrar_area(input("Área: "))
            elif opcao == "2":
                mostrar_registros(sistema, "areas")
                numero = sistema.cadastrar_colaborador(
                    input("Nome fictício: "), inteiro("ID da área: ")
                )
            elif opcao == "3":
                numero = sistema.cadastrar_ciclo(inteiro("Ano: "), inteiro("Trimestre (1-4): "))
            elif opcao == "4":
                mostrar_registros(sistema, "areas")
                mostrar_registros(sistema, "ciclos")
                numero = sistema.cadastrar_objetivo(
                    input("Objetivo: "), inteiro("ID da área: "), inteiro("ID do ciclo: ")
                )
            elif opcao == "5":
                mostrar_registros(sistema, "objetivos")
                numero = sistema.cadastrar_kr(
                    input("Descrição do KR: "), inteiro("ID do objetivo: "),
                    float(input("Valor inicial: ").replace(",", ".")),
                    float(input("Meta: ").replace(",", ".")),
                    input("Unidade (%, dias, R$ etc.): "),
                    input("Direção (aumentar/diminuir): ").strip().lower(),
                )
            elif opcao == "6":
                print("Tabelas: areas, colaboradores, ciclos, objetivos, krs")
                mostrar_registros(sistema, input("Tabela: ").strip().lower())
                continue
            elif opcao == "0":
                print("Até a próxima!")
                break
            else:
                print("Opção inválida.")
                continue
            print(f"Cadastro realizado! ID criado: {numero}")
        except (ValueError, sqlite3.IntegrityError) as erro:
            print(f"ERRO: {erro}")


if __name__ == "__main__":
    executar()
