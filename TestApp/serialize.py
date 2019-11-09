from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Articles,Louma,Zone,Categorie
from ai.models import CommonInfo



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','password')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['password'],
        )
        return user

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Erreur de connexion.")

class CategorieSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    categoriearticle = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model= Categorie    
        fields=('id','nomCategorie','imageCategorie','image_url','categoriearticle','descriptionCategorie')

    def get_image_url(self, obj):
        return obj.imageCategorie.url    


class ArticlesSerializer(serializers.ModelSerializer):
    created_by=CommonInfo.get_current_user
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model=Articles    
        fields=('id','nom','categorie','prix','image','image_url','louma','created_by')

    def get_image_url(self, obj):
        return obj.image.url

class LoumaSerializer(serializers.ModelSerializer):
    total_articles = serializers.IntegerField(read_only=True)
    articles = serializers.StringRelatedField(many=True, read_only=True)
    min_prix = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Louma
        fields = ( 'id','nom','jour' ,'zone','articles','total_articles','min_prix')

class ZoneSerializer(serializers.ModelSerializer):
    zone = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model= Zone   
        fields=('id','departement','description','zone')     


class LoumaMinSerializer(serializers.ModelSerializer):    
    articles = serializers.StringRelatedField(many=True, read_only=True)
    articlePlus = serializers.IntegerField()
    min_prix = serializers.IntegerField(read_only=True)

    class Meta:
        model = Louma
        fields = ( 'id','nom','jour' ,'zone','articles','articlePlus','min_prix')

  

class LoumaRechercheSerializer(serializers.ModelSerializer):
   
    articles = serializers.StringRelatedField(many=True, read_only=True)
    articleLesPlusPresents = serializers.IntegerField()
    
    class Meta:
        model = Louma
        fields = ( 'id','nom','jour' ,'localite','articles','articleLesPlusPresents')

                