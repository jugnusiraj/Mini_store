from django.shortcuts import  render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from .models import Product,Cart,Order, OrderItem , Wishlist
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Sum



stripe.api_key = settings.STRIPE_SECRET_KEY




# Create your views here
def home(request):
    search = request.GET.get("search")

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    cart_count = 0

    if request.user.is_authenticated:
        cart_count = (
            Cart.objects.filter(user=request.user)
            .aggregate(total=Sum("quantity"))["total"] or 0
        )


    context = {
        "products": products,
        "cart_count": cart_count,
        
    }

    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):

    logout(request)

    return redirect("home")

@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    Cart.objects.create(
        user=request.user,
        product=product
    )

    return redirect("home")


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

@login_required
def remove_from_cart(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.delete()

    return redirect("cart")

@login_required
def update_quantity(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.quantity += 1

    item.save()

    return redirect("cart")

@login_required

def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    line_items = []

    for item in cart_items:

        line_items.append({
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": int(item.product.price * 100),
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=line_items,

        mode="payment",

        success_url=request.build_absolute_uri(
            reverse("success")
        ),

        cancel_url=request.build_absolute_uri(
            reverse("cancel")
        ),
    )

    return redirect(session.url)

# @login_required

# def success(request):

#     cart_items = Cart.objects.filter(user=request.user)

#     total = 0

#     for item in cart_items:
#         total += item.product.price * item.quantity

#     order = Order.objects.create(
#         user=request.user,
#         total_price=total,
#         status="Paid"
#     )

#     for item in cart_items:

#         OrderItem.objects.create(
#             order=order,
#             product=item.product,
#             total_price=item.product.price * item.quantity,
#             quantity=item.quantity,
#             status="paid"

#         )

    cart_items.delete()

    return render(request, "success.html")

@login_required
def success(request):
    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related("product")

    if not cart_items.exists():
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status="paid",
        payment_method="Card",
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    cart_items.delete()

    return render(
        request,
        "success.html",
        {"order": order},
    )

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-ordered_at")

    return render(request, "order_history.html", {
        "orders": orders
    })

@login_required
def cancel(request):

    return render(request, "cancel.html")

from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    context = {
        "product": product
    }

    return render(request, "product_detail.html", context)

from .models import Wishlist, Product

def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'items': items
    })

def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('home')
