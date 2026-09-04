# As especificações dos casos de teste para o modelo Pericia estão no arquivo 'CT-CDU014.md' na pasta de documentação "/workspaces/Arkheion/doc/testes/CT-CDU014.md" e "/workspaces/Arkheion/doc/testes/detalhamento-testes/Detalhamento_CT-CDU014.md".

# --- Validar os testes apontados aqui com o arquivo de especificações mencionado acima. ---

from django.test import TestCase
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from backend.models import Pericia


class PericiaModelTest(TestCase):
    # Suite de testes unitários para o modelo Pericia, o qual testa as condições de sucesso e falha da entidade.
    # Método 'setUp' chamado automaticamente antes de cada método de testes. (alocação de recursos, inicialização de objetos)
    def setUp(self):
        self.pericia_atletismo = Pericia.objects.create(
            nome="atl", requer_treino=False  # Atletismo
        )
        self.pericia_ladinagem = Pericia.objects.create(
            nome="lad", requer_treino=True  # Ladinagem
        )

    # Método 'tearDown' chamado automaticamente ao final de cada método de testes (liberação de recursos)
    def tearDown(self):
        """
        (Nota: O TestCase do Django já faz o rollback do banco de dados
        automaticamente, mas este método foi mantido conforme solicitado em tarefa).
        """
        Pericia.objects.all().delete()

    # --- Testes de Sucesso ---
    def test_criacao_sucesso_pericia(self):
        """
        Testa a criação bem-sucedida de uma perícia e a verificação
        de seus atributos.
        """
        msg_erro = "O valor recuperado do banco de dados não corresponde ao esperado."

        # Recupera os objetos criados no setUp
        atletismo = Pericia.objects.get(nome="atl")
        ladinagem = Pericia.objects.get(nome="lad")

        # Assertions com mensagens significativas
        self.assertEqual(atletismo.nome, "atl", msg_erro)
        self.assertFalse(
            atletismo.requer_treino,
            "O valor de 'requer_treino' para Atletismo deveria ser False.",
        )
        self.assertEqual(ladinagem.nome, "lad", msg_erro)
        self.assertTrue(
            ladinagem.requer_treino,
            "O valor de 'requer_treino' para Ladinagem deveria ser True.",
        )

    def test_default_requer_treino(self):
        # Testa se o campo 'requer_treino' assume 'False' por padrão, conforme definido no models.py.
        # Cria uma perícia sem especificar 'requer_treino'
        pericia_cura = Pericia.objects.create(nome="cur")  # Cura

        self.assertFalse(
            pericia_cura.requer_treino,
            "O campo 'requer_treino' deveria ser 'False' por padrão.",
        )

    def test_str_method(self):
        # Testa se o método __str__ retorna o nome de exibição (get_nome_display) corretamente, conforme definido no models.py.
        atletismo = self.pericia_atletismo
        ladinagem = self.pericia_ladinagem

        # O método get_nome_display() busca o valor legível das 'choices'
        self.assertEqual(
            str(atletismo),
            "Atletismo",
            "O método __str__ não retornou 'Atletismo' para 'atl'.",
        )
        self.assertEqual(
            str(ladinagem),
            "Ladinagem",
            "O método __str__ não retornou 'Ladinagem' para 'lad'.",
        )

    # --- Testes de Falha (capturando exceções) ---

    def test_falha_nome_nulo(self):
        """
        Testa se um IntegrityError é levantado ao tentar criar uma
        perícia com 'nome' nulo (NOT NULL constraint).
        """
        try:
            # Tenta criar uma perícia com nome=None
            # Envolve a operação que vai falhar em um bloco atômico
            with transaction.atomic():
                Pericia.objects.create(nome=None, requer_treino=False)

            # Se a linha acima não levantar a exceção, o teste deve falhar
            self.fail(
                "A exceção IntegrityError não foi levantada, mas era esperada "
                "ao criar uma Pericia com nome=None."
            )
        except IntegrityError:
            # Sucesso, a exceção esperada foi capturada.
            pass
        except Exception as e:
            # Falha se uma exceção diferente de IntegrityError for levantada
            self.fail(f"Uma exceção inesperada foi levantada: {type(e).__name__} ({e})")

    def test_falha_nome_fora_das_choices(self):
        # Testa se um ValidationError é levantado ao usar um 'nome' que não está na lista de 'choices' do modelo.
        try:
            # Cria a instância, mas não salva
            pericia_invalida = Pericia(nome="xyz", requer_treino=False)

            # Força a execução dos validadores do modelo (incluindo 'choices')
            pericia_invalida.full_clean()

            # Se full_clean() não levantar a exceção, o teste deve falhar
            self.fail(
                "A exceção ValidationError não foi levantada, mas era esperada "
                "para um 'nome' que não está nas 'choices'."
            )
        except ValidationError as e:
            # Sucesso, a exceção foi capturada. É verificado se o erro foi especificamente no campo 'nome'
            self.assertIn(
                "nome",
                e.message_dict,
                "A chave 'nome' não está no dicionário de erros de validação.",
            )
        except Exception as e:
            # Falha se outra exceção for levantada
            self.fail(f"Uma exceção inesperada foi levantada: {type(e).__name__} ({e})")

    def test_falha_nome_excede_max_length(self):
        # Testa se um ValidationError é levantado se 'nome' excede o max_length definido no modelo (max_length=3).
        try:
            # Tenta criar uma instância com nome='abcde'
            pericia_longa = Pericia(nome="abcde", requer_treino=False)

            # Força a execução dos validadores (incluindo 'max_length')
            pericia_longa.full_clean()

            # Se full_clean() não levantar a exceção, o teste deve falhar
            self.fail(
                "A exceção ValidationError não foi levantada, mas era esperada "
                "para um 'nome' que excede max_length=3."
            )
        except ValidationError as e:
            # Sucesso, a exceção foi capturada.
            self.assertIn(
                "nome",
                e.message_dict,
                "A chave 'nome' não está no dicionário de erros de validação.",
            )
        except Exception as e:
            # Falha se outra exceção for levantada
            self.fail(f"Uma exceção inesperada foi levantada: {type(e).__name__} ({e})")

    def test_falha_nome_vazio(self):
        """
        Testa se um ValidationError é levantado ao tentar criar uma
        perícia com nome vazio.
        """
        try:
            pericia_vazia = Pericia(nome="", requer_treino=False)
            pericia_vazia.full_clean()

            self.fail(
                "A exceção ValidationError não foi levantada, mas era esperada "
                "para um 'nome' vazio."
            )
        except ValidationError as e:
            self.assertIn(
                "nome",
                e.message_dict,
                "A chave 'nome' não está no dicionário de erros de validação.",
            )
        except Exception as e:
            self.fail(f"Uma exceção inesperada foi levantada: {type(e).__name__} ({e})")

    # --- Testes adicionais de validação ---

    def test_todas_pericias_choices_validas(self):
        """
        Testa se todas as perícias definidas nas choices podem ser criadas
        e retornam o display name correto.
        """
        pericias_choices = [
            ("acr", "Acrobacia"),
            ("ade", "Adestramento"),
            ("atl", "Atletismo"),
            ("atu", "Atuação"),
            ("cav", "Cavalgar"),
            ("con", "Conhecimento"),
            ("cur", "Cura"),
            ("dip", "Diplomacia"),
            ("eng", "Enganação"),
            ("for", "Fortitude"),
            ("fur", "Furtividade"),
            ("gue", "Guerra"),
            ("ini", "Iniciativa"),
            ("int", "Intimidação"),
            ("inu", "Intuição"),
            ("inv", "Investigação"),
            ("jog", "Jogatina"),
            ("lad", "Ladinagem"),
            ("lut", "Luta"),
            ("mis", "Misticismo"),
            ("nob", "Nobreza"),
            ("ofi", "Ofício"),
            ("per", "Percepção"),
            ("pil", "Pilotagem"),
            ("pon", "Pontaria"),
            ("ref", "Reflexos"),
            ("rel", "Religião"),
            ("sob", "Sobrevivência"),
            ("von", "Vontade"),
        ]

        for codigo, nome_completo in pericias_choices:
            with self.subTest(codigo=codigo):
                pericia = Pericia.objects.create(nome=codigo, requer_treino=False)
                self.assertEqual(pericia.nome, codigo)
                self.assertEqual(str(pericia), nome_completo)
                self.assertEqual(pericia.get_nome_display(), nome_completo)

    def test_duplicidade_pericias_permitida(self):
        """
        Testa se o modelo permite criar múltiplas instâncias da mesma perícia.
        Nota: O modelo atualmente não possui constraint de unicidade.
        """
        # Cria a primeira instância
        pericia1 = Pericia.objects.create(nome="atl", requer_treino=False)

        # Tenta criar uma segunda instância com o mesmo nome
        # Isso deve ser permitido pois não há constraint UNIQUE
        pericia2 = Pericia.objects.create(nome="atl", requer_treino=True)

        # Verifica que ambas existem
        self.assertNotEqual(pericia1.pk, pericia2.pk)
        self.assertEqual(
            Pericia.objects.filter(nome="atl").count(), 3
        )  # setUp criou 1 instância e depois foi criada outra

    def test_verbose_name_campo_nome(self):
        # Testa se o campo 'nome' possui o verbose_name correto.
        campo_nome = Pericia._meta.get_field("nome")
        self.assertEqual(campo_nome.verbose_name, "Perícia")

    def test_verbose_name_campo_requer_treino(self):
        # Testa se o campo 'requer_treino' possui o verbose_name correto.
        campo_requer_treino = Pericia._meta.get_field("requer_treino")
        self.assertEqual(campo_requer_treino.verbose_name, "Requer treino?")

    def test_max_length_campo_nome(self):
        # Testa se o campo 'nome' possui max_length=3 conforme esperado.
        campo_nome = Pericia._meta.get_field("nome")
        self.assertEqual(campo_nome.max_length, 3)

    def test_alteracao_requer_treino(self):
        # Testa se é possível alterar o valor de 'requer_treino' após a criação.
        pericia = Pericia.objects.create(nome="acr", requer_treino=False)
        self.assertFalse(pericia.requer_treino)

        # Altera o valor
        pericia.requer_treino = True
        pericia.save()

        # Recupera do banco e verifica
        pericia_atualizada = Pericia.objects.get(pk=pericia.pk)
        self.assertTrue(pericia_atualizada.requer_treino)
