"""Regras de negócio da primeira versão do Axes (sem depender do terminal)."""

import csv
import os
import tempfile
from pathlib import Path

COLUNAS = ["nome", "contratacoes", "meta"]


def normalizar_nome(nome):
    return nome.strip().upper()


def validar_indicadores(contratacoes, meta):
    if not isinstance(contratacoes, int) or not isinstance(meta, int):
        raise ValueError("Contratações e meta precisam ser números inteiros.")
    if contratacoes < 0:
        raise ValueError("Contratações não podem ser negativas.")
    if meta <= 0:
        raise ValueError("A meta precisa ser maior que zero.")


def calcular_atingimento(contratacoes, meta):
    validar_indicadores(contratacoes, meta)
    return (contratacoes / meta) * 100


def classificar_atingimento(percentual):
    if percentual >= 100:
        return "Meta atingida!"
    if percentual >= 70:
        return "Estamos próximos da meta."
    return "Estamos abaixo da meta."


def encontrar_departamento(registros, nome):
    nome = normalizar_nome(nome)
    for registro in registros:
        if normalizar_nome(registro["nome"]) == nome:
            return registro
    return None


def cadastrar_departamento(registros, nome, contratacoes, meta):
    nome = normalizar_nome(nome)
    if not nome:
        raise ValueError("O departamento não pode ficar em branco.")
    validar_indicadores(contratacoes, meta)
    if encontrar_departamento(registros, nome) is not None:
        raise ValueError("Departamento já cadastrado.")
    registros.append({"nome": nome, "contratacoes": str(contratacoes), "meta": str(meta)})


def atualizar_departamento(registros, nome, contratacoes, meta):
    validar_indicadores(contratacoes, meta)
    registro = encontrar_departamento(registros, nome)
    if registro is None:
        raise ValueError("Departamento não encontrado.")
    registro["contratacoes"] = str(contratacoes)
    registro["meta"] = str(meta)


def remover_departamento(registros, nome):
    registro = encontrar_departamento(registros, nome)
    if registro is None:
        return False
    registros.remove(registro)
    return True


def gerar_relatorio(registros):
    """Retorna linhas prontas para mostrar; não altera os dados."""
    if not registros:
        return ["Nenhum departamento cadastrado."]

    linhas = []
    for registro in registros:
        nome = registro.get("nome", "SEM NOME")
        try:
            contratacoes = int(registro["contratacoes"])
            meta = int(registro["meta"])
            percentual = calcular_atingimento(contratacoes, meta)
        except (KeyError, ValueError, TypeError) as erro:
            linhas.append(f"{nome}: ERRO - {erro}")
            continue
        linhas.append(f"{nome}: {percentual:.2f}% — {classificar_atingimento(percentual)}")
    return linhas


def carregar_departamentos(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return []

    with caminho.open("r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames != COLUNAS:
            raise ValueError(f"Cabeçalho inválido. Esperado: {', '.join(COLUNAS)}")
        registros = list(leitor)

    # Uma base com registros incorretos não deve ser sobrescrita silenciosamente.
    nomes = set()
    for registro in registros:
        if None in registro or any(registro.get(coluna) is None for coluna in COLUNAS):
            raise ValueError("Existe uma linha CSV malformada.")
        nome = normalizar_nome(registro["nome"] or "")
        if not nome or nome in nomes:
            raise ValueError("Existe departamento vazio ou duplicado no CSV.")
        nomes.add(nome)
    return registros


def salvar_departamentos(registros, caminho):
    """Grava num arquivo temporário e só depois substitui o CSV destino."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", dir=caminho.parent,
            prefix=".axes_", suffix=".tmp", delete=False
        ) as arquivo:
            temporario = Path(arquivo.name)
            escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
            escritor.writeheader()
            escritor.writerows(registros)
        os.replace(temporario, caminho)
    finally:
        if temporario is not None and temporario.exists():
            temporario.unlink()
