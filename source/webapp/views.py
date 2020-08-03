from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, Http404
from webapp.models import Product
from webapp.forms import ProductForm

def index_view(request):

    product = Product.objects.all()
    context = {
        'product': product
    }
    return render(request, 'index.html', context)


def product_create(request):
    if request.method == "GET":
        return render(request, 'product_create.html', context={
            'form': ProductForm()
         })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                amount=form.cleaned_data['amount'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description']
            )
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])



def product_view(request, pk):

    product = get_object_or_404(Product, pk=pk)

    context = {'product': product}
    return render(request, 'product_view.html', context)



def product_update(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            'name': product.name,
            'price': product.price,
            'amount': product.amount,
            'category':product.category,
            'description':product.description
        })
        return render(request, 'product_update.html', context={
            'form': form,
            'product': product
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.amount = form.cleaned_data['amount']
            product.category = form.cleaned_data['category']
            product.description = form.cleaned_data['description']
            product.save()
            return redirect('product_view',pk=product.pk)
        else:
            return render(request, 'product_update.html', context={
                'product': product,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])



def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
       return render(request, 'product_delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')