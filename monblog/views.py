from .models import Article
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from comments.forms import CommentForm  # ✅ Import du formulaire
from comments.models import Comment  # ✅ Import du modèle Comment

def article_detail(request, article_id):
    """Affiche un article spécifique avec ses commentaires ET un formulaire"""
    article = get_object_or_404(Article, id=article_id)
    
    # ✅ Récupère les commentaires APPROUVÉS de cet article
    commentaires = article.comments.filter(approuve=True)
    
    # ✅ Gestion du formulaire de commentaire
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Crée le commentaire mais ne sauvegarde pas encore
            commentaire = form.save(commit=False)
            
            # Associe l'article et l'auteur
            commentaire.article = article
            if request.user.is_authenticated:
                commentaire.auteur = request.user
            else:
                # Pour les utilisateurs anonymes, on pourrait créer un user "Anonyme"
                # Pour l'instant, on redirige vers la connexion
                messages.info(request, "Vous devez être connecté pour commenter.")
                return redirect('login')  # On créera cette vue plus tard
            
            # Sauvegarde le commentaire
            commentaire.save()
            
            messages.success(request, "Votre commentaire a été soumis et est en attente de modération.")
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()
    
    # Passe tout au template
    context = {
        'article': article,
        'commentaires': commentaires,
        'form': form,
    }
    
    return render(request, 'monblog/detail.html', context)