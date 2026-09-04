from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("personagens", views.PersonagensView.as_view(), name="personagens"),
    path(
        "personagens/<int:ficha_id>/combate",
        views.FichaCombateView.as_view(),
        name="ficha_combate",
    ),
    path(
        "personagens/<int:ficha_id>/habilidades",
        views.FichaHabilidadesView.as_view(),
        name="ficha_habilidades",
    ),
    path(
        "ficha/<int:pk>/delete/", views.FichaDeleteView.as_view(), name="ficha_delete"
    ),
    path("ficha/nova/", views.CriarFichaView.as_view(), name="criar_ficha"),
    path(
        "ficha/<int:ficha_id>/atualizar/",
        views.AtualizarFichaView.as_view(),
        name="atualizar_ficha",
    ),
    path(
        "personagens/<int:ficha_id>/habilidades/adicionar/",
        views.AddHabilidadeView.as_view(),
        name="add_habilidade",
    ),
    path(
        "ficha/<int:ficha_id>/remove_habilidade/",
        views.RemoveHabilidadeView.as_view(),
        name="remove_habilidade",
    ),
    path(
        "escolher_subir_nivel/<int:ficha_id>/",
        views.EscolherSubirNivelView.as_view(),
        name="escolher_subir_nivel",
    ),
    path(
        "subir_nivel_classe_atual/<int:ficha_id>/",
        views.SubirNivelClasseAtualView.as_view(),
        name="subir_nivel_classe_atual",
    ),
    path(
        "adicionar_nova_classe/<int:ficha_id>/",
        views.AdicionarNovaClasseView.as_view(),
        name="adicionar_nova_classe",
    ),
    path(
        "subir_nivel_classe/<int:ficha_id>/<int:classe_id>/",
        views.SubirNivelClasseView.as_view(),
        name="subir_nivel_classe",
    ),
    path(
        "deletar_classe/<int:ficha_id>/<int:classe_id>/",
        views.DeletarClasseView.as_view(),
        name="deletar_classe",
    ),
    path(
        "atualizar_outros/<int:ficha_id>/",
        views.AtualizarOutrosView.as_view(),
        name="atualizar_outros",
    ),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "atualizar_bonus/<int:pericia_id>/",
        views.AtualizarBonusView.as_view(),
        name="atualizar_bonus",
    ),
    path(
        "atualizar_atributo_chave/<int:pericia_id>/",
        views.AtualizarAtributoChaveView.as_view(),
        name="atualizar_atributo_chave",
    ),
    path(
        "atualizar_treinamento/<int:pericia_id>/",
        views.AtualizarTreinamentoView.as_view(),
        name="atualizar_treinamento",
    ),
    path(
        "visualizar_perfil/",
        views.VisualizarPerfilView.as_view(),
        name="visualizar_perfil",
    ),
    path("alterar_nome/", views.AlterarNomeView.as_view(), name="alterar_nome"),
    path("alterar_email/", views.AlterarEmailView.as_view(), name="alterar_email"),
    path("alterar_senha/", views.AlterarSenhaView.as_view(), name="alterar_senha"),
    path("excluir-conta/", views.ExcluirContaView.as_view(), name="excluir_conta"),
]
