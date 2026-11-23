"""Testes simples da lógica do Axes v0.1. Rode com: python -m unittest discover -s tests -v"""

import tempfile
import unittest
from pathlib import Path

from axes_core import (
    atualizar_departamento,
    cadastrar_departamento,
    calcular_atingimento,
    carregar_departamentos,
    encontrar_departamento,
    gerar_relatorio,
    remover_departamento,
    salvar_departamentos,
)


class TestAxesCore(unittest.TestCase):
    def test_calculo(self):
        self.assertEqual(calcular_atingimento(7, 10), 70)
        with self.assertRaises(ValueError):
            calcular_atingimento(1, 0)
        with self.assertRaises(ValueError):
            calcular_atingimento(-1, 10)

    def test_cadastro_atualizacao_e_remocao(self):
        registros = []
        cadastrar_departamento(registros, " pesquisa ", 7, 10)
        self.assertEqual(encontrar_departamento(registros, "PESQUISA")["contratacoes"], "7")
        with self.assertRaises(ValueError):
            cadastrar_departamento(registros, "pesquisa", 4, 10)
        atualizar_departamento(registros, "pesquisa", 9, 10)
        self.assertIn("90.00%", gerar_relatorio(registros)[0])
        self.assertTrue(remover_departamento(registros, "PESQUISA"))
        self.assertFalse(remover_departamento(registros, "PESQUISA"))

    def test_persistencia_em_csv(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "departamentos.csv"
            registros = []
            cadastrar_departamento(registros, "RH", 5, 10)
            salvar_departamentos(registros, arquivo)
            recuperados = carregar_departamentos(arquivo)
            self.assertEqual(recuperados, registros)
            atualizar_departamento(recuperados, "RH", 10, 10)
            salvar_departamentos(recuperados, arquivo)
            self.assertIn("100.00%", gerar_relatorio(carregar_departamentos(arquivo))[0])

    def test_csv_invalido_nao_sobrescrito(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "departamentos.csv"
            arquivo.write_text("nome,contratacoes,meta\nRH,abc,20\n", encoding="utf-8")
            registros = carregar_departamentos(arquivo)
            self.assertIn("ERRO", gerar_relatorio(registros)[0])


if __name__ == "__main__":
    unittest.main()
