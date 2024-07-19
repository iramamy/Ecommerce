from django import forms
from .models import ProductReview

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholer': 'Write review',
            'style': 'resize: none;'
            }))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']