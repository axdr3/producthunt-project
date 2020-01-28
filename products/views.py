from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.db import models

# Create your views here.
def home(request):
    # products = Product.objects.order_by('pub_date')
    products = Product.objects
    if request.method == 'POST':
        print('passou')
        most_voted = request.POST.get('most_voted')
        most_recent = request.POST.get('most_recent')
        print('valor de most_voted: {0}'.format(request.POST))
        if most_recent:
            products = products.order_by('-pub_date')
            print('passou2')
        elif most_voted:
            products = products.order_by('-votes_total')

    return render(request, 'products/home.html', {'products': products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        image = request.FILES.get('image')
        icon = request.FILES.get('icon')
        if title and body and url and image and icon:
            product = Product()
            product.populate(title, body, url, image, icon)
            if not product.isValidURL():
                return render(request, 'products/create.html', {'error': 'Invalid url.'})
            product.pub_date = timezone.datetime.now()
            product.pub_date_pretty()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are mandatory'})
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
