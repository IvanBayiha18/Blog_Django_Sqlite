from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Article, Category, Tag #importe le model article

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = (
        'titre', 
        'auteur', 
        'categorie', 
        'statut_badge', 
        'date_publication', 
        'est_publie_maintenant'
    )
    list_filter = (
        'statut', 
        'categorie', 
        'tags', 
        'date_publication',
        'auteur'
    )
    list_editable = ('statut',)  # Édition rapide
    search_fields = ('titre', 'contenu', 'resume')
    date_hierarchy = 'date_publication'
    filter_horizontal = ('tags',)
    list_display = ('titre','auteur', 'categorie', 'statut', 'date_publication', 'est_publie_maintenant') #Ajoutez 'statut' ici
    list_display_links = ('titre',)
    
    # Configuration du formulaire d'édition
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'resume', 'contenu')
        }),
        ('Métadonnées', {
            'fields': ('auteur', 'categorie', 'tags', 'image_couverture')
        }),
        ('Publication', {
            'fields': (
                'statut', 
                'date_publication', 
                'date_publication_programmee'
            )
        }),
        ('SEO', {
            'classes': ('collapse',),  # Peut être replié
            'fields': ('meta_description',)
        }),
    )
    
    # Pré-remplissage automatique
    prepopulated_fields = {'slug': ('titre',)}
    
    # Actions personnalisées
    actions = ['publier_articles', 'depublier_articles']
    
    def statut_badge(self, obj):
        """Affiche le statut avec un badge coloré"""
        colors = {
            'brouillon': 'orange',
            'publie': 'green'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">{}</span>',
            colors.get(obj.statut, 'gray'),
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def est_publie_maintenant(self, obj):
        """Indique si l'article est actuellement publié"""
        if obj.est_publie:
            return format_html('✅ Publié')
        elif obj.date_publication_programmee:
            return format_html('⏰ Programmé')
        else:
            return format_html('📝 Brouillon')
    est_publie_maintenant.short_description = 'État'
    
    def publier_articles(self, request, queryset):
        """Action pour publier plusieurs articles"""
        updated = queryset.update(statut=Article.STATUT_PUBLIE)
        self.message_user(request, f"{updated} articles publiés avec succès.")
    publier_articles.short_description = "Publier les articles sélectionnés"
    
    def depublier_articles(self, request, queryset):
        """Action pour dépublier plusieurs articles"""
        updated = queryset.update(statut=Article.STATUT_BROUILLON)
        self.message_user(request, f"{updated} articles dépubliés.")
    depublier_articles.short_description = "Dépublier les articles sélectionnés"
    
    # Configuration par défaut
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Auteur par défaut = utilisateur connecté"""
        if db_field.name == "auteur":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'nombre_articles')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom', 'description')
    
    def nombre_articles(self, obj):
        return obj.article_set.count()
    nombre_articles.short_description = "Nombre d'articles"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'couleur', 'nombre_articles')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)
    
    def nombre_articles(self, obj):
        return obj.article_set.count()
    nombre_articles.short_description = "Nombre d'articles"