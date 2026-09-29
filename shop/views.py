from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def get_cart_items(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart_data.keys())
    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = max(1, int(cart_data.get(str(product.id), 1)))
        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    return items, total


def home(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "home.html", {"products": products, "query": query})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = min(int(cart.get(key, 0)) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.META.get("HTTP_REFERER", "home"))


def cart(request):
    items, total = get_cart_items(request)
    return render(request, "cart.html", {"items": items, "total": total})


def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = max(1, min(int(request.POST.get("quantity", 1)), product.stock))
    cart = request.session.get("cart", {})
    cart[str(product.id)] = quantity
    request.session["cart"] = cart
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")


@login_required
def checkout(request):
    items, total = get_cart_items(request)
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("home")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()

        if not full_name or not email or not address:
            messages.error(request, "Please fill all checkout fields.")
            return render(request, "checkout.html", {"items": items, "total": total})

        with transaction.atomic():
            for item in items:
                if item["quantity"] > item["product"].stock:
                    messages.error(request, f"Not enough stock for {item['product'].name}.")
                    return redirect("cart")

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                address=address,
                total_amount=total,
            )

            for item in items:
                product = Product.objects.get(pk=item["product"].pk)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=product.price,
                )
                product.stock -= item["quantity"]
                product.save(update_fields=["stock"])

        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed successfully.")
        return redirect("orders")

    return render(request, "checkout.html", {"items": items, "total": total})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "orders.html", {"orders": user_orders})


def cart_count(request):
    return sum(int(qty) for qty in request.session.get("cart", {}).values())
