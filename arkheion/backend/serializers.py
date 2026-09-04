from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
    Monstro,
    MonstroPericia,
    Mesa,
    MesaParticipante,
    MesaCombate,
)

# --- Serializers para modelos base/relacionados ---


class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ["id", "nome", "ordem"]


class PericiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pericia
        fields = ["id", "nome", "requer_treino"]


class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = ["id", "nome", "descricao", "homebrew", "dono"]


class OrigemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origem
        fields = ["id", "nome", "descricao", "homebrew", "dono"]


class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = [
            "id",
            "nome",
            "descricao",
            "proficiencia",
            "vida_base",
            "vida_por_nivel",
            "mana_base",
            "mana_por_nivel",
            "pericias_treinadas",
            "pericias_para_escolher",
            "homebrew",
            "dono",
        ]


class AtaqueSerializer(serializers.ModelSerializer):
    tipo_dano_display = serializers.CharField(
        # Exibir nome completo do tipo de dano
        source="get_tipo_dano_display",
        read_only=True,
    )
    # Aninhar a perícia para ver detalhes
    pericia = PericiaSerializer(read_only=True)

    class Meta:
        model = Ataque
        fields = [
            "id",
            "nome",
            "descricao",
            "dano",
            "tipo_dano",
            "tipo_dano_display",
            "pericia",
            "resistencia",
            "homebrew",
            "dono",
        ]


class HabilidadeSerializer(serializers.ModelSerializer):
    origem_display = serializers.CharField(
        source="get_origem_display", read_only=True
    )  # Exibir nome completo da origem
    # Aninhar raça de origem, se houver
    raca_pers = RacaSerializer(read_only=True)
    # Aninhar origem de origem, se houver
    origem_pers = OrigemSerializer(read_only=True)
    # Aninhar classe de origem, se houver
    classe_pers = ClasseSerializer(read_only=True)

    class Meta:
        model = Habilidade
        fields = [
            "id",
            "nome",
            "descricao",
            "origem",
            "origem_display",
            "ativo",
            "nivel_habilidade",
            "raca_pers",
            "origem_pers",
            "classe_pers",
            "homebrew",
            "dono",
        ]


class DivindadeSerializer(serializers.ModelSerializer):
    # poderes_concedidos_divindade = HabilidadeSerializer(many=True, read_only=True) # Se quiser aninhar as habilidades da divindade

    class Meta:
        model = Divindade
        fields = [
            "id",
            "nome",
            "descricao",
            "obrigacoes",
            "restrições",
            "simbolo",
            "homebrew",
            "dono",
            # 'poderes_concedidos_divindade' # Descomentar se quiser aninhar as habilidades
        ]


# --- Serializers para os modelos "through" (intermediários) ---


class AtributoFichaSerializer(serializers.ModelSerializer):
    atributo = AtributoSerializer(read_only=True)

    class Meta:
        model = AtributoFicha
        fields = ["id", "atributo", "valor"]


class PericiaTreinadaSerializer(serializers.ModelSerializer):
    pericia = PericiaSerializer(read_only=True)
    atributo_chave = AtributoFichaSerializer(many=True, read_only=True)

    valor_calculado = serializers.SerializerMethodField()  # Campo calculado

    class Meta:
        model = PericiaTreinada
        fields = [
            "id",
            "pericia",
            "treinado",
            "bonus_adicional",
            "atributo_chave",
            "valor_calculado",
        ]

    def get_valor_calculado(self, obj):
        return obj.calcularValor()


class NivelClasseFichaSerializer(serializers.ModelSerializer):
    classe = ClasseSerializer(read_only=True)

    class Meta:
        model = NivelClasseFicha
        fields = ["id", "classe", "nivel"]


class AtributoFichaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoFicha
        fields = ["id", "atributo", "valor", "ficha"]
        extra_kwargs = {"ficha": {"write_only": True}}


class PericiaTreinadaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PericiaTreinada
        fields = ["id", "ficha", "pericia", "treinado", "bonus_adicional"]
        extra_kwargs = {"ficha": {"write_only": True}}


class NivelClasseFichaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelClasseFicha
        fields = ["id", "ficha", "classe", "nivel"]
        extra_kwargs = {"ficha": {"write_only": True}}


# --- Serializer principal da Ficha ---


class FichaSerializer(serializers.ModelSerializer):
    # Campos de leitura (para exibição)
    atributos_ficha = AtributoFichaSerializer(
        source="atributoficha_set", many=True, read_only=True
    )
    pericias_treinadas = PericiaTreinadaSerializer(
        source="periciatreinada_set", many=True, read_only=True
    )
    niveis_classes = NivelClasseFichaSerializer(
        source="nivelclasseficha_set", many=True, read_only=True
    )
    racas = RacaSerializer(many=True, read_only=True)
    origens = OrigemSerializer(many=True, read_only=True)
    habilidades = HabilidadeSerializer(many=True, read_only=True)
    ataques = AtaqueSerializer(many=True, read_only=True)
    divindade = DivindadeSerializer(read_only=True)

    # Campos para escrita (aceitando IDs ou objetos completos)
    atributos = AtributoFichaWriteSerializer(many=True, write_only=True, required=False)
    classes = NivelClasseFichaWriteSerializer(
        many=True, write_only=True, required=False
    )
    racas_ids = serializers.PrimaryKeyRelatedField(
        queryset=Raca.objects.all(),
        many=True,
        write_only=True,
        source="racas",
        required=False,
    )
    origens_ids = serializers.PrimaryKeyRelatedField(
        queryset=Origem.objects.all(),
        many=True,
        write_only=True,
        source="origens",
        required=False,
    )
    divindade_id = serializers.PrimaryKeyRelatedField(
        queryset=Divindade.objects.all(),
        write_only=True,
        source="divindade",
        required=False,
    )

    class Meta:
        model = Ficha
        fields = "__all__"
        read_only_fields = [
            "dono",
            "vida_maxima_calculada",
            "mana_maxima_calculada",
            "vida_atual",
            "mana_atual",
            "nivel",
            "exp",
        ]

    def create(self, validated_data):
        # Extrai os dados dos relacionamentos
        atributos_data = validated_data.pop("atributoficha_set", [])
        pericias_data = validated_data.pop("periciatreinada_set", [])
        classes_data = validated_data.pop("nivelclasseficha_set", [])
        racas_data = validated_data.pop("racas", [])
        origens_data = validated_data.pop("origens", [])
        divindade_data = validated_data.pop("divindade", None)

        # Cria a ficha base
        ficha = Ficha.objects.create(**validated_data)

        # Cria os atributos (through model)
        for atributo in atributos_data:
            AtributoFicha.objects.create(ficha=ficha, **atributo)

        # Cria as perícias treinadas
        for pericia in pericias_data:
            PericiaTreinada.objects.create(ficha=ficha, **pericia)

        # Cria os níveis de classe
        for classe in classes_data:
            NivelClasseFicha.objects.create(ficha=ficha, **classe)

        # Adiciona os relacionamentos ManyToMany
        ficha.racas.set(racas_data)
        ficha.origens.set(origens_data)

        # Adiciona a divindade (ForeignKey)
        if divindade_data:
            ficha.divindade = divindade_data
            ficha.save()

        return ficha

    def update(self, instance, validated_data):
        # Similar ao create, mas para atualização
        # Implemente conforme sua necessidade
        return super().update(instance, validated_data)

    def add_habilidades_automaticas(self, ficha, racas, origens, classes):
        # Habilidades de classe (nível 1)
        for nivel_classe in classes:
            habilidades = Habilidade.objects.filter(
                classe_pers=nivel_classe["classe"], origem="cl", nivel_habilidade=1
            )
            ficha.habilidades.add(*habilidades)

        # Habilidades de origem
        for origem in origens:
            habilidades = Habilidade.objects.filter(origem_pers=origem, origem="or")
            ficha.habilidades.add(*habilidades)

        # Habilidades de raça
        for raca in racas:
            habilidades = Habilidade.objects.filter(raca_pers=raca, origem="rc")
            ficha.habilidades.add(*habilidades)


#    def validate(self, data):
#        # Verifica se pelo menos uma raça foi selecionada
#        if 'racas' not in data or len(data['racas']) == 0:
#            raise serializers.ValidationError("Pelo menos uma raça deve ser selecionada")

# Verifica se pelo menos uma origem foi selecionada
#        if 'origens' not in data or len(data['origens']) == 0:
#            raise serializers.ValidationError("Pelo menos uma origem deve ser selecionada")

# Verifica se pelo menos uma classe foi selecionada
#        if 'classes' not in data or len(data['classes']) == 0:
#            raise serializers.ValidationError("Pelo menos uma classe deve ser selecionada")

#        return data

# --- Serializer para o modelo User ---


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


# --- Serializers para Monstros (se precisar de uma API para eles) ---


class MonstroPericiaSerializer(serializers.ModelSerializer):
    pericia = PericiaSerializer(read_only=True)
    # Assumindo que AtributoFicha é aplicável a monstros
    atributo_chave = AtributoFichaSerializer(many=True, read_only=True)

    class Meta:
        model = MonstroPericia
        fields = ["id", "pericia", "atributo_chave"]


class MonstroSerializer(serializers.ModelSerializer):
    atributos_monstro = AtributoFichaSerializer(
        # Reutilizando AtributoFichaSerializer
        source="atributoficha_set",
        many=True,
        read_only=True,
    )
    habilidades = HabilidadeSerializer(many=True, read_only=True)
    ataques = AtaqueSerializer(many=True, read_only=True)
    pericias_monstro = MonstroPericiaSerializer(
        # Usando MonstroPericiaSerializer
        source="monstropericia_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Monstro
        fields = [
            "id",
            "dono",
            "nome",
            "nivel",
            "nd",
            "cd",
            "ca",
            "vida",
            "mana",
            "deslocamento",
            "tamanho",
            "atributos_monstro",
            "habilidades",
            "ataques",
            "pericias_monstro",
        ]
        read_only_fields = ["dono", "nivel", "nd"]


# --- Serializers para Mesa (se precisar de uma API para elas) ---


class MesaParticipanteSerializer(serializers.ModelSerializer):
    jogador = UserSerializer(read_only=True)  # Aninha o usuário
    # Aninha a ficha do participante (pode ser um resumo se for muito grande)
    ficha = FichaSerializer(read_only=True)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = MesaParticipante
        fields = [
            "id",
            "mesa",
            "jogador",
            "tipo",
            "tipo_display",
            "data_entrada",
            "data_saida",
            "iniciativa",
            "ficha",
        ]
        read_only_fields = ["data_entrada", "data_saida"]


class MesaSerializer(serializers.ModelSerializer):
    participantes_mesa = MesaParticipanteSerializer(
        # Usando related_name 'mesa_jogador'
        source="mesa_jogador",
        many=True,
        read_only=True,
    )
    # monstros = MonstroSerializer(many=True, read_only=True) # Se quiser aninhar monstros no serializer de mesa

    class Meta:
        model = Mesa
        fields = [
            "id",
            "dono",
            "nome",
            "descricao",
            "data_criacao",
            "participantes_mesa",  # 'monstros' # Descomentar se quiser aninhar monstros na mesa
        ]
        read_only_fields = ["dono", "data_criacao"]


class MesaCombateSerializer(serializers.ModelSerializer):
    mesa = MesaSerializer(read_only=True)  # Aninha a mesa
    # Aninha os monstros do combate
    monstros = MonstroSerializer(many=True, read_only=True)

    class Meta:
        model = MesaCombate
        fields = ["id", "mesa", "monstros", "rodada_atual", "turno_atual", "ativo"]


# --- Serializers para Autenticação JWT ---


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para incluir dados do usuário no login
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Adicionar dados do usuário à resposta
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "date_joined": self.user.date_joined,
            "last_login": self.user.last_login,
        }

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novos usuários
    """

    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        """
        Validação customizada
        """
        # Verificar se as senhas coincidem
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("As senhas não coincidem.")

        # Verificar se o email já existe
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Este email já está em uso.")

        # Verificar se o username já existe
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")

        return attrs

    def create(self, validated_data):
        """
        Criar usuário com senha hasheada
        """
        # Remover password_confirm dos dados
        validated_data.pop("password_confirm")

        # Criar usuário
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico para dados do usuário
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class GoogleOAuthSerializer(serializers.Serializer):
    """
    Serializer para autenticação via Google OAuth2 usando código de autorização
    """

    code = serializers.CharField(
        required=True, help_text="Código de autorização do Google"
    )
    redirect_uri = serializers.URLField(
        required=False, help_text="URI de redirecionamento usado na autorização"
    )

    def validate_code(self, code):
        """
        Valida o código de autorização do Google e troca por tokens
        """
        import requests
        from django.conf import settings
        import logging

        logger = logging.getLogger(__name__)

        # URL para trocar código por tokens
        token_url = "https://oauth2.googleapis.com/token"

        # Usar redirect_uri fornecido ou o padrão das configurações
        redirect_uri = self.initial_data.get(
            "redirect_uri", settings.GOOGLE_OAUTH2_REDIRECT_URI
        )

        # Dados para a requisição
        token_data = {
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        try:
            # Trocar código por tokens
            logger.info("Trocando código de autorização por tokens do Google")
            token_response = requests.post(token_url, data=token_data, timeout=10)

            if token_response.status_code != 200:
                logger.error(
                    f"Erro ao trocar código: {token_response.status_code} - {token_response.text}"
                )
                error_detail = token_response.json().get(
                    "error_description", "Código de autorização inválido"
                )
                raise serializers.ValidationError(
                    f"Erro do Google OAuth: {error_detail}"
                )

            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                logger.error("Access token não encontrado na resposta do Google")
                raise serializers.ValidationError(
                    "Não foi possível obter token de acesso do Google"
                )

            # Buscar informações do usuário usando o token de acesso
            user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
            logger.info("Buscando informações do usuário no Google")
            user_response = requests.get(user_info_url, timeout=10)

            if user_response.status_code != 200:
                logger.error(
                    f"Erro ao buscar dados do usuário: {user_response.status_code}"
                )
                raise serializers.ValidationError(
                    "Não foi possível obter informações do usuário do Google"
                )

            user_data = user_response.json()

            # Verificar se o email está presente
            if "email" not in user_data:
                logger.error("Email não fornecido pelo Google")
                raise serializers.ValidationError("Email não fornecido pelo Google")

            # Verificar se o email foi verificado pelo Google
            if not user_data.get("verified_email", False):
                logger.warning(
                    f"Email não verificado pelo Google: {user_data.get('email')}"
                )
                raise serializers.ValidationError(
                    "Email não foi verificado pelo Google"
                )

            logger.info(f"Usuário autenticado com sucesso: {user_data.get('email')}")
            return user_data

        except requests.RequestException as e:
            logger.error(f"Erro de rede ao comunicar com Google: {str(e)}")
            raise serializers.ValidationError(f"Erro ao comunicar com Google: {str(e)}")
        except serializers.ValidationError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado na validação do código: {str(e)}")
            raise serializers.ValidationError(
                "Erro interno na validação do código Google"
            )

    def create(self, validated_data):
        """
        Criar ou recuperar usuário baseado nos dados do Google
        """
        import logging
        import secrets

        logger = logging.getLogger(__name__)
        # Os dados do usuário Google vêm do método validate_code via validated_data['code']
        google_user_data = validated_data["code"]

        # Buscar ou criar usuário
        try:
            user = User.objects.get(email=google_user_data["email"])
            logger.info(f"Usuário existente encontrado: {user.email}")

            # Atualizar dados se necessário
            updated = False
            if not user.first_name and google_user_data.get("given_name"):
                user.first_name = google_user_data["given_name"]
                updated = True
            if not user.last_name and google_user_data.get("family_name"):
                user.last_name = google_user_data["family_name"]
                updated = True
            if updated:
                user.save()
                logger.info(f"Dados do usuário atualizados: {user.email}")

        except User.DoesNotExist:
            logger.info(f"Criando novo usuário para: {google_user_data['email']}")

            # Criar novo usuário
            username = google_user_data["email"].split("@")[0]
            # Garantir que o username seja único
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1

            # Gerar uma senha aleatória para usuários do Google
            # Isso permite login tradicional futuro se necessário
            random_password = secrets.token_urlsafe(50)

            user = User.objects.create_user(
                username=username,
                email=google_user_data["email"],
                first_name=google_user_data.get("given_name", ""),
                last_name=google_user_data.get("family_name", ""),
                password=random_password,  # Senha aleatória forte
            )

            logger.info(
                f"Novo usuário criado: {user.email} (username: {user.username})"
            )

        return user
