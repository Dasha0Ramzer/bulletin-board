
from django.contrib import admin
from django.urls import path

from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API для сайта объявлений",
        default_version='v1',
        description="""Backend для доски объявлений. 
        Реализована JWT-авторизация, роли (админ/пользователь), 
        CRUD для объявлений, отзывы и поиск по названию.""",
        terms_of_service="https://github.com/Dasha0Ramzer/bulletin-board",
        contact=openapi.Contact(email="kda2000.123@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
