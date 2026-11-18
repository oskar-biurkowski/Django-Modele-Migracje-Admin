from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "is_available", "description"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if name.lower() in {"test", "asdf"}:
            raise forms.ValidationError("Wpisz prawdziwą nazwę produktu, a nie 'test'!")
        return name


class SearchForm(forms.Form):
    q = forms.CharField(label="Szukaj", required=False, max_length=50)
    only_available = forms.BooleanField(label="Tylko dostępne", required=False)
