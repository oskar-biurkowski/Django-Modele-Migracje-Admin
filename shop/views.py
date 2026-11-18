from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductForm, SearchForm
from .models import Product


def index(request):
    return render(request, "shop/index.html", {
        "project_name": "Sklep 4TP",
        "user_name": "Oskar"
    })


def product_list(request):
    form = SearchForm(request.GET)
    products = Product.objects.select_related("category")
    
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            products = products.filter(name__icontains=q)
        if form.cleaned_data.get("only_available"):
            products = products.filter(is_available=True)
            
    return render(request, "shop/product_list.html", {
        "products": products,
        "form": form
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shop:product_list")
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "title": "Nowy produkt"})


def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("shop:product_detail", product_id=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "title": f"Edycja: {product.name}"})


@require_POST
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect("shop:product_list")
