"""Testes da estrutura do OKR Core (Parte 2)."""

import tempfile
import unittest
from pathlib import Path

from okr_core import OKRCore


class TestOKRCore(unittest.TestCase):
    def test_cadastro_relacionado(self):
        with tempfile.TemporaryDirectory() as pasta:
            banco = OKRCore(Path(pasta) / "teste.db")
            area = banco.cadastrar_area("Pessoas e Cultura")
            colaborador = banco.cadastrar_colaborador("Pessoa Fictícia", area)
            ciclo = banco.cadastrar_ciclo(2027, 1)
            objetivo = banco.cadastrar_objetivo("Melhorar a experiência", area, ciclo, colaborador)
            kr = banco.cadastrar_kr(
                "Diminuir tempo de contratação", objetivo, 45, 30, "dias", "diminuir", colaborador
            )
            self.assertEqual(banco.listar("krs")[0]["id"], kr)
            self.assertEqual(len(banco.listar("areas")), 1)
            outro = OKRCore(Path(pasta) / "teste.db")
            self.assertEqual(len(outro.listar("krs")), 1)  # Persistência entre aberturas

    def test_invalidos(self):
        with tempfile.TemporaryDirectory() as pasta:
            banco = OKRCore(Path(pasta) / "teste.db")
            with self.assertRaises(ValueError):
                banco.cadastrar_ciclo(2027, 5)
            with self.assertRaises(ValueError):
                banco.listar("usuarios; DROP TABLE areas")


if __name__ == "__main__":
    unittest.main()
