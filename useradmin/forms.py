from core.models import Product, Category
from django import forms


class AddProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Type here', 
            'class': 'form-control'
        }
    ))

    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))

    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'Type here', 
            'class': 'form-control'
        }
    ))

    price = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'Sale price', 
            'class': 'form-control'
        }
    ))

    old_price = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'Old price', 
            'class': 'form-control'
        }
    ))

    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Product tags', 
            'class': 'form-control'
        }
    ))

    product_status = forms.ChoiceField(
        choices=Product.STATUS,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
        )

    stock_count = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'How many?',
            'class': 'form-control'
        }
    ))

    digital = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        ))
    featured = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
                'class': 'form-check-input'
            }
    ))

    product_type = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'eg: organic',
            'class': 'form-control'
        }
    ))

    life = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'How long?',
            'class': 'form-control'
        }
    ))

    manufactured = forms.DateTimeField(
        input_formats=['%d/%m/%y'],
        widget=forms.DateTimeInput(
            format='%d/%m/%y',
            attrs={
                'placeholder': 'eg: 20/07/24',
                'class': 'form-control'
            }
        ))

    class Meta:
        model = Product
        fields = [
                'category',
                'title',
                'image',
                'description',
                'price',
                'old_price',
                'specifications',
                'tags',
                'product_status',
                'status',
                'featured',
                'digital',
                'stock_count',
                'product_type',
                'manufactured',
                'life',
            ]
