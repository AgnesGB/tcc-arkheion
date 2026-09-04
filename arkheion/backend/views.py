from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q


from .models import (
    Ficha,
    Pericia,
    Atributo,
    PericiaTreinada,
    AtributoFicha,
    Ataque,
    Classe,
    NivelClasseFicha,
    Origem,
    Raca,
    Habilidade,
    Divindade,
)
from .serializers import (
    UserSerializer,
    FichaSerializer,
    PericiaTreinadaSerializer,
    AtributoFichaSerializer,
    RacaSerializer,
    OrigemSerializer,
    ClasseSerializer,
    AtributoSerializer,
    PericiaSerializer,
    DivindadeSerializer,
    HabilidadeSerializer,
    AtaqueSerializer,
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
)
from .filters import FichaFilter, AtaqueFilter, HabilidadeFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AtaqueViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar, criar e gerenciar ataques.
    """

    queryset = Ataque.objects.all()
    serializer_class = AtaqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = AtaqueFilter
    search_fields = ["nome", "descricao"]
    ordering_fields = ["nome"]
    ordering = ["nome"]

    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # Garante que o usuário só veja os itens oficiais (None) ou os criados por ele mesmo
        queryset = self.queryset.filter(Q(dono=user) | Q(dono=None))

        # Filtra por homebrew se o parâmetro estiver presente na requisição
        homebrew = self.request.query_params.get("homebrew", None)
        if homebrew is not None:
            queryset = queryset.filter(homebrew=homebrew.lower() == "true")

        return queryset


class HabilidadeViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar, criar e gerenciar habilidades.
    """

    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = HabilidadeFilter
    search_fields = ["nome", "descricao"]
    ordering_fields = ["nome", "nivel_habilidade"]
    ordering = ["nome"]

    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # Garante que o usuário só veja os itens oficiais (None) ou os criados por ele mesmo
        queryset = self.queryset.filter(Q(dono=user) | Q(dono=None))

        # Filtra por homebrew se o parâmetro estiver presente na requisição
        homebrew = self.request.query_params.get("homebrew", None)
        if homebrew is not None:
            queryset = queryset.filter(homebrew=homebrew.lower() == "true")

        return queryset


class FichaViewSet(viewsets.ModelViewSet):
    # Otimizando a queryset para carregar todos os dados relacionados de uma vez
    # Usamos select_related para ForeignKeys e prefetch_related para ManyToMany e ForeignKeys reversas
    queryset = (
        Ficha.objects.all()
        .select_related(
            "dono",  # Usuário dono da ficha
            "divindade",  # A divindade associada à ficha
        )
        .prefetch_related(
            "racas",  # Relação ManyToMany com Raca
            "origens",  # Relação ManyToMany com Origem
            "habilidades",  # Relação ManyToMany com Habilidade
            "ataques",  # Relação ManyToMany com Ataque
            # Para os modelos 'through' (intermediários), precisamos ir um nível mais fundo
            # 'atributoficha_set' é o related_name padrão para a ForeignKey de Ficha em AtributoFicha
            "atributoficha_set__atributo",  # Carrega AtributoFicha e o Atributo relacionado
            # 'periciatreinada_set' é o related_name padrão para a ForeignKey de Ficha em PericiaTreinada
            "periciatreinada_set__pericia",  # Carrega PericiaTreinada e a Pericia relacionada
            "periciatreinada_set__atributo_chave__atributo",  # Para o ManyToMany 'atributo_chave' dentro de PericiaTreinada, e o Atributo dentro dele
            # 'nivelclasseficha_set' é o related_name padrão para a ForeignKey de Ficha em NivelClasseFicha
            "nivelclasseficha_set__classe",  # Carrega NivelClasseFicha e a Classe relacionada
        )
    )
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = FichaFilter
    search_fields = ["nome", "racas__nome", "origens__nome", "classes__nome"]
    ordering_fields = ["nome", "nivel"]
    ordering = ["nome"]

    def get_queryset(self):
        # Filtra as fichas pelo usuário logado
        if self.request.user.is_authenticated:
            # Retorna a queryset otimizada, filtrada pelo dono
            return self.queryset.filter(dono=self.request.user)
        # Se o usuário não estiver autenticado, retorna uma queryset vazia para segurança
        return Ficha.objects.none()

    @action(detail=False, methods=["get"], url_path="busca-avancada")
    def busca_avancada(self, request):
        """
        Endpoint para busca avançada de fichas.
        Permite filtrar por nome, nível, classe, raça, origem e divindade.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Paginação se necessário
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="update-resources")
    def update_resources(self, request, pk=None):
        ficha = (
            self.get_object()
        )  # Obtém a ficha do usuário autenticado (graças ao get_queryset)
        data = request.data

        # Validar dados antes de atualizar é uma boa prática para garantir que os valores são inteiros, etc.
        # Por simplicidade, vamos apenas tentar converter para int e usar o valor atual como fallback
        vida_atual = data.get("vida_atual")
        mana_atual = data.get("mana_atual")

        if vida_atual is not None:
            try:
                ficha.vida_atual = int(vida_atual)
            except (ValueError, TypeError):
                return Response(
                    {"detail": "Vida atual deve ser um número inteiro."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if mana_atual is not None:
            try:
                ficha.mana_atual = int(mana_atual)
            except (ValueError, TypeError):
                return Response(
                    {"detail": "Mana atual deve ser um número inteiro."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        ficha.save()
        # Retorna a ficha atualizada com o serializer completo
        return Response(self.get_serializer(ficha).data)

    @action(detail=True, methods=["post"], url_path="update-stats")
    def update_stats(self, request, pk=None):
        ficha = self.get_object()  # Obtém a ficha do usuário autenticado
        # Lista de campos que esta ação pode atualizar
        fields_to_update = ["ca", "cd", "deslocamento", "tamanho"]
        updated = False  # Flag para verificar se alguma atualização ocorreu

        for field in fields_to_update:
            if field in request.data:
                # Usa setattr para atualizar o campo do objeto Ficha dinamicamente
                setattr(ficha, field, request.data[field])
                updated = True

        if updated:
            ficha.save()
            # Retorna a ficha atualizada com o serializer completo
            return Response(self.get_serializer(ficha).data)

        # Se nenhum campo válido para atualização foi fornecido, retorna um erro
        return Response(
            {
                "detail": "Nenhum campo válido para atualização (CA, CD, Deslocamento, Tamanho) fornecido."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post"], url_path="update-pericia-bonus")
    def update_pericia_bonus(self, request, pk=None):
        ficha = self.get_object()  # Obtém a ficha do usuário autenticado
        pericia_id = request.data.get("pericia_id")
        bonus_adicional = request.data.get("bonus_adicional")

        if not pericia_id or bonus_adicional is None:
            return Response(
                {"detail": "pericia_id e bonus_adicional são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca a instância de PericiaTreinada para a ficha e perícia fornecidas
        # Use get_object_or_404 para retornar 404 se não encontrar
        pericia_treinada = get_object_or_404(
            PericiaTreinada, ficha=ficha, pericia__id=pericia_id
        )

        try:
            # Converte o bônus adicional para inteiro
            pericia_treinada.bonus_adicional = int(bonus_adicional)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Bônus adicional deve ser um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pericia_treinada.save()

        # Recalcula e retorna o valor da perícia atualizado
        # Usamos PericiaTreinadaSerializer para serializar apenas a perícia treinada atualizada
        serializer = PericiaTreinadaSerializer(pericia_treinada)
        return Response(
            {
                "status": "success",
                "valor": pericia_treinada.calcularValor(),  # Retorna o valor calculado
                "data": serializer.data,  # Retorna os dados completos da perícia treinada
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="update-pericia-atributo")
    def update_pericia_atributo(self, request, pk=None):
        ficha = self.get_object()  # Obtém a ficha do usuário autenticado
        pericia_id = request.data.get("pericia_id")
        atributo_id = request.data.get("atributo_id")  # Recebe o ID do AtributoFicha

        if not pericia_id or not atributo_id:
            return Response(
                {"detail": "pericia_id e atributo_id são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca a instância de PericiaTreinada para a ficha e perícia fornecidas
        pericia_treinada = get_object_or_404(
            PericiaTreinada, ficha=ficha, pericia__id=pericia_id
        )

        # Busca diretamente o AtributoFicha pelo ID recebido
        atributo_ficha_obj = get_object_or_404(
            AtributoFicha, id=atributo_id, ficha=ficha
        )

        # Atualiza o ManyToManyField 'atributo_chave'. Como é um M2M, set() espera uma lista.
        # Definimos que 'atributo_chave' terá apenas o atributo_ficha_obj fornecido.
        pericia_treinada.atributo_chave.set([atributo_ficha_obj])
        pericia_treinada.save()

        # Força recálculo do valor após a atualização
        valor_calculado = pericia_treinada.calcularValor()

        serializer = PericiaTreinadaSerializer(pericia_treinada)
        return Response(
            {
                "status": "success",
                "valor_calculado": valor_calculado,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="update-pericia-treino")
    def update_pericia_treino(self, request, pk=None):
        ficha = self.get_object()  # Obtém a ficha do usuário autenticado
        pericia_id = request.data.get("pericia_id")
        treinado = request.data.get("treinado")

        if not pericia_id or treinado is None:
            return Response(
                {"detail": "pericia_id e treinado são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pericia_treinada = get_object_or_404(
            PericiaTreinada, ficha=ficha, pericia__id=pericia_id
        )

        # O valor 'treinado' pode vir como string ('true', 'false') do JS, então converta para booleano
        if isinstance(treinado, str):
            treinado = treinado.lower() == "true"

        pericia_treinada.treinado = treinado
        pericia_treinada.save()

        serializer = PericiaTreinadaSerializer(pericia_treinada)
        return Response(
            {
                "status": "success",
                "valor": pericia_treinada.calcularValor(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="update-atributo")
    def update_atributo(self, request, pk=None):
        """
        Atualiza o valor de um atributo específico da ficha.
        """
        ficha = self.get_object()
        atributo_ficha_id = request.data.get("atributo_ficha_id")
        valor = request.data.get("valor")

        if not atributo_ficha_id or valor is None:
            return Response(
                {"detail": "atributo_ficha_id e valor são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca o AtributoFicha específico desta ficha
        atributo_ficha = get_object_or_404(
            AtributoFicha, id=atributo_ficha_id, ficha=ficha
        )

        # Atualiza o valor
        atributo_ficha.valor = int(valor)
        atributo_ficha.save()

        # Retorna o atributo atualizado
        serializer = AtributoFichaSerializer(atributo_ficha)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get"], url_path="ataques-filtrados")
    def ataques_filtrados(self, request, pk=None):
        """
        Endpoint para filtrar ataques da ficha.
        Permite filtrar por nome e homebrew.
        """
        ficha = self.get_object()

        # Obtém ataques da ficha
        ataques = ficha.ataques.all()

        # Filtragem por nome
        nome = request.query_params.get("nome", None)
        if nome:
            ataques = ataques.filter(nome__icontains=nome)

        # Filtragem por homebrew
        incluir_homebrew = request.query_params.get("homebrew", "false")
        if incluir_homebrew.lower() != "true":
            ataques = ataques.filter(homebrew=False)

        serializer = AtaqueSerializer(ataques, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="habilidades-filtradas")
    def habilidades_filtradas(self, request, pk=None):
        """
        Endpoint para filtrar habilidades da ficha.
        Permite filtrar por nome e homebrew.
        """
        ficha = self.get_object()

        # Obtém habilidades da ficha
        habilidades = ficha.habilidades.all()

        # Filtragem por nome
        nome = request.query_params.get("nome", None)
        if nome:
            habilidades = habilidades.filter(nome__icontains=nome)

        # Filtragem por homebrew
        incluir_homebrew = request.query_params.get("homebrew", "false")
        if incluir_homebrew.lower() != "true":
            habilidades = habilidades.filter(homebrew=False)

        serializer = HabilidadeSerializer(habilidades, many=True)
        return Response(serializer.data)

    # --- Ações para Subir de Nível ---
    # Esta ação simula a lógica de subir de nível para uma ficha.
    @action(detail=True, methods=["post"], url_path="subir-nivel")
    def subir_nivel(self, request, pk=None):
        ficha = self.get_object()

        ficha.subirUmNivel()  # Chama o método do modelo para subir de nível
        ficha.save()

        # Retorna a ficha atualizada para o frontend
        return Response(self.get_serializer(ficha).data, status=status.HTTP_200_OK)

    # Exemplo de ação para setar nível (se necessário para algum caso de uso)
    @action(detail=True, methods=["post"], url_path="setar-nivel")
    def setar_nivel(self, request, pk=None):
        ficha = self.get_object()
        novo_nivel = request.data.get("nivel")

        if novo_nivel is None:
            return Response(
                {"detail": "O campo 'nivel' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            novo_nivel = int(novo_nivel)
            if novo_nivel < 0:
                raise ValueError("Nível não pode ser negativo.")
        except (ValueError, TypeError):
            return Response(
                {"detail": "Nível deve ser um número inteiro positivo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ficha.setarNivel(novo_nivel)  # Chama o método do modelo
        ficha.save()

        return Response(self.get_serializer(ficha).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="criar-ficha")
    def criar_ficha(self, request):
        """
        Action para criar uma nova ficha completa com todos os dados necessários.
        Espera os seguintes dados no request:
        - nome: Nome da ficha
        - nivel: Nível inicial (default: 1)
        - divindade: ID da divindade
        - raca: ID da raça
        - origem: ID da origem
        - classe: ID da classe
        - atributos: Dict com os valores dos atributos (ex: {"for": 10, "des": 12, ...})
        """
        try:
            print(f"DEBUG: Dados recebidos: {request.data}")
            with transaction.atomic():
                # Extrair dados do request
                nome = request.data.get("nome")
                nivel = request.data.get("nivel", 1)
                divindade_id = request.data.get("divindade")
                raca_id = request.data.get("raca")
                origem_id = request.data.get("origem")
                classe_id = request.data.get("classe")
                atributos_data = request.data.get("atributos", {})

            # Validações básicas
            if not nome:
                return Response(
                    {"detail": "O campo 'nome' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not raca_id:
                return Response(
                    {"detail": "O campo 'raca' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not origem_id:
                return Response(
                    {"detail": "O campo 'origem' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not classe_id:
                return Response(
                    {"detail": "O campo 'classe' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Buscar objetos relacionados
            try:
                raca = Raca.objects.get(id=raca_id)
                origem = Origem.objects.get(id=origem_id)
                classe = Classe.objects.get(id=classe_id)
                divindade = None
                if divindade_id:
                    divindade = Divindade.objects.get(id=divindade_id)
            except (
                Raca.DoesNotExist,
                Origem.DoesNotExist,
                Classe.DoesNotExist,
                Divindade.DoesNotExist,
            ) as e:
                return Response(
                    {"detail": f"Objeto não encontrado: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Criar a ficha
            dono = request.user  # Usuário autenticado será sempre o dono

            ficha = Ficha.objects.create(
                nome=nome, nivel=nivel, divindade=divindade, dono=dono
            )

            # Definir relações ManyToMany
            ficha.racas.set([raca])
            ficha.origens.set([origem])

            # Criar NivelClasseFicha
            NivelClasseFicha.objects.create(ficha=ficha, classe=classe, nivel=1)

            # Associar atributos à ficha
            for atributo in Atributo.objects.all():
                # Usar o nome do atributo como chave ou usar um valor padrão
                valor = atributos_data.get(atributo.nome, 0)  # Padrão: 0
                AtributoFicha.objects.create(
                    ficha=ficha, atributo=atributo, valor=int(valor)
                )

            # Mapeamento das perícias para seus atributos-chave
            atributos_por_pericia = {
                "acr": "des",
                "ade": "car",
                "atl": "for",
                "atu": "car",
                "cav": "des",
                "con": "int",
                "cur": "sab",
                "dip": "car",
                "eng": "car",
                "for": "con",
                "fur": "des",
                "gue": "int",
                "ini": "des",
                "int": "car",
                "inu": "sab",
                "inv": "int",
                "jog": "car",
                "lad": "des",
                "lut": "for",
                "mis": "int",
                "nob": "int",
                "ofi": "int",
                "per": "sab",
                "pil": "des",
                "pon": "des",
                "ref": "des",
                "rel": "sab",
                "sob": "sab",
                "von": "sab",
            }

            # Criar perícias treinadas
            for pericia in Pericia.objects.all():
                if pericia.nome in atributos_por_pericia:
                    atributo_nome = atributos_por_pericia[pericia.nome]
                    try:
                        atributo_ch = AtributoFicha.objects.get(
                            ficha=ficha, atributo__nome=atributo_nome
                        )
                        pericia_treinada = PericiaTreinada.objects.create(
                            ficha=ficha, pericia=pericia, treinado=False
                        )
                        pericia_treinada.atributo_chave.set([atributo_ch])
                    except AtributoFicha.DoesNotExist:
                        # Se não encontrar o atributo, pular esta perícia
                        continue

            # Adicionar automaticamente o ataque "Ataque desarmado"
            try:
                pericia_luta = Pericia.objects.get(nome="lut")
                ataque_desarmado, _ = Ataque.objects.get_or_create(
                    nome="Ataque desarmado",
                    defaults={
                        "dano": "1d4",
                        "pericia": pericia_luta,
                        "tipo_dano": "imp",
                    },
                )
                ficha.ataques.set([ataque_desarmado])
            except Pericia.DoesNotExist:
                pass  # Se não encontrar a perícia de luta, pular

            # Associar habilidades automáticas
            # Habilidades de nível 1 da classe
            habilidades_classe = Habilidade.objects.filter(
                classe_pers=classe, origem="cl", nivel_habilidade=1
            )
            for habilidade in habilidades_classe:
                ficha.habilidades.add(habilidade)

            # Habilidades de origem
            habilidades_origem = Habilidade.objects.filter(
                origem_pers=origem, origem="or"
            )
            for habilidade in habilidades_origem:
                ficha.habilidades.add(habilidade)

            # Habilidades de raça
            habilidades_raca = Habilidade.objects.filter(raca_pers=raca, origem="rc")
            for habilidade in habilidades_raca:
                ficha.habilidades.add(habilidade)

            # Calcular vida e mana máximas
            ficha.vida_max = ficha.calcularVida()
            ficha.mana_max = ficha.calcularMana()
            ficha.vida_atual = ficha.vida_max
            ficha.mana_atual = ficha.mana_max
            ficha.save()

            # Retornar a ficha criada
            return Response(
                self.get_serializer(ficha).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"DEBUG: Erro ao criar ficha: {str(e)}")
            return Response(
                {"detail": f"Erro ao criar ficha: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["get"],
        url_path="dados-criacao",
        permission_classes=[permissions.AllowAny],
    )
    def dados_criacao(self, request):
        """
        Action para obter todos os dados necessários para criar uma ficha.
        Retorna raças, origens, classes, atributos, perícias e divindades.
        """
        context = {
            "racas": RacaSerializer(Raca.objects.all(), many=True).data,
            "origens": OrigemSerializer(Origem.objects.all(), many=True).data,
            "classes": ClasseSerializer(Classe.objects.all(), many=True).data,
            "atributos": AtributoSerializer(
                Atributo.objects.all().order_by("ordem"), many=True
            ).data,
            "pericias": PericiaSerializer(Pericia.objects.all(), many=True).data,
            "divindades": DivindadeSerializer(Divindade.objects.all(), many=True).data,
        }
        return Response(context)

    @action(detail=True, methods=["post"], url_path="add-habilidade")
    def add_habilidade(self, request, pk=None):
        """
        Action para adicionar uma habilidade à ficha.
        Espera: {"habilidade_id": 123}
        """
        ficha = self.get_object()
        habilidade_id = request.data.get("habilidade_id")

        if not habilidade_id:
            return Response(
                {"detail": "O campo 'habilidade_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            habilidade = get_object_or_404(Habilidade, pk=habilidade_id)

            # Verificar se a habilidade já está na ficha
            if ficha.habilidades.filter(id=habilidade_id).exists():
                return Response(
                    {"detail": f"A habilidade '{habilidade.nome}' já está na ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Adicionar a habilidade à ficha
            ficha.habilidades.add(habilidade)

            return Response(
                {
                    "message": f"Habilidade '{habilidade.nome}' adicionada com sucesso!",
                    "habilidade": HabilidadeSerializer(habilidade).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao adicionar habilidade: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="remove-habilidade")
    def remove_habilidade(self, request, pk=None):
        """
        Action para remover uma habilidade da ficha.
        Espera: {"habilidade_id": 123}
        """
        ficha = self.get_object()
        habilidade_id = request.data.get("habilidade_id")

        if not habilidade_id:
            return Response(
                {"detail": "O campo 'habilidade_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            habilidade = get_object_or_404(Habilidade, pk=habilidade_id)

            # Verificar se a habilidade está na ficha
            if not ficha.habilidades.filter(id=habilidade_id).exists():
                return Response(
                    {"detail": f"A habilidade '{habilidade.nome}' não está na ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Remover a habilidade da ficha
            ficha.habilidades.remove(habilidade)

            return Response(
                {
                    "message": f"Habilidade '{habilidade.nome}' removida com sucesso!",
                    "habilidade": HabilidadeSerializer(habilidade).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao remover habilidade: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="add-ataque")
    def add_ataque(self, request, pk=None):
        """
        Action para adicionar um ataque à ficha.
        Espera: {"ataque_id": 123}
        """
        ficha = self.get_object()
        ataque_id = request.data.get("ataque_id")

        if not ataque_id:
            return Response(
                {"detail": "O campo 'ataque_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ataque = get_object_or_404(Ataque, pk=ataque_id)

            # Verificar se o ataque já está na ficha
            if ficha.ataques.filter(id=ataque_id).exists():
                return Response(
                    {"detail": f"O ataque '{ataque.nome}' já está na ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Adicionar o ataque à ficha
            ficha.ataques.add(ataque)

            return Response(
                {
                    "message": f"Ataque '{ataque.nome}' adicionado com sucesso!",
                    "ataque": AtaqueSerializer(ataque).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao adicionar ataque: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="remove-ataque")
    def remove_ataque(self, request, pk=None):
        """
        Action para remover um ataque da ficha.
        Espera: {"ataque_id": 123}
        """
        ficha = self.get_object()
        ataque_id = request.data.get("ataque_id")

        if not ataque_id:
            return Response(
                {"detail": "O campo 'ataque_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ataque = get_object_or_404(Ataque, pk=ataque_id)

            # Verificar se o ataque está na ficha
            if not ficha.ataques.filter(id=ataque_id).exists():
                return Response(
                    {"detail": f"O ataque '{ataque.nome}' não está na ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Remover o ataque da ficha
            ficha.ataques.remove(ataque)

            return Response(
                {
                    "message": f"Ataque '{ataque.nome}' removido com sucesso!",
                    "ataque": AtaqueSerializer(ataque).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao remover ataque: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # --- Actions para subir de nível ---
    @action(detail=True, methods=["post"], url_path="subir-nivel-classe-atual")
    def subir_nivel_classe_atual(self, request, pk=None):
        """
        Action para subir o nível da classe atual da ficha.
        Aumenta o nível do personagem e da primeira classe.
        """
        ficha = self.get_object()

        try:
            # Aumenta o nível do personagem
            ficha.nivel += 1
            ficha.save()

            # Aumenta o nível da classe atual (primeira classe encontrada)
            nivel_classe = NivelClasseFicha.objects.filter(ficha=ficha).first()
            if nivel_classe:
                nivel_classe.nivel += 1
                novo_nivel = nivel_classe.nivel
                nivel_classe.save()

                # Adicionar automaticamente habilidades de classe do novo nível
                habilidades_adicionadas = []
                try:
                    # Buscar habilidades da classe para o novo nível
                    habilidades_classe_nivel = Habilidade.objects.filter(
                        classe_pers=nivel_classe.classe,
                        origem="cl",
                        nivel_habilidade=novo_nivel,
                    )

                    for habilidade in habilidades_classe_nivel:
                        # Verificar se a habilidade já está na ficha
                        if not ficha.habilidades.filter(id=habilidade.id).exists():
                            ficha.habilidades.add(habilidade)
                            habilidades_adicionadas.append(
                                {
                                    "id": habilidade.id,
                                    "nome": habilidade.nome,
                                    "nivel": habilidade.nivel_habilidade,
                                }
                            )

                except Exception as hab_error:
                    # Se houver erro ao adicionar habilidades, apenas loga mas não falha a operação
                    print(
                        f"Erro ao adicionar habilidades automáticas: {str(hab_error)}"
                    )

                return Response(
                    {
                        "message": f"Nível da classe {nivel_classe.classe.nome} aumentado para {nivel_classe.nivel}!",
                        "habilidades_adicionadas": habilidades_adicionadas,
                        "total_habilidades_adicionadas": len(habilidades_adicionadas),
                        "ficha": self.get_serializer(ficha).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Nenhuma classe encontrada para esta ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao subir nível: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="adicionar-nova-classe")
    def adicionar_nova_classe(self, request, pk=None):
        """
        Action para adicionar uma nova classe à ficha (multiclasse).
        Espera: {"classe_id": 123, "nivel": 1}
        """
        ficha = self.get_object()
        classe_id = request.data.get("classe_id")
        nivel = request.data.get("nivel", 1)

        if not classe_id:
            return Response(
                {"detail": "O campo 'classe_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            classe = get_object_or_404(Classe, id=classe_id)
            nivel = int(nivel)

            # Verificar se a classe já está na ficha
            if NivelClasseFicha.objects.filter(ficha=ficha, classe=classe).exists():
                return Response(
                    {"detail": f"A classe '{classe.nome}' já está na ficha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Adiciona a nova classe à ficha
            NivelClasseFicha.objects.create(ficha=ficha, classe=classe, nivel=nivel)

            # Aumenta o nível do personagem
            ficha.nivel += nivel
            ficha.save()

            # Adicionar automaticamente habilidades de classe de nível 1 (ou do nível inicial especificado)
            habilidades_adicionadas = []
            try:
                # Buscar habilidades da classe para os níveis de 1 até o nível especificado
                for nivel_hab in range(1, nivel + 1):
                    habilidades_classe_nivel = Habilidade.objects.filter(
                        classe_pers=classe, origem="cl", nivel_habilidade=nivel_hab
                    )

                    for habilidade in habilidades_classe_nivel:
                        # Verificar se a habilidade já está na ficha
                        if not ficha.habilidades.filter(id=habilidade.id).exists():
                            ficha.habilidades.add(habilidade)
                            habilidades_adicionadas.append(
                                {
                                    "id": habilidade.id,
                                    "nome": habilidade.nome,
                                    "nivel": habilidade.nivel_habilidade,
                                }
                            )

            except Exception as hab_error:
                # Se houver erro ao adicionar habilidades, apenas loga mas não falha a operação
                print(f"Erro ao adicionar habilidades automáticas: {str(hab_error)}")

            return Response(
                {
                    "message": f"Nova classe '{classe.nome}' adicionada com sucesso!",
                    "habilidades_adicionadas": habilidades_adicionadas,
                    "total_habilidades_adicionadas": len(habilidades_adicionadas),
                    "ficha": self.get_serializer(ficha).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao adicionar classe: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="subir-nivel-classe-especifica")
    def subir_nivel_classe_especifica(self, request, pk=None):
        """
        Action para subir o nível de uma classe específica.
        Espera: {"classe_id": 123}
        """
        ficha = self.get_object()
        classe_id = request.data.get("classe_id")

        if not classe_id:
            return Response(
                {"detail": "O campo 'classe_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            nivel_classe = get_object_or_404(
                NivelClasseFicha, ficha=ficha, classe_id=classe_id
            )

            # Aumenta o nível da classe
            nivel_classe.nivel += 1
            novo_nivel = nivel_classe.nivel
            nivel_classe.save()

            # Aumenta o nível do personagem
            ficha.nivel += 1
            ficha.save()

            # Adicionar automaticamente habilidades de classe do novo nível
            habilidades_adicionadas = []
            try:
                # Buscar habilidades da classe para o novo nível
                habilidades_classe_nivel = Habilidade.objects.filter(
                    classe_pers_id=classe_id, origem="cl", nivel_habilidade=novo_nivel
                )

                for habilidade in habilidades_classe_nivel:
                    # Verificar se a habilidade já está na ficha
                    if not ficha.habilidades.filter(id=habilidade.id).exists():
                        ficha.habilidades.add(habilidade)
                        habilidades_adicionadas.append(
                            {
                                "id": habilidade.id,
                                "nome": habilidade.nome,
                                "nivel": habilidade.nivel_habilidade,
                            }
                        )

            except Exception as hab_error:
                # Se houver erro ao adicionar habilidades, apenas loga mas não falha a operação
                print(f"Erro ao adicionar habilidades automáticas: {str(hab_error)}")

            return Response(
                {
                    "message": f"Nível da classe '{nivel_classe.classe.nome}' aumentado para {nivel_classe.nivel}!",
                    "habilidades_adicionadas": habilidades_adicionadas,
                    "total_habilidades_adicionadas": len(habilidades_adicionadas),
                    "ficha": self.get_serializer(ficha).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao subir nível da classe: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="deletar-classe")
    def deletar_classe(self, request, pk=None):
        """
        Action para remover uma classe da ficha.
        Espera: {"classe_id": 123}
        """
        ficha = self.get_object()
        classe_id = request.data.get("classe_id")

        if not classe_id:
            return Response(
                {"detail": "O campo 'classe_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            nivel_classe = get_object_or_404(
                NivelClasseFicha, ficha=ficha, classe_id=classe_id
            )

            # Salva informações antes de deletar
            classe_nome = nivel_classe.classe.nome
            niveis_perdidos = nivel_classe.nivel

            # Remove a classe e diminui o nível do personagem
            nivel_classe.delete()
            ficha.nivel = max(1, ficha.nivel - niveis_perdidos)  # Evita nível 0
            ficha.save()

            return Response(
                {
                    "message": f"Classe '{classe_nome}' removida! Níveis perdidos: {niveis_perdidos}.",
                    "ficha": self.get_serializer(ficha).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao deletar classe: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="habilidades-disponiveis")
    def habilidades_disponiveis(self, request, pk=None):
        """
        Action para listar habilidades disponíveis com busca.
        Query params:
        - ?q=nome_da_habilidade: para buscar habilidades pelo nome
        - ?incluirTodasHabilidades=true: para retornar todas as habilidades

        Sem busca: mostra apenas habilidades relevantes (origem, classe, raça, gerais, destino da divindade, tormenta se lefou)
        Com busca: mostra qualquer habilidade que contenha o termo pesquisado
        """
        ficha = self.get_object()
        query = request.query_params.get("q", "")
        incluir_todas = (
            request.query_params.get("incluirTodasHabilidades", "").lower() == "true"
        )

        # Se solicitado para incluir todas as habilidades, não aplicamos filtros
        if incluir_todas:
            # Retorna todas as habilidades
            habilidades = Habilidade.objects.all().order_by("nome")

            return Response(
                {
                    "habilidades": HabilidadeSerializer(habilidades, many=True).data,
                    "total": habilidades.count(),
                    "query": query,
                    "filtros_aplicados": "todas_habilidades",
                }
            )

        # Buscar habilidades que não estão na ficha
        habilidades_na_ficha = ficha.habilidades.values_list("id", flat=True)
        habilidades = Habilidade.objects.exclude(id__in=habilidades_na_ficha)

        if query:
            # Se há busca, mostra qualquer habilidade que contenha o termo
            habilidades = habilidades.filter(nome__icontains=query)
        else:
            # Sem busca, filtra por características da ficha

            # IDs das raças, origens e classes da ficha
            racas_ficha = ficha.racas.values_list("id", flat=True)
            origens_ficha = ficha.origens.values_list("id", flat=True)
            classes_ficha = NivelClasseFicha.objects.filter(ficha=ficha).values_list(
                "classe_id", flat=True
            )
            divindade_ficha = ficha.divindade

            # Condições base
            condicoes = Q()

            # 1. Habilidades de origem
            if origens_ficha:
                condicoes |= Q(origem_pers__in=origens_ficha, origem="or")

            # 2. Habilidades de classe
            if classes_ficha:
                condicoes |= Q(classe_pers__in=classes_ficha, origem="cl")

            # 3. Habilidades de raça
            if racas_ficha:
                condicoes |= Q(raca_pers__in=racas_ficha, origem="rc")

            # 4. Habilidades gerais (origem='ge')
            condicoes |= Q(origem="ge")

            # 5. Habilidades de destino da divindade (origem='de')
            if divindade_ficha:
                condicoes |= Q(divindade_pers=divindade_ficha, origem="de")

            # 6. Habilidades de tormenta se a raça for lefou
            raca_lefou_existe = ficha.racas.filter(nome__iexact="lefou").exists()
            if raca_lefou_existe:
                condicoes |= Q(origem="to")  # Assumindo que 'to' é tormenta

            habilidades = habilidades.filter(condicoes)

        habilidades = habilidades.order_by("nome")

        return Response(
            {
                "habilidades": HabilidadeSerializer(habilidades, many=True).data,
                "total": habilidades.count(),
                "query": query,
                "filtros_aplicados": (
                    "busca_geral" if query else "filtros_personalizados"
                ),
            }
        )

    @action(detail=True, methods=["get"], url_path="ataques-disponiveis")
    def ataques_disponiveis(self, request, pk=None):
        """
        Action para listar ataques disponíveis com busca.
        Query params: ?q=nome_do_ataque
        """
        ficha = self.get_object()
        query = request.query_params.get("q", "")

        # Buscar ataques que não estão na ficha
        ataques_na_ficha = ficha.ataques.values_list("id", flat=True)
        ataques = Ataque.objects.exclude(id__in=ataques_na_ficha)

        if query:
            ataques = ataques.filter(nome__icontains=query)

        ataques = ataques.order_by("nome")

        return Response(
            {
                "ataques": AtaqueSerializer(ataques, many=True).data,
                "total": ataques.count(),
                "query": query,
            }
        )

    @action(detail=True, methods=["get"], url_path="classes-disponiveis")
    def classes_disponiveis(self, request, pk=None):
        """
        Action para listar classes disponíveis para multiclasse.
        Retorna classes que a ficha ainda não possui.
        """
        ficha = self.get_object()

        # Buscar classes que não estão na ficha
        classes_na_ficha = NivelClasseFicha.objects.filter(ficha=ficha).values_list(
            "classe_id", flat=True
        )
        classes = Classe.objects.exclude(id__in=classes_na_ficha).order_by("nome")

        return Response(
            {
                "classes": ClasseSerializer(classes, many=True).data,
                "total": classes.count(),
            }
        )


# === VIEWSETS PARA HOMEBREW CONTENT ===


class RacaViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    queryset = Raca.objects.all()
    serializer_class = RacaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(dono=user) | Q(dono=None))


class OrigemViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    queryset = Origem.objects.all()
    serializer_class = OrigemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(dono=user) | Q(dono=None))


class DivindadeViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    queryset = Divindade.objects.all()
    serializer_class = DivindadeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(dono=user) | Q(dono=None))


class ClasseViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)

    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(dono=user) | Q(dono=None))


class CustomAuthToken(ObtainAuthToken):
    """
    Custom token authentication view que retorna dados do usuário junto com o token
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Action para registrar um novo usuário
    """
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")

    # Validações básicas
    if not username:
        return Response(
            {"detail": "O campo 'username' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not password:
        return Response(
            {"detail": "O campo 'password' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(password) < 6:
        return Response(
            {"detail": "A senha deve ter pelo menos 6 caracteres."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Verificar se o usuário já existe
    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Este nome de usuário já está em uso."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"detail": "Este email já está em uso."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Criar o usuário
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Criar token para o usuário
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Usuário criado com sucesso!",
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"detail": f"Erro ao criar usuário: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Action para fazer logout (deletar token)
    """
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Usuário não está logado."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Deletar o token do usuário
        Token.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"detail": f"Erro ao fazer logout: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Action para obter dados do usuário logado
    """
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Usuário não está logado."}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = request.user
    return Response(
        {
            "user_id": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Action para atualizar dados do usuário logado
    """
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Usuário não está logado."}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = request.user
    email = request.data.get("email")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")

    # Verificar se o email já está em uso por outro usuário
    if email and User.objects.filter(email=email).exclude(id=user.id).exists():
        return Response(
            {"detail": "Este email já está em uso."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Atualizar dados do usuário
        if email:
            user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return Response(
            {
                "message": "Perfil atualizado com sucesso!",
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"detail": f"Erro ao atualizar perfil: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# --- Views JWT Customizadas ---


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada para login com JWT que retorna dados do usuário
    """

    serializer_class = CustomTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    """
    View para registro de novos usuários com JWT automático
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Criar usuário e retornar tokens JWT automaticamente
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Criar usuário
        user = serializer.save()

        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Resposta com tokens e dados do usuário
        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "access": str(access_token),
                "refresh": str(refresh),
                "message": "Usuário criado com sucesso!",
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    """
    View para logout que adiciona refresh token à blacklist
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Fazer logout adicionando o refresh token à blacklist
        """
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Adicionar token à blacklist
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response(
                {"detail": f"Token inválido: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro ao fazer logout: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CurrentUserAPIView(APIView):
    """
    View para obter e atualizar dados do usuário autenticado atual
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retornar dados do usuário autenticado
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Atualizar dados do usuário autenticado
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenAPIView(APIView):
    """
    View para verificar se um token JWT é válido
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verificar se um token é válido
        """
        try:
            token = request.data.get("token")
            if not token:
                return Response(
                    {"detail": "Token é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Tentar decodificar o token
            from rest_framework_simplejwt.tokens import UntypedToken

            UntypedToken(token)

            return Response(
                {"valid": True, "message": "Token válido"}, status=status.HTTP_200_OK
            )
        except (InvalidToken, TokenError) as e:
            return Response(
                {"valid": False, "detail": f"Token inválido: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"valid": False, "detail": f"Erro ao verificar token: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleOAuthLoginView(APIView):
    """
    View para autenticação via Google OAuth2 usando código de autorização
    Endpoint: POST /arkheion_api/auth/google/
    Recebe um código de autorização e retorna tokens JWT do Arkheion
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Recebe o código de autorização do frontend
        import logging
        from .serializers import GoogleOAuthSerializer
        from rest_framework_simplejwt.tokens import RefreshToken

        logger = logging.getLogger(__name__)

        try:
            logger.info("Iniciando autenticação Google OAuth2")
            serializer = GoogleOAuthSerializer(data=request.data)

            if serializer.is_valid():
                # O serializer já validou o código e criou/recuperou o usuário
                user = serializer.save()

                # Gerar tokens JWT para o usuário
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Atualizar last_login
                from django.utils import timezone

                user.last_login = timezone.now()
                user.save(update_fields=["last_login"])

                logger.info(f"Autenticação Google bem-sucedida para: {user.email}")

                return Response(
                    {
                        "access": str(access_token),
                        "refresh": str(refresh),
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "date_joined": user.date_joined,
                            "last_login": user.last_login,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            logger.warning(
                f"Erro de validação na autenticação Google: {serializer.errors}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Erro inesperado na autenticação Google: {str(e)}")
            return Response(
                {
                    "error": "Erro interno do servidor",
                    "detail": "Ocorreu um erro durante a autenticação com Google",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
