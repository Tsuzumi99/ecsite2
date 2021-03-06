from django.shortcuts import render
from django.shortcuts import render, redirect # 追加
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404, render, redirect 
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def index(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'app/index.html', {'products': products})
def signup(request):
    if request.method == 'POST':
       form = CustomUserCreationForm(request.POST)
       if form.is_valid():
           new_user = form.save()
           input_email = form.cleaned_data['email']
           input_password = form.cleaned_data['password1']
           new_user = authenticate(email=input_email,
password=input_password)
           if new_user is not None:
               login(request, new_user)
               return redirect('app:index')
    else:
       form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
       'product': product,
    }
    return render(request, 'app/detail.html', context)

@login_required

def fav_products(request):
    user = request.user
    products = user.fav_products.all()
    return render(request, 'app/index.html', {'products': products})
    
@require_POST
def toggle_fav_product_status(request):
    product = get_object_or_404(Product, pk=request.POST["product_id"])
    user = request.user
    if product in user.fav_products.all():
       user.fav_products.remove(product)
    else:
       user.fav_products.add(product)
    return redirect('app:detail', product_id=product.id)