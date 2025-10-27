from django.shortcuts import get_object_or_404, render
from .models import Article


# Create your views here.
def index(request):
    """Affiche la page d'accueil avec la liste des articles"""
    articles = Article.objects.all() #Recupere tout les articles

    #Envoie les articles au template
    return render(request, 'monblog/index.html', {'articles': articles})

def article_detail(request, article_id):
    """Affiche un article specifique en details"""
    # Recupere l'article ou renvoie une 404 si non trouvé
    article = get_object_or_404(Article, pk=article_id)

    #debug
    print(f"Article recuperer : {article}")
    print(f"Type : {type(article)}")
    print(f"ID : {article.id}")

    # Passe l'article au template
    return render(request, 'monblog/detail.html', {'article': article})