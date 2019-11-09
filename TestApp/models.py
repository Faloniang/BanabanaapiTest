from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from ai.models import CommonInfo

class Zone(models.Model):
    departement=models.CharField(max_length=10)
    description=models.CharField(max_length=50)

    def __str__(self):
	    return '%s %s %s ' %(self.departement, '-', self.description)

class Categorie(models.Model):
    nomCategorie = models.CharField(max_length=20)
    descriptionCategorie = models.CharField(max_length=50)
    imageCategorie = models.ImageField(upload_to='images/',default='')

    def __str__(self):
	    return '%s %s %s' %(self.nomCategorie, '-', self.descriptionCategorie)

class Louma(models.Model):
    lun='Lundi'
    mar='Mardi'
    mer='Mercredi'
    jeu='Jeudi'
    ven='vendredi'
    sam='Samdi'
    dim='Dimanche'
    JOUR_CHOICES=[
        (lun,'Lundi'),
        (mar,'Mardi'),
        (mer,'Mercredi'),
        (jeu,'Jeudi'),
        (ven,'Vendredi'),
        (sam,'Samdi'),
        (dim,'Dimanche')
    ]
    nom = models.CharField(max_length=19)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,related_name='zone',default='')
    jour = models.CharField(max_length=10,choices=JOUR_CHOICES,default=lun)

    def __str__(self):
	    return '%s %s %s' %(self.nom,'-',self.zone)


class Articles(CommonInfo):
    louma = models.ForeignKey(Louma, on_delete=models.CASCADE, related_name='articles')
    nom = models.CharField(max_length=19)
    categorie=models.ForeignKey(Categorie, on_delete=models.CASCADE,related_name='categoriearticle')   
    prix=models.IntegerField()
    desc=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/',default='')    
    date_ajout=models.DateTimeField(auto_now_add=True)

    def __str__(self):
	    return '%s %s %s %s %s %s %s' %(self.nom,'-',self.categorie,'ajouté le ',self.date_ajout,'par ', self.created_by)
    
    
