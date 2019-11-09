from django.urls import include, path
from rest_framework import routers
from TestApp import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from django.conf import settings


from django.conf.urls.static import static



schema_view = get_swagger_view(title="Baana-Baana API Documentation")


# Ajout des URLs pour l'accés à  l'API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testApp/', include('TestApp.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view),
    path('documentation/', include_docs_urls(title='Baana-Baana API')),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)