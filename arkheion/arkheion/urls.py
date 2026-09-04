from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from backend.views import (
    FichaViewSet,
    UserViewSet,
    CustomAuthToken,
    register_user,
    logout_user,
    user_profile,
    update_profile,
    # JWT Views
    CustomTokenObtainPairView,
    UserCreateAPIView,
    LogoutAPIView,
    CurrentUserAPIView,
    VerifyTokenAPIView,
    GoogleOAuthLoginView,
    # Homebrew ViewSets
    RacaViewSet,
    OrigemViewSet,
    DivindadeViewSet,
    ClasseViewSet,
    HabilidadeViewSet,
    AtaqueViewSet,
    # MesaViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Servir arquivos estáticos em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Documentação da API Arkheion",
        default_version="v1",
        description="Documentação interativa da API Arkheion",
        terms_of_service="https://swagger.io/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="Licença BSD"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"personagem", FichaViewSet, basename="personagem")
router.register(r"usuario", UserViewSet, basename="usuario")
# Homebrew content
router.register(r"racas", RacaViewSet, basename="racas")
router.register(r"origens", OrigemViewSet, basename="origens")
router.register(r"divindades", DivindadeViewSet, basename="divindades")
router.register(r"classes", ClasseViewSet, basename="classes")
router.register(r"habilidades", HabilidadeViewSet, basename="habilidades")
router.register(r"ataques", AtaqueViewSet, basename="ataques")
# router.register(r'mesa', MesaViewSet, basename='mesa')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("arkheion_api/", include(router.urls)),
    # Rotas de autenticação Token (mantidas para compatibilidade)
    path("arkheion_api/auth/login/", CustomAuthToken.as_view(), name="api_login"),
    path("arkheion_api/auth/register/", register_user, name="api_register"),
    path("arkheion_api/auth/logout/", logout_user, name="api_logout"),
    path("arkheion_api/auth/profile/", user_profile, name="api_profile"),
    path(
        "arkheion_api/auth/update-profile/", update_profile, name="api_update_profile"
    ),
    # Rotas de autenticação JWT (novas)
    path(
        "arkheion_api/auth/jwt/login/",
        CustomTokenObtainPairView.as_view(),
        name="jwt_login",
    ),
    path(
        "arkheion_api/auth/jwt/register/",
        UserCreateAPIView.as_view(),
        name="jwt_register",
    ),
    path("arkheion_api/auth/jwt/logout/", LogoutAPIView.as_view(), name="jwt_logout"),
    path(
        "arkheion_api/auth/jwt/user/",
        CurrentUserAPIView.as_view(),
        name="jwt_current_user",
    ),
    path(
        "arkheion_api/auth/jwt/token/refresh/",
        TokenRefreshView.as_view(),
        name="jwt_token_refresh",
    ),
    path(
        "arkheion_api/auth/jwt/token/verify/",
        VerifyTokenAPIView.as_view(),
        name="jwt_token_verify",
    ),
    # Rota de autenticação Google OAuth2
    path(
        "arkheion_api/auth/google/",
        GoogleOAuthLoginView.as_view(),
        name="google_oauth_login",
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
