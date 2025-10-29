from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Formulaire pour ajouter un commentaire"""
    
    class Meta:
        model = Comment
        fields = ['contenu']  # ✅ Seul le contenu est saisi par le visiteur
        
        # Personnalisation des labels et help_text
        labels = {
            'contenu': 'Votre commentaire'
        }
        help_texts = {
            'contenu': 'Maximum 1000 caractères'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation du widget
        self.fields['contenu'].widget = forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Partagez votre avis...',
            'class': 'form-control'
        })