from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import (
    Pericia,
    PericiaTreinada,
    Classe,
    Ataque,
    Atributo,
    AtributoFicha,
    Origem,
    Raca,
    Habilidade,
    Ficha,
    NivelClasseFicha,
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

# Create your views here.


class PersonagensView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")  # Obtém o valor do campo de busca
        fichas = Ficha.objects.filter(dono=request.user).order_by(
            "-id"
        )  # Filtra as fichas pelo usuário logado

        if query:
            fichas = fichas.filter(
                nome__icontains=query
            )  # Filtra pelo nome, se houver uma busca

        context = {"fichas": fichas, "query": query}
        return render(request, "personagens.html", context)


@method_decorator(login_required, name="dispatch")
class CriarFichaView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "racas": Raca.objects.all(),
            "origens": Origem.objects.all(),
            "classes": Classe.objects.all(),
            "atributos": Atributo.objects.all(),
            "pericias": Pericia.objects.all(),
            "divindades": Ficha.DIVINDADES,
        }
        return render(request, "editar/criar_ficha.html", context)

    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        nivel = request.POST.get("nivel", 1)
        divindade = request.POST.get("divindade")
        raca = Raca.objects.get(id=request.POST.get("raca"))
        origem = Origem.objects.get(id=request.POST.get("origem"))
        classe = Classe.objects.get(id=request.POST.get("classe"))

        # Criar a ficha no banco de dados
        ficha = Ficha.objects.create(
            nome=nome, nivel=nivel, divindade=divindade, dono=request.user
        )

        # Definir relações ManyToMany
        ficha.racas.set([raca])
        ficha.origens.set([origem])
        ficha.classes.set([classe])

        # Associar atributos à ficha
        for atributo in Atributo.objects.all():
            valor = request.POST.get(f"atributo_{atributo.id}", 1)
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

        for pericia in Pericia.objects.all():
            if pericia.nome in atributos_por_pericia:
                atributo_nome = atributos_por_pericia[pericia.nome]
                atributo_ch = AtributoFicha.objects.get(
                    ficha=ficha, atributo__nome=atributo_nome
                )

                pericia_treinada = PericiaTreinada.objects.create(
                    ficha=ficha, pericia=pericia, treinado=False
                )
                pericia_treinada.atributo_chave.set(
                    [atributo_ch]
                )  # Define o atributo chave

        # Adicionar automaticamente o ataque "Ataque desarmado"
        pericia_luta = Pericia.objects.get(nome="lut")
        ataque_desarmado, _ = Ataque.objects.get_or_create(
            nome="Ataque desarmado",
            defaults={"dano": "1d4", "pericia": pericia_luta, "tipo_dano": "imp"},
        )
        ficha.ataques.set([ataque_desarmado])

        # Associar habilidades de nível 1 da classe à ficha
        habilidades_classe = Habilidade.objects.filter(
            classe_pers=classe, origem="cl", nivel_habilidade=1
        )
        for habilidade in habilidades_classe:
            ficha.habilidades.add(habilidade)

        # Associar habilidades de origem à ficha
        habilidades_origem = Habilidade.objects.filter(origem_pers=origem, origem="or")
        for habilidade in habilidades_origem:
            ficha.habilidades.add(habilidade)

        # Associar habilidades de raça à ficha
        habilidades_raca = Habilidade.objects.filter(raca_pers=raca, origem="rc")
        for habilidade in habilidades_raca:
            ficha.habilidades.add(habilidade)

        ficha.vida_max = ficha.calcularVida()
        ficha.mana_max = ficha.calcularMana()
        ficha.save()

        messages.success(request, "Ficha criada com sucesso!")
        return redirect("personagens")


@method_decorator(login_required, name="dispatch")
class FichaDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        ficha = get_object_or_404(Ficha, pk=pk)

        if (
            ficha.dono != request.user
        ):  # Verificar se o usuário logado é o dono da ficha
            messages.error(request, "Você não tem permissão para excluir esta ficha.")
            return redirect("personagens")

        ficha.delete()
        messages.success(request, "Ficha excluída com sucesso.")
        return redirect("personagens")  # Redireciona de volta para a lista de fichas


@method_decorator(login_required, name="dispatch")
class FichaCombateView(View):
    def get(self, request, ficha_id, *args, **kwargs):  # Usar 'ficha_id' aqui
        ficha = get_object_or_404(Ficha, pk=ficha_id)  # Obter a ficha pelo 'ficha_id'

        query = request.GET.get("q", "")  # Captura o parâmetro de busca
        if query:
            # Filtra os ataques pela busca no nome
            ataques = ficha.ataques.filter(nome__icontains=query).order_by("nome")
        else:
            # Se não houver busca, mostra todos os ataques
            ataques = ficha.ataques.all().order_by("nome")

        context = {"ficha": ficha, "ataques": ataques, "query": query}
        return render(request, "ficha/ficha_combate.html", context)


@method_decorator(login_required, name="dispatch")
class FichaHabilidadesView(View):
    def get(self, request, ficha_id, *args, **kwargs):  # Usar 'ficha_id' aqui
        ficha = get_object_or_404(Ficha, pk=ficha_id)  # Obter a ficha pelo 'ficha_id'

        query = request.GET.get("q", "")  # Captura o parâmetro de busca
        if query:
            # Filtra as habilidades pela busca no nome
            habilidades = ficha.habilidades.filter(nome__icontains=query).order_by(
                "nome"
            )
        else:
            # Se não houver busca, mostra todas as habilidades
            habilidades = ficha.habilidades.all().order_by("nome")

        context = {"ficha": ficha, "habilidades": habilidades, "query": query}
        return render(request, "ficha/ficha_habilidades.html", context)


@method_decorator(login_required, name="dispatch")
class AddHabilidadeView(View):
    def get(self, request, ficha_id, *args, **kwargs):
        ficha = get_object_or_404(Ficha, pk=ficha_id)  # Usar 'ficha_id' aqui
        query = request.GET.get("q", "")  # Obtém o termo de pesquisa
        habilidades = Habilidade.objects.all()

        if query:
            habilidades = habilidades.filter(nome__icontains=query)

        context = {"ficha": ficha, "habilidades": habilidades, "query": query}
        return render(request, "editar/add_habilidade.html", context)

    def post(self, request, ficha_id, *args, **kwargs):
        ficha = get_object_or_404(Ficha, pk=ficha_id)
        habilidade_id = request.POST.get(
            "habilidade_id"
        )  # ID da habilidade a ser conectada

        if habilidade_id:
            habilidade = get_object_or_404(Habilidade, pk=habilidade_id)
            ficha.habilidades.add(habilidade)  # Adiciona a habilidade à ficha

        return redirect("add_habilidade", ficha_id=ficha.id)


@method_decorator(login_required, name="dispatch")
class RemoveHabilidadeView(View):
    def post(self, request, ficha_id, *args, **kwargs):
        ficha = get_object_or_404(Ficha, pk=ficha_id)
        habilidade_id = request.POST.get(
            "habilidade_id"
        )  # ID da habilidade a ser removida

        if habilidade_id:
            habilidade = get_object_or_404(Habilidade, pk=habilidade_id)
            ficha.habilidades.remove(habilidade)  # Remove a habilidade da ficha
            messages.success(
                request, f"Habilidade '{habilidade.nome}' removida com sucesso!"
            )

        return redirect("ficha_habilidades", ficha_id=ficha.id)


@method_decorator(login_required, name="dispatch")
class EscolherSubirNivelView(View):
    def get(self, request, ficha_id):
        ficha = get_object_or_404(Ficha, id=ficha_id)
        classes = Classe.objects.all()  # Lista de classes disponíveis
        return render(
            request,
            "editar/escolher_subir_nivel.html",
            {"ficha": ficha, "classes": classes},
        )


@method_decorator(login_required, name="dispatch")
class SubirNivelClasseAtualView(View):
    def post(self, request, ficha_id):
        ficha = get_object_or_404(Ficha, id=ficha_id)

        # Aumenta o nível do personagem
        ficha.nivel += 1
        ficha.save()

        # Aumenta o nível da classe atual (se houver)
        nivel_classe = NivelClasseFicha.objects.filter(ficha=ficha).first()
        if nivel_classe:
            nivel_classe.nivel += 1
            nivel_classe.save()

        messages.success(request, "Nível da classe atual aumentado com sucesso!")
        return redirect("ficha_combate", ficha_id=ficha.id)


@method_decorator(login_required, name="dispatch")
class AdicionarNovaClasseView(View):
    def post(self, request, ficha_id):
        ficha = get_object_or_404(Ficha, id=ficha_id)

        classe_id = request.POST.get("classe_id")
        nivel = int(request.POST.get("nivel", 1))

        classe = get_object_or_404(Classe, id=classe_id)

        # Adiciona a nova classe à ficha
        NivelClasseFicha.objects.create(ficha=ficha, classe=classe, nivel=nivel)

        # Aumenta o nível do personagem
        ficha.nivel += 1
        ficha.save()

        messages.success(request, f"Nova classe {classe.nome} adicionada com sucesso!")
        return redirect("ficha_combate", ficha_id=ficha.id)


@method_decorator(login_required, name="dispatch")
class SubirNivelClasseView(View):
    def post(self, request, ficha_id, classe_id):
        ficha = get_object_or_404(Ficha, id=ficha_id)
        nivel_classe = get_object_or_404(
            NivelClasseFicha, ficha=ficha, classe_id=classe_id
        )

        # Aumenta o nível da classe
        nivel_classe.nivel += 1
        nivel_classe.save()

        # Aumenta o nível do personagem
        ficha.nivel += 1
        ficha.save()

        messages.success(
            request,
            f"Nível da classe {nivel_classe.classe.nome} aumentado para {nivel_classe.nivel}!",
        )
        return redirect("escolher_subir_nivel", ficha_id=ficha.id)


@method_decorator(login_required, name="dispatch")
class DeletarClasseView(View):
    def post(self, request, ficha_id, classe_id):
        ficha = get_object_or_404(Ficha, id=ficha_id)
        nivel_classe = get_object_or_404(
            NivelClasseFicha, ficha=ficha, classe_id=classe_id
        )

        # Remove a classe e diminui o nível do personagem
        nivel_classe.delete()
        ficha.nivel -= nivel_classe.nivel
        ficha.save()

        messages.success(
            request,
            f"Classe {nivel_classe.classe.nome} removida! Níveis perdidos: {nivel_classe.nivel}.",
        )
        return redirect("escolher_subir_nivel", ficha_id=ficha.id)


@method_decorator(csrf_exempt, name="dispatch")
class AtualizarOutrosView(View):
    def post(self, request, ficha_id, *args, **kwargs):
        ficha = get_object_or_404(Ficha, id=ficha_id)
        data = json.loads(request.body)

        # Atualiza apenas o campo enviado
        if "ca" in data:
            ficha.ca = int(data["ca"])
        if "cd" in data:
            ficha.cd = int(data["cd"])
        if "deslocamento" in data:
            ficha.deslocamento = data["deslocamento"]
        if "tamanho" in data:
            ficha.tamanho = data["tamanho"]

        ficha.save()

        return JsonResponse({"status": "success"})


@method_decorator(
    csrf_exempt, name="dispatch"
)  # Para permitir requisições AJAX sem CSRF Token (se necessário)
class AtualizarFichaView(View):
    def post(self, request, ficha_id, *args, **kwargs):
        ficha = get_object_or_404(Ficha, id=ficha_id)

        try:
            data = json.loads(request.body)
            ficha.vida_atual = int(data.get("vida_atual", ficha.vida_atual))
            ficha.mana_atual = int(data.get("mana_atual", ficha.mana_atual))
            ficha.save()

            return JsonResponse(
                {
                    "status": "success",
                    "vida_atual": ficha.vida_atual,
                    "mana_atual": ficha.mana_atual,
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@method_decorator(csrf_exempt, name="dispatch")
class AtualizarBonusView(View):
    def post(self, request, pericia_id, *args, **kwargs):
        pericia_treinada = get_object_or_404(PericiaTreinada, id=pericia_id)
        data = json.loads(request.body)
        pericia_treinada.bonus_adicional = int(data.get("bonus", 0))
        pericia_treinada.save()
        return JsonResponse(
            {"status": "success", "valor": pericia_treinada.calcularValor()}
        )


@method_decorator(csrf_exempt, name="dispatch")
class AtualizarAtributoChaveView(View):
    def post(self, request, pericia_id, *args, **kwargs):
        pericia_treinada = get_object_or_404(PericiaTreinada, id=pericia_id)
        data = json.loads(request.body)
        atributo_nome = data.get("atributo")
        atributo = Atributo.objects.get(nome=atributo_nome)
        atributo_ficha = AtributoFicha.objects.get(
            ficha=pericia_treinada.ficha, atributo=atributo
        )
        pericia_treinada.atributo_chave.set([atributo_ficha])
        pericia_treinada.save()
        return JsonResponse(
            {"status": "success", "valor": pericia_treinada.calcularValor()}
        )


@method_decorator(csrf_exempt, name="dispatch")
class AtualizarTreinamentoView(View):
    def post(self, request, pericia_id, *args, **kwargs):
        pericia_treinada = get_object_or_404(PericiaTreinada, id=pericia_id)
        data = json.loads(request.body)
        pericia_treinada.treinado = data.get("treinado", False)
        pericia_treinada.save()
        return JsonResponse(
            {"status": "success", "valor": pericia_treinada.calcularValor()}
        )


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o registro
            messages.success(request, "Registro realizado com sucesso!")
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class VisualizarPerfilView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "perfil/visualizar.html")


@method_decorator(login_required, name="dispatch")
class AlterarNomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "perfil/alterar_nome.html")

    def post(self, request, *args, **kwargs):
        novo_nome = request.POST.get("username")
        if novo_nome:
            request.user.username = novo_nome
            request.user.save()
            messages.success(request, "Nome alterado com sucesso!")
            return redirect("visualizar_perfil")
        else:
            messages.error(request, "O nome não pode estar vazio.")
        return render(request, "perfil/alterar_nome.html")


@method_decorator(login_required, name="dispatch")
class AlterarEmailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "perfil/alterar_email.html")

    def post(self, request, *args, **kwargs):
        novo_email = request.POST.get("email")
        if novo_email:
            request.user.email = novo_email
            request.user.save()
            messages.success(request, "E-mail alterado com sucesso!")
            return redirect("visualizar_perfil")
        else:
            messages.error(request, "O e-mail não pode estar vazio.")
        return render(request, "perfil/alterar_email.html")


@method_decorator(login_required, name="dispatch")
class AlterarSenhaView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "perfil/alterar_senha.html")

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Mantém o usuário logado após a alteração da senha
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("visualizar_perfil")
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return render(request, "perfil/alterar_senha.html")


@method_decorator(login_required, name="dispatch")
class ExcluirContaView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)  # Desloga o usuário antes de excluir a conta
        user.delete()  # Exclui o usuário
        messages.success(request, "Sua conta foi excluída com sucesso.")
        return redirect("index")  # Redireciona para a página inicial
