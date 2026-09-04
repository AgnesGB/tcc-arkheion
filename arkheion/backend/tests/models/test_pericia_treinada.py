# As especificações dos casos de teste para o modelo PericiaTreinada estão no arquivo 'CT-CDU014.md'
# na pasta de documentação "/workspaces/Arkheion/doc/testes/CT-CDU014.md"
# e "/workspaces/Arkheion/doc/testes/detalhamento-testes/Detalhamento_CT-CDU014.md".

from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import Pericia, PericiaTreinada, Ficha, Atributo, AtributoFicha


class PericiaTreinadaModelTest(TestCase):
    """
    Suite de testes unitários para o modelo PericiaTreinada, baseado nos casos de teste
    especificados em CT-CDU014.md.

    Testa o cálculo de valores de perícia considerando:
    - Nível do personagem
    - Modificador de atributo
    - Bônus de treinamento
    - Bônus adicional
    - Perícias que requerem treinamento obrigatório
    """

    def setUp(self):
        """
        Configuração inicial executada antes de cada teste.
        Cria os objetos necessários para os testes.
        """
        # Cria um usuário para ser dono da ficha
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Cria os atributos necessários
        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_destreza = Atributo.objects.create(nome="des", ordem=2)
        self.atributo_sabedoria = Atributo.objects.create(nome="sab", ordem=5)

        # Cria as perícias
        self.pericia_atletismo = Pericia.objects.create(
            nome="atl", requer_treino=False  # Atletismo
        )
        self.pericia_ladinagem = Pericia.objects.create(
            nome="lad", requer_treino=True  # Ladinagem
        )
        self.pericia_percepcao = Pericia.objects.create(
            nome="per", requer_treino=False  # Percepção
        )

        # Cria fichas de teste (serão usadas nos testes específicos)
        self.ficha_nivel_10 = Ficha.objects.create(
            dono=self.user, nome="Guerreiro Nível 10", nivel=10
        )

        self.ficha_nivel_4 = Ficha.objects.create(
            dono=self.user, nome="Ladino Nível 4", nivel=4
        )

        self.ficha_nivel_8 = Ficha.objects.create(
            dono=self.user, nome="Rastreador Nível 8", nivel=8
        )

    def tearDown(self):
        """
        Limpeza executada após cada teste.
        (Django já faz rollback automático, mas mantido por padrão)
        """
        PericiaTreinada.objects.all().delete()
        AtributoFicha.objects.all().delete()
        Ficha.objects.all().delete()
        Pericia.objects.all().delete()
        Atributo.objects.all().delete()
        User.objects.all().delete()

    # --- CT-PER-01: Cálculo de perícia comum ---
    def test_CT_PER_01_calculo_pericia_comum(self):
        """
        CT-PER-01: Verifica o cálculo base de uma perícia que não exige treinamento.

        Cenário: Atletismo (não requer treino), Personagem nível 10, Força 14 (+2 mod)
        Esperado: valor_calculado = 7 (5 de nível + 2 de atributo)
        """
        # Cria o atributo Força com modificador +2 (valor = 2)
        atributo_forca_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca,
            ficha=self.ficha_nivel_10,
            valor=2,  # Modificador de Força 14 = +2
        )

        # Cria a perícia treinada
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_10,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_forca_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            7,
            "CT-PER-01: O valor calculado para Atletismo (nível 10, For +2, sem treino) "
            "deveria ser 7 (5 de nível + 2 de atributo).",
        )

    # --- CT-PER-02: Treino, não obrigatório, de perícia ---
    def test_CT_PER_02_treino_nao_obrigatorio(self):
        """
        CT-PER-02: Testa o bônus de treino em uma perícia comum.

        Cenário: Atletismo (não requer treino), Personagem nível 10, Força 14 (+2 mod), Treinado
        Esperado: valor_calculado = 11 (5 de nível + 2 de atributo + 4 de bônus de treino)
        """
        # Cria o atributo Força com modificador +2
        atributo_forca_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha_nivel_10, valor=2
        )

        # Cria a perícia treinada com treino marcado
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_10,
            pericia=self.pericia_atletismo,
            treinado=True,  # Marca como treinado
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_forca_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        # Nível 10 está entre 6 e 14, então bônus de treino = 4
        self.assertEqual(
            valor_calculado,
            11,
            "CT-PER-02: O valor calculado para Atletismo (nível 10, For +2, treinado) "
            "deveria ser 11 (5 de nível + 2 de atributo + 4 de bônus de treino).",
        )

    # --- CT-PER-03: Cálculo de perícia obrigatória ---
    def test_CT_PER_03_calculo_pericia_obrigatoria(self):
        """
        CT-PER-03: Verifica o cálculo de uma perícia que exige treinamento e está treinada.

        Cenário: Ladinagem (requer treino), Personagem nível 4, Destreza 16 (+3 mod), Treinado
        Esperado: valor_calculado = 7 (2 de nível + 3 de atributo + 2 de bônus de treino)
        """
        # Cria o atributo Destreza com modificador +3
        atributo_destreza_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_destreza,
            ficha=self.ficha_nivel_4,
            valor=3,  # Modificador de Destreza 16 = +3
        )

        # Cria a perícia treinada
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_4,
            pericia=self.pericia_ladinagem,
            treinado=True,  # Treinado (obrigatório para Ladinagem)
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_destreza_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        # Nível 4 está entre 0 e 5, então bônus de treino = 2
        self.assertEqual(
            valor_calculado,
            7,
            "CT-PER-03: O valor calculado para Ladinagem (nível 4, Des +3, treinado) "
            "deveria ser 7 (2 de nível + 3 de atributo + 2 de bônus de treino).",
        )

    # --- CT-PER-04: Uso de perícia obrigatória sem treino (CI1) ---
    def test_CT_PER_04_pericia_obrigatoria_sem_treino(self):
        """
        CT-PER-04: Garante que o valor da perícia é zerado quando não treinada (mas requer treino).

        Cenário: Ladinagem (requer treino), Personagem nível 4, Destreza 16 (+3 mod), NÃO Treinado
        Esperado: valor_calculado = 0 (todos os bônus ignorados)
        """
        # Cria o atributo Destreza com modificador +3
        atributo_destreza_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_destreza, ficha=self.ficha_nivel_4, valor=3
        )

        # Cria a perícia NÃO treinada
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_4,
            pericia=self.pericia_ladinagem,
            treinado=False,  # NÃO treinado
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_destreza_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            0,
            "CT-PER-04: O valor calculado para Ladinagem (requer treino, mas não treinado) "
            "deveria ser 0, ignorando todos os outros bônus.",
        )

    # --- CT-PER-05: Inserir bônus adicional válido ---
    def test_CT_PER_05_bonus_adicional_positivo(self):
        """
        CT-PER-05: Testa a adição de um bônus positivo.

        Cenário: Percepção (não requer treino), Personagem nível 8, Sabedoria 12 (+1 mod),
                 Bônus adicional +5
        Esperado: valor_calculado = 10 (4 de nível + 1 de atributo + 5 de bônus)
        """
        # Cria o atributo Sabedoria com modificador +1
        atributo_sabedoria_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_sabedoria,
            ficha=self.ficha_nivel_8,
            valor=1,  # Modificador de Sabedoria 12 = +1
        )

        # Cria a perícia sem treino, mas com bônus adicional
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=5,  # Bônus adicional positivo
        )
        pericia_treinada.atributo_chave.add(atributo_sabedoria_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            10,
            "CT-PER-05: O valor calculado para Percepção (nível 8, Sab +1, bônus +5) "
            "deveria ser 10 (4 de nível + 1 de atributo + 5 de bônus).",
        )

    # --- CT-PER-06: Inserir bônus adicional negativo ---
    def test_CT_PER_06_bonus_adicional_negativo(self):
        """
        CT-PER-06: Testa a aplicação de uma penalidade (bônus negativo).

        Cenário: Percepção (não requer treino), Personagem nível 8, Sabedoria 12 (+1 mod),
                 Bônus adicional -2
        Esperado: valor_calculado = 3 (4 de nível + 1 de atributo - 2 de penalidade)
        """
        # Cria o atributo Sabedoria com modificador +1
        atributo_sabedoria_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_sabedoria, ficha=self.ficha_nivel_8, valor=1
        )

        # Cria a perícia sem treino, mas com bônus negativo (penalidade)
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=-2,  # Penalidade
        )
        pericia_treinada.atributo_chave.add(atributo_sabedoria_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            3,
            "CT-PER-06: O valor calculado para Percepção (nível 8, Sab +1, penalidade -2) "
            "deveria ser 3 (4 de nível + 1 de atributo - 2 de penalidade).",
        )

    # --- CT-PER-07: Deixar bônus adicional vazio ---
    def test_CT_PER_07_bonus_adicional_zero_default(self):
        """
        CT-PER-07: Testa o comportamento quando o bônus adicional é 0 (valor padrão).

        Cenário: Percepção (não requer treino), Personagem nível 8, Sabedoria 12 (+1 mod),
                 Bônus adicional = 0 (padrão)
        Esperado: valor_calculado = 5 (4 de nível + 1 de atributo)
        """
        # Cria o atributo Sabedoria com modificador +1
        atributo_sabedoria_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_sabedoria, ficha=self.ficha_nivel_8, valor=1
        )

        # Cria a perícia sem especificar bonus_adicional (usa default = 0)
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            # bonus_adicional não especificado, usa default = 0
        )
        pericia_treinada.atributo_chave.add(atributo_sabedoria_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            5,
            "CT-PER-07: O valor calculado para Percepção (nível 8, Sab +1, sem bônus) "
            "deveria ser 5 (4 de nível + 1 de atributo).",
        )

    # --- CT-PER-08: Inserir bônus adicional inválido (CV5) ---
    def test_CT_PER_08_bonus_adicional_invalido_tratado_como_zero(self):
        """
        CT-PER-08: Testa o tratamento de valores inválidos no bônus adicional.

        Nota: Este teste valida o comportamento do MODEL. No contexto do modelo Django,
        o campo bonus_adicional é um IntegerField, então valores não-numéricos causariam
        erro na validação/salvamento. Este teste simula o comportamento esperado quando
        o frontend trata entradas inválidas como 0 antes de enviar ao backend.

        Cenário: Percepção (não requer treino), Personagem nível 8, Sabedoria 12 (+1 mod),
                 Bônus adicional inválido tratado como 0
        Esperado: valor_calculado = 5 (4 de nível + 1 de atributo + 0)
        """
        # Cria o atributo Sabedoria com modificador +1
        atributo_sabedoria_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_sabedoria, ficha=self.ficha_nivel_8, valor=1
        )

        # Simula o comportamento esperado: entrada inválida é tratada como 0
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=0,  # Entrada inválida tratada como 0
        )
        pericia_treinada.atributo_chave.add(atributo_sabedoria_ficha)

        # Calcula o valor
        valor_calculado = pericia_treinada.calcularValor()

        # Validação
        self.assertEqual(
            valor_calculado,
            5,
            "CT-PER-08: O valor calculado para Percepção com entrada inválida "
            "(tratada como 0) deveria ser 5 (4 de nível + 1 de atributo).",
        )

    # --- Testes Adicionais de Validação do Bônus de Treino ---

    def test_bonus_treino_nivel_0_a_5(self):
        """
        Testa se o bônus de treino é 2 para níveis de 0 a 5.
        """
        ficha_nivel_3 = Ficha.objects.create(
            dono=self.user, nome="Teste Nível 3", nivel=3
        )
        atributo_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=ficha_nivel_3, valor=2
        )

        pericia_treinada = PericiaTreinada.objects.create(
            ficha=ficha_nivel_3,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_ficha)

        bonus_treino = pericia_treinada.verificarTreino()
        self.assertEqual(bonus_treino, 2, "Bônus de treino para nível 3 deveria ser 2.")

    def test_bonus_treino_nivel_6_a_14(self):
        """
        Testa se o bônus de treino é 4 para níveis de 6 a 14.
        """
        atributo_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha_nivel_10, valor=2
        )

        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_10,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_ficha)

        bonus_treino = pericia_treinada.verificarTreino()
        self.assertEqual(
            bonus_treino, 4, "Bônus de treino para nível 10 deveria ser 4."
        )

    def test_bonus_treino_nivel_15_ou_mais(self):
        """
        Testa se o bônus de treino é 6 para níveis 15 ou superiores.
        """
        ficha_nivel_20 = Ficha.objects.create(
            dono=self.user, nome="Teste Nível 20", nivel=20
        )
        atributo_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=ficha_nivel_20, valor=2
        )

        pericia_treinada = PericiaTreinada.objects.create(
            ficha=ficha_nivel_20,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_ficha)

        bonus_treino = pericia_treinada.verificarTreino()
        self.assertEqual(
            bonus_treino, 6, "Bônus de treino para nível 20 deveria ser 6."
        )

    def test_bonus_treino_nao_treinado(self):
        """
        Testa se o bônus de treino é 0 quando não treinado.
        """
        atributo_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha_nivel_10, valor=2
        )

        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_10,
            pericia=self.pericia_atletismo,
            treinado=False,  # Não treinado
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_ficha)

        bonus_treino = pericia_treinada.verificarTreino()
        self.assertEqual(
            bonus_treino, 0, "Bônus de treino deveria ser 0 quando não treinado."
        )

    # --- Teste de Edge Cases ---

    def test_calculo_sem_ficha_associada(self):
        """
        Testa se calcularValor() retorna 0 quando não há ficha associada.
        """
        pericia_sem_ficha = PericiaTreinada.objects.create(
            ficha=None,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )

        valor_calculado = pericia_sem_ficha.calcularValor()
        self.assertEqual(
            valor_calculado,
            0,
            "calcularValor() deveria retornar 0 quando não há ficha associada.",
        )

    def test_calculo_com_multiplos_atributos(self):
        """
        Testa o cálculo quando múltiplos atributos estão associados à perícia.
        """
        atributo_forca_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha_nivel_10, valor=2
        )

        atributo_destreza_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_destreza, ficha=self.ficha_nivel_10, valor=3
        )

        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_10,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )
        # Adiciona múltiplos atributos
        pericia_treinada.atributo_chave.add(
            atributo_forca_ficha, atributo_destreza_ficha
        )

        valor_calculado = pericia_treinada.calcularValor()

        # nível 10 // 2 = 5, atributos = 2 + 3 = 5, total = 10
        self.assertEqual(
            valor_calculado,
            10,
            "calcularValor() deveria somar todos os atributos associados.",
        )

    def test_adicionar_bonus_temporario(self):
        """
        Testa o método adicionarBonus() que adiciona um bônus temporário
        ao valor calculado da perícia sem modificar o bonus_adicional persistente.

        Cenário: Atletismo (nível 4, For +3, treinado, bonus_adicional=0)
                 + bônus temporário de +5
        Esperado: retorna valor calculado (7) + bônus temporário (5) = 12
        """
        # Cria o atributo Força com modificador +3
        atributo_forca_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha_nivel_4, valor=3  # nivel 4
        )

        # Cria a perícia treinada
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_nivel_4,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia_treinada.atributo_chave.add(atributo_forca_ficha)

        # Calcula o valor base
        valor_base = pericia_treinada.calcularValor()
        # nivel 4 // 2 = 2, atributo = 3, bonus treino (nivel 4) = 2
        # 2 + 3 + 2 = 7
        self.assertEqual(valor_base, 7)

        # Adiciona bônus temporário de +5
        valor_com_bonus_temporario = pericia_treinada.adicionarBonus(5)
        self.assertEqual(
            valor_com_bonus_temporario,
            12,
            "O método adicionarBonus(5) deveria retornar 12 (7 + 5).",
        )

        # Verifica que o bonus_adicional persistente não foi modificado
        self.assertEqual(
            pericia_treinada.bonus_adicional,
            0,
            "O bonus_adicional persistente não deveria ter sido alterado.",
        )

        # Testa com bônus negativo (penalidade temporária)
        valor_com_penalidade = pericia_treinada.adicionarBonus(-3)
        self.assertEqual(
            valor_com_penalidade,
            4,
            "O método adicionarBonus(-3) deveria retornar 4 (7 - 3).",
        )
