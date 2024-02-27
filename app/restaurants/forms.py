from .models import Comment, Restaurant
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

"""
Definition of a Django form for Comment.

This form, `CommentForm`, is a ModelForm that allows users to submit comments
along with a user_rating for a particular item.

Attributes:
    user_rating (forms.DecimalField): A DecimalField for user rating input.
        It is constrained between 0 and 5.0 with a step of 0.1.
    Meta (class): Meta information about the form, including the model and fields.
        - model: Specifies the model associated with the form (Comment).
        - fields: Specifies the fields to be included in the form (comment_body, user_rating).
    widgets (dict): Customizes the rendering of form fields via widgets.
        - comment_body: Textarea widget for comment_body field with CSS class 'form-control'.
"""
class CommentForm(forms.ModelForm):
    user_rating = forms.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5.0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'})
    )
    class Meta:
        model = Comment
        fields = ('comment_body','user_rating',)
        widgets = {
            'comment_body' : forms.Textarea(attrs={'class':'form-control'}),
        }