from django.contrib.auth.models import User
from rest_framework import viewsets,generics, permissions
from TestApp.serialize import UserSerializer,RegisterSerializer,LoumaMinSerializer,ArticlesSerializer, LoginUserSerializer,LoumaSerializer,LoumaRechercheSerializer, ZoneSerializer,CategorieSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from knox.models import AuthToken
from .models import Articles,Louma,Zone,Categorie
from django.views.generic import ListView
from rest_framework.filters import OrderingFilter,SearchFilter
from django.db.models import Count , Min, Max, Q

from .permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint pour consuLter ou modifier les informations des utilisateurs.
    """
    serializer_class = UserSerializer
    queryset=User.objects.all()


class RegisterAPIView(generics.GenericAPIView):
    """
        API endpoint pour inscrire un utilisateur.
    """
    permission_classes=(IsAdminUser,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })         

class ArticlesView(viewsets.ModelViewSet):
    permission_classes=(IsOwnerOrReadOnly,)
    serializer_class = ArticlesSerializer
    queryset=Articles.objects.all()

    
class MinArticlesView(viewsets.ModelViewSet):
    serializer_class = ArticlesSerializer
    query =Articles.objects.all()
    queryset= query.order_by('-date_ajout')[:6]

class CategorieView(viewsets.ModelViewSet):
    """
        API endpoint pour consuLter ou modifier les informations des catégories seul l'administrateur peut le faire.
    """
    permission_classes=(IsAuthenticatedOrReadOnly,)
    serializer_class = CategorieSerializer
    queryset=Categorie.objects.all()   

class LoumaViewSet(viewsets.ModelViewSet):
    """
        API endpoint pour consuLter ou modifier les informations des loumas.
    """

    serializer_class = LoumaSerializer
    queryset=Louma.objects.annotate(
        total_articles=Count('articles'),
        min_prix = Min('articles__prix')
    )

class ZoneView(viewsets.ModelViewSet):
    """
        API endpoint pour consuLter ou modifier les informations des zones seul l'administrateur peut le faire.
    """
    permission_classes=(IsAuthenticatedOrReadOnly,)
    serializer_class = ZoneSerializer
    queryset = Zone.objects.all()      

class RechercheArticlesView(viewsets.ModelViewSet):
    """
        Permet la recherche du nombre d'articles dans chaque louma.
        On met le nom de l'article en question à la place du variable nom dans filter
    """
    serializer_class = LoumaRechercheSerializer
    queryset=Louma.objects.annotate(
        articleLesPlusPresents = Count('articles')
        
    )

class ArticleListView(generics.ListAPIView):
    """
        Permet la recherche du nombre d'articles dans chaque louma.
        On met le nom de l'article en question à la place du variable nom dans filter
    """      
  
    serializer_class = LoumaMinSerializer
    def get_queryset(self,*args,**kwargs):
        serializer_class = LoumaMinSerializer
        nom=self.request.GET.get('nom')
        nom='Mouton'
        return Louma.objects.annotate(
                articlePlus=Count('articles' , filter=Q(articles__nom=nom)),
                min_prix = Min('articles__prix' , filter=Q(articles__nom=nom))
                )
    

