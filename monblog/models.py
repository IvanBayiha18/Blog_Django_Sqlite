from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    """ Categori pour classer les articles """
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

class Tag(models.Model):
    """Tags pour etiqueter les articles"""
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    couleur = models.CharField(max_length=7, default='#3897f0')

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        

class Article(models.Model):
    # STATUTS DE PUBLICATION
    STATUT_BROUILLON = 'brouillon'
    STATUT_PUBLIE = 'publie'
    STATUT_CHOICES = [
        (STATUT_BROUILLON, 'Brouillon'),
        (STATUT_PUBLIE, 'Publié'),
    ]
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # Nouveau : URL propre
    contenu = models.TextField()
    resume = models.TextField(blank=True, help_text="Résumé court pour la page d'accueil")  # Nouveau
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # NOUVEAUX CHAMPS
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default=STATUT_BROUILLON
    )
    date_publication = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication_programmee = models.DateTimeField(  # Nouveau
        null=True, 
        blank=True,
        help_text="Si défini, l'article sera publié à cette date"
    )
    image_couverture = models.ImageField(  # Nouveau
        upload_to='articles/couverture/',
        null=True,
        blank=True,
        help_text="Image de couverture de l'article"
    )
    meta_description = models.CharField(  # Nouveau (SEO)
        max_length=300,
        blank=True,
        help_text="Description pour les moteurs de recherche"
    )
    
    # Relations existantes
    categorie = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        """URL canonique de l'article"""
        return reverse('article_detail', kwargs={'article_id': self.id})
    
    @property
    def est_publie(self):
        """Vérifie si l'article est publié"""
        if self.statut == self.STATUT_PUBLIE:
            if self.date_publication_programmee:
                return self.date_publication_programmee <= timezone.now()
            return True
        return False
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Article"
        verbose_name_plural = "Articles"