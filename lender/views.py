from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import render, redirect

from .models import Lender
from product.models import Product
from .forms import ProductForm


def become_lender(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            lender = Lender.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'lender/become_lender.html', {'form': form})

@login_required
def lender_admin(request):
    lender = request.user.lender
    products = lender.products.all()
    return render(request, 'lender/lender_admin.html', {'lender': lender, 'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.lender = request.user.lender
            product.slug = slugify(product.title)
            product.save()

            return redirect('lender_admin')
    else:
        form = ProductForm()
    
    return render(request, 'lender/add_product.html', {'form': form})