"""Interface de terminal do Axes v0.1."""

from pathlib import Path
from axes_core import (
    atualizar_departamento,
    cadastrar_departamento,
    carregar_departamentos,
    encontrar_departamento,
    gerar_relatorio,
    remover_departamento,
    salvar_departamentos,
)

BASE = Path(__file__).resolve().parent
ARQUIVO = BASE / "dados" / "departamentos.csv"


def pedir_inteiro(mensagem, minimo):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:
                print(f"Digite um número maior ou igual a {minimo}.")
            else:
                return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def confirmar(mensagem):
    return input(mensagem).strip().upper() == "S"


def cadastrar_ou_atualizar(registros):
    nome = input("Departamento: ").strip().upper()
    if not nome:
        print("ERRO: informe o nome do departamento.")
        return

    atual = encontrar_departamento(registros, nome)
    if atual is not None:
        print(f"{nome} já existe: {atual['contratacoes']}/{atual['meta']}.")
        if not confirmar("Deseja atualizar? (S/N) "):
            print("Dados mantidos.")
            return

    contratacoes = pedir_inteiro("Contratações realizadas: ", 0)
    meta = pedir_inteiro("Meta de contratações: ", 1)
    if atual is None:
        cadastrar_departamento(registros, nome, contratacoes, meta)
        operacao = "cadastrado"
    else:
        atualizar_departamento(registros, nome, contratacoes, meta)
        operacao = "atualizado"

    salvar_departamentos(registros, ARQUIVO)
    print(f"Departamento {nome} {operacao} com sucesso!")


def excluir(registros):
    nome = input("Departamento para remover: ").strip().upper()
    if encontrar_departamento(registros, nome) is None:
        print("Departamento não encontrado.")
        return
    if not confirmar(f"Confirmar remoção de {nome}? (S/N) "):
        print("Remoção cancelada.")
        return
    remover_departamento(registros, nome)
    salvar_departamentos(registros, ARQUIVO)
    print("Departamento removido com sucesso!")


def mostrar_relatorio(registros):
    print("\n=== RELATÓRIO DE DEPARTAMENTOS ===")
    for linha in gerar_relatorio(registros):
        print(linha)


def executar():
    print("Bem-vindo ao Axes v0.1!")
    try:
        registros = carregar_departamentos(ARQUIVO)
    except (OSError, ValueError) as erro:
        print(f"Não foi possível carregar os dados: {erro}")
        return

    while True:
        print("\n1. Cadastrar ou atualizar  2. Remover  3. Relatório  0. Sair")
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "1":
                cadastrar_ou_atualizar(registros)
                mostrar_relatorio(registros)  # Relatório já atualizado
            elif opcao == "2":
                excluir(registros)
                mostrar_relatorio(registros)
            elif opcao == "3":
                mostrar_relatorio(registros)
            elif opcao == "0":
                print("Até a próxima!")
                break
            else:
                print("Opção inválida.")
        except (OSError, ValueError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")
            # Recarrega, evitando que a memória difira do disco após falha de escrita.
            try:
                registros = carregar_departamentos(ARQUIVO)
            except (OSError, ValueError):
                print("Falha ao recarregar dados. Encerre e verifique o arquivo.")
                break


if __name__ == "__main__":
    executar()
