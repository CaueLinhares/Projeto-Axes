"""Parte 2 (OKR Core): banco de dados SQLite e cadastro das entidades básicas."""

import sqlite3
import math
from contextlib import contextmanager
from pathlib import Path


class OKRCore:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.criar_tabelas()

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            yield conexao
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def criar_tabelas(self):
        with self.conectar() as banco:
            banco.executescript("""
                CREATE TABLE IF NOT EXISTS areas (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL UNIQUE COLLATE NOCASE
                );
                CREATE TABLE IF NOT EXISTS colaboradores (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    area_id INTEGER NOT NULL REFERENCES areas(id)
                );
                CREATE TABLE IF NOT EXISTS ciclos (
                    id INTEGER PRIMARY KEY,
                    ano INTEGER NOT NULL CHECK (ano >= 2000),
                    trimestre INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
                    UNIQUE (ano, trimestre)
                );
                CREATE TABLE IF NOT EXISTS objetivos (
                    id INTEGER PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    area_id INTEGER NOT NULL REFERENCES areas(id),
                    ciclo_id INTEGER NOT NULL REFERENCES ciclos(id),
                    responsavel_id INTEGER REFERENCES colaboradores(id)
                );
                CREATE TABLE IF NOT EXISTS krs (
                    id INTEGER PRIMARY KEY,
                    descricao TEXT NOT NULL,
                    objetivo_id INTEGER NOT NULL REFERENCES objetivos(id),
                    valor_inicial REAL NOT NULL,
                    meta REAL NOT NULL,
                    unidade TEXT NOT NULL,
                    direcao TEXT NOT NULL CHECK (direcao IN ('aumentar', 'diminuir')),
                    responsavel_id INTEGER REFERENCES colaboradores(id)
                );
            """)

    @staticmethod
    def texto_valido(valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("O texto não pode estar vazio.")
        return valor

    def cadastrar_area(self, nome):
        nome = self.texto_valido(nome).upper()
        with self.conectar() as banco:
            cursor = banco.execute("INSERT INTO areas (nome) VALUES (?)", (nome,))
            return cursor.lastrowid

    def cadastrar_colaborador(self, nome, area_id):
        nome = self.texto_valido(nome)
        with self.conectar() as banco:
            cursor = banco.execute(
                "INSERT INTO colaboradores (nome, area_id) VALUES (?, ?)",
                (nome, area_id),
            )
            return cursor.lastrowid

    def cadastrar_ciclo(self, ano, trimestre):
        if not (2000 <= ano <= 2100) or trimestre not in (1, 2, 3, 4):
            raise ValueError("Ano ou trimestre inválido.")
        with self.conectar() as banco:
            cursor = banco.execute(
                "INSERT INTO ciclos (ano, trimestre) VALUES (?, ?)",
                (ano, trimestre),
            )
            return cursor.lastrowid

    def cadastrar_objetivo(self, titulo, area_id, ciclo_id, responsavel_id=None):
        titulo = self.texto_valido(titulo)
        with self.conectar() as banco:
            cursor = banco.execute(
                "INSERT INTO objetivos (titulo, area_id, ciclo_id, responsavel_id) VALUES (?, ?, ?, ?)",
                (titulo, area_id, ciclo_id, responsavel_id),
            )
            return cursor.lastrowid

    def cadastrar_kr(self, descricao, objetivo_id, inicial, meta, unidade, direcao, responsavel_id=None):
        descricao = self.texto_valido(descricao)
        unidade = self.texto_valido(unidade)
        if direcao not in ("aumentar", "diminuir"):
            raise ValueError("Direção deve ser 'aumentar' ou 'diminuir'.")
        inicial, meta = float(inicial), float(meta)
        if not (math.isfinite(inicial) and math.isfinite(meta)):
            raise ValueError("Valores precisam ser números finitos.")
        if inicial == meta:
            raise ValueError("Meta precisa ser diferente do valor inicial.")
        if direcao == "aumentar" and meta < inicial:
            raise ValueError("Meta deve ser maior que o início para o tipo aumentar.")
        if direcao == "diminuir" and meta > inicial:
            raise ValueError("Meta deve ser menor que o início para o tipo diminuir.")
        with self.conectar() as banco:
            cursor = banco.execute(
                """INSERT INTO krs
                (descricao, objetivo_id, valor_inicial, meta, unidade, direcao, responsavel_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (descricao, objetivo_id, inicial, meta, unidade, direcao, responsavel_id),
            )
            return cursor.lastrowid

    def listar(self, tabela):
        # Lista permitida evita montar SQL com um nome de tabela fornecido pelo usuário.
        tabelas = {"areas", "colaboradores", "ciclos", "objetivos", "krs"}
        if tabela not in tabelas:
            raise ValueError("Tabela não permitida.")
        with self.conectar() as banco:
            banco.row_factory = sqlite3.Row
            return [dict(linha) for linha in banco.execute(f"SELECT * FROM {tabela} ORDER BY id")]
