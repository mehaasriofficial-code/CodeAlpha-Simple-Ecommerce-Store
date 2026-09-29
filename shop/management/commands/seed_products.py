from django.core.management.base import BaseCommand
from shop.models import Product


PRODUCTS = [
    {
        "name": "Wireless Headphones",
        "description": "Comfortable wireless headphones with clear sound.",
        "price": 1499,
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Smart Watch",
        "description": "Modern smart watch for daily fitness and notifications.",
        "price": 2499,
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Laptop Backpack",
        "description": "Water-resistant backpack with a laptop compartment.",
        "price": 999,
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight shoes suitable for running and everyday use.",
        "price": 1899,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=700&q=80",
    },
]


class Command(BaseCommand):
    help = "Create sample products for the e-commerce project."

    def handle(self, *args, **options):
        for data in PRODUCTS:
            Product.objects.update_or_create(
                name=data["name"],
                defaults=data,
            )
        self.stdout.write(self.style.SUCCESS("Sample products created/updated."))
