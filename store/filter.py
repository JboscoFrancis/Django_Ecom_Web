import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput
from .models import Product

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name = 'title', lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control ml-2','placeholder': 'search'}))
    class Meta:
        model = Product
        fields = ['category','title',]