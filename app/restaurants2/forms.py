from .models import Comment, Restaurant
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body','user_rating',)
        widgets = {
            'comment_body' : forms.Textarea(attrs={'class':'form-control'}),
        }