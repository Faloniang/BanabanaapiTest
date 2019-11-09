from django.urls import include, path
from rest_framework import routers
from knox.views import LogoutView
from .views import RechercheArticlesView,UserViewSet,ArticlesView,CategorieView,LoumaViewSet,MinArticlesView,LoginAPI, RegisterAPIView,ArticleListView,ZoneView
#from django.contrib import admin


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticlesView)
router.register(r'louma', LoumaViewSet)
router.register(r'zone', ZoneView)
router.register(r'categorie', CategorieView)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [   
    path(r'', include(router.urls)),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPI.as_view()),
    path('articleRecherche', RechercheArticlesView.as_view({'get': 'list'})),
    path('articleLimit', MinArticlesView.as_view({'get': 'list'})),
    path('articless', ArticleListView.as_view()),
]