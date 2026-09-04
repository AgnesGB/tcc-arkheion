"""
Testes unitários para models relacionados a Ficha
"""

from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import (
    Ficha,
    AtributoFicha,
    Atributo,
    PericiaTreinada,
    Pericia,
    NivelClasseFicha,
    Classe,
)


class FichaModelTest(TestCase):
    """Testes para o model Ficha"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.classe = Classe.objects.create(
            nome="Guerreiro",
            proficiencia="Armas",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
        )
        self.ficha = Ficha.objects.create(
            dono=self.user,
            nome="Conan",
            nivel=5,
            cd="15",
            ca="18",
            vida_atual=50,
            mana_atual=0,
            exp=10000,
            deslocamento="9 metros",
            tamanho="Médio",
        )

    def test_criacao_ficha(self):
        """Testa criação de ficha"""
        self.assertEqual(self.ficha.nome, "Conan")
        self.assertEqual(self.ficha.nivel, 5)
        self.assertEqual(self.ficha.dono, self.user)

    def test_str_ficha(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.ficha), "Conan")

    def test_defaults_ficha(self):
        """Testa valores padrão"""
        ficha_nova = Ficha.objects.create(nome="Nova Ficha", dono=self.user)
        self.assertEqual(ficha_nova.nivel, 0)
        self.assertEqual(ficha_nova.cd, "10")
        self.assertEqual(ficha_nova.ca, "10")
        self.assertEqual(ficha_nova.deslocamento, "9 metros/ 6 quadrados")

    def test_calcular_vida_sem_classe(self):
        """Testa cálculo de vida sem classe"""
        vida = self.ficha.calcularVida()
        self.assertEqual(vida, 10)  # Valor padrão

    def test_calcular_vida_com_classe(self):
        """Testa cálculo de vida com classe"""
        # Adiciona atributo Constituição
        atributo_con = Atributo.objects.create(nome="con", ordem=3)
        AtributoFicha.objects.create(
            ficha=self.ficha, atributo=atributo_con, valor=2  # +2 de modificador
        )

        # Adiciona classe
        NivelClasseFicha.objects.create(ficha=self.ficha, classe=self.classe, nivel=5)

        vida = self.ficha.calcularVida()
        # vida_base (20) + const (2) + (vida_por_nivel (5) * nivel (5)) - vida_por_nivel (5)
        # 20 + 2 + 25 - 5 = 42
        self.assertEqual(vida, 42)

    def test_calcular_mana_sem_classe(self):
        """Testa cálculo de mana sem classe"""
        mana = self.ficha.calcularMana()
        self.assertEqual(mana, 0)

    def test_calcular_mana_com_classe_magica(self):
        """Testa cálculo de mana com classe mágica"""
        classe_mago = Classe.objects.create(
            nome="Mago",
            proficiencia="Cajados",
            vida_base=12,
            vida_por_nivel=3,
            mana_base=6,
            mana_por_nivel=6,
        )

        NivelClasseFicha.objects.create(ficha=self.ficha, classe=classe_mago, nivel=5)

        mana = self.ficha.calcularMana()
        # mana_por_nivel (6) * nivel (5) = 30
        self.assertEqual(mana, 30)

    def test_subir_um_nivel(self):
        """Testa método subirUmNivel"""
        nivel_inicial = self.ficha.nivel
        self.ficha.subirUmNivel()
        self.assertEqual(self.ficha.nivel, nivel_inicial + 1)

    def test_setar_nivel(self):
        """Testa método setarNivel"""
        self.ficha.setarNivel(10)
        self.assertEqual(self.ficha.nivel, 10)


class AtributoFichaModelTest(TestCase):
    """Testes para o model AtributoFicha"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Teste", dono=self.user)
        self.atributo = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo, valor=3
        )

    def test_criacao_atributo_ficha(self):
        """Testa criação de atributo na ficha"""
        self.assertEqual(self.atributo_ficha.valor, 3)
        self.assertEqual(self.atributo_ficha.ficha, self.ficha)

    def test_str_atributo_ficha(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.atributo_ficha), "for")

    def test_multiplos_atributos(self):
        """Testa criação de múltiplos atributos para uma ficha"""
        atributos = ["des", "con", "int", "sab", "car"]
        for i, nome_atrib in enumerate(atributos, start=2):
            atrib = Atributo.objects.create(nome=nome_atrib, ordem=i)
            AtributoFicha.objects.create(ficha=self.ficha, atributo=atrib, valor=i)

        self.assertEqual(self.ficha.atributoficha_set.count(), 6)


class PericiaTreinadaModelTest(TestCase):
    """Testes para o model PericiaTreinada"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Teste", nivel=5, dono=self.user)
        self.pericia = Pericia.objects.create(nome="atl", requer_treino=False)
        self.atributo = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo, valor=3
        )

        self.pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha, pericia=self.pericia, treinado=True, bonus_adicional=0
        )
        self.pericia_treinada.atributo_chave.add(self.atributo_ficha)

    def test_criacao_pericia_treinada(self):
        """Testa criação de perícia treinada"""
        self.assertEqual(self.pericia_treinada.ficha, self.ficha)
        self.assertTrue(self.pericia_treinada.treinado)

    def test_str_pericia_treinada(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.pericia_treinada), "atl")

    def test_verificar_treino_nivel_baixo(self):
        """Testa bônus de treino para níveis 1-5"""
        self.ficha.nivel = 3
        bonus = self.pericia_treinada.verificarTreino()
        self.assertEqual(bonus, 2)

    def test_verificar_treino_nivel_medio(self):
        """Testa bônus de treino para níveis 6-14"""
        self.ficha.nivel = 10
        bonus = self.pericia_treinada.verificarTreino()
        self.assertEqual(bonus, 4)

    def test_verificar_treino_nivel_alto(self):
        """Testa bônus de treino para níveis 15+"""
        self.ficha.nivel = 16
        bonus = self.pericia_treinada.verificarTreino()
        self.assertEqual(bonus, 6)

    def test_verificar_treino_nao_treinado(self):
        """Testa que não treinado não dá bônus"""
        self.pericia_treinada.treinado = False
        bonus = self.pericia_treinada.verificarTreino()
        self.assertEqual(bonus, 0)

    def test_calcular_valor(self):
        """Testa cálculo do valor da perícia"""
        self.ficha.nivel = 5
        valor = self.pericia_treinada.calcularValor()
        # (nivel // 2) + valor_atributo + bonus_treino + bonus_adicional
        # (5 // 2) + 3 + 2 + 0 = 7
        self.assertEqual(valor, 7)

    def test_calcular_valor_pericia_requer_treino_sem_treino(self):
        """Testa que perícia que requer treino sem treino retorna 0"""
        pericia_treino = Pericia.objects.create(nome="gue", requer_treino=True)
        pt = PericiaTreinada.objects.create(
            ficha=self.ficha, pericia=pericia_treino, treinado=False
        )
        pt.atributo_chave.add(self.atributo_ficha)

        valor = pt.calcularValor()
        self.assertEqual(valor, 0)

    def test_adicionar_bonus(self):
        """Testa adicionar bônus adicional"""
        valor_base = self.pericia_treinada.calcularValor()
        valor_com_bonus = self.pericia_treinada.adicionarBonus(5)
        self.assertEqual(valor_com_bonus, valor_base + 5)


class NivelClasseFichaModelTest(TestCase):
    """Testes para o model NivelClasseFicha"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Teste", dono=self.user)
        self.classe = Classe.objects.create(
            nome="Guerreiro", proficiencia="Armas", vida_base=20, vida_por_nivel=5
        )
        self.nivel_classe = NivelClasseFicha.objects.create(
            ficha=self.ficha, classe=self.classe, nivel=5
        )

    def test_criacao_nivel_classe(self):
        """Testa criação de nível de classe"""
        self.assertEqual(self.nivel_classe.nivel, 5)
        self.assertEqual(self.nivel_classe.classe, self.classe)

    def test_str_nivel_classe(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.nivel_classe), "Teste")

    def test_multiclasse(self):
        """Testa personagem com múltiplas classes"""
        classe2 = Classe.objects.create(
            nome="Ladino", proficiencia="Armas leves", vida_base=16, vida_por_nivel=4
        )

        NivelClasseFicha.objects.create(ficha=self.ficha, classe=classe2, nivel=3)

        self.assertEqual(self.ficha.nivelclasseficha_set.count(), 2)
