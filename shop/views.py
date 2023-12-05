from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'shop/index.html', context)


def check_buys_count():
    purchase_list = Purchase.objects.all()
    products_count_in_purchase_list = dict()
    for purchase in purchase_list:
        if purchase.product.name not in list(products_count_in_purchase_list.keys()):
            products_count_in_purchase_list[purchase.product.name] = 1
        else:
            products_count_in_purchase_list[purchase.product.name] += 1

    for key, value in products_count_in_purchase_list.items():
        if value % 10 == 0:
            product_object = Product.objects.filter(name=key).first()
            old_price = product_object.price
            Product.objects.filter(name=key).update(price=old_price + old_price * 0.15)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        check_buys_count()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
