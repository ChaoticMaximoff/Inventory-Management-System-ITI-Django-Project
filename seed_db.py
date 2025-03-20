import random
import os
from pathlib import Path
from django.core.files import File
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile

# Django setup
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import models
from accounts.models import User
from factories.models import Factory
from inventory.models import Product
from supermarkets.models import Supermarket
from orders.models import Order, OrderItem
from shipments.models import Shipment, ShipmentItem


def get_default_image():
    """Get the default product image"""
    static_path = os.path.join(
        settings.BASE_DIR, "static", "images", "default", "default_product.jpg"
    )
    with open(static_path, "rb") as f:
        return ContentFile(f.read(), name="default_product.jpg")


def clean_database():
    """Remove all data from tables"""
    print("Cleaning database...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    ShipmentItem.objects.all().delete()
    Shipment.objects.all().delete()
    Product.objects.all().delete()
    Factory.objects.all().delete()
    Supermarket.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()


def seed_database():
    """Seed database with sample data"""
    print("Seeding database...")

    # Create basic users
    manager = User.objects.create_user(
        username="manager1",
        password="password123",
        role="manager",
        email="manager@example.com",
        first_name="Manager",
        last_name="One",
    )
    employee = User.objects.create_user(
        username="employee1",
        password="password123",
        role="employee",
        email="employee@example.com",
        first_name="Employee",
        last_name="One",
    )

    # Generate 50 factories
    print("Creating factories...")
    factories = []
    cities = [
        "Cairo",
        "Alexandria",
        "Giza",
        "Shubra El Kheima",
        "Port Said",
        "Suez",
        "Luxor",
        "Mansoura",
        "El-Mahalla",
        "Tanta",
        "Asyut",
        "Ismailia",
        "Faiyum",
        "Zagazig",
        "Aswan",
        "Damietta",
        "Damanhur",
        "Minya",
        "Beni Suef",
        "Qena",
        "Sohag",
        "Hurghada",
        "6th of October",
        "Shibin El Kom",
        "Banha",
        "Kafr el-Sheikh",
        "Arish",
        "Mallawi",
        "10th of Ramadan",
        "Bilbais",
        "Marsa Matruh",
        "Idfu",
        "Mit Ghamr",
        "Al-Hamidiyya",
        "Desouk",
        "Qalyub",
        "Abu Kabir",
        "Kafr el-Dawwar",
        "Girga",
        "Akhmim",
        "Al-Qanayat",
        "Al-Qanater",
        "Al-Reef",
        "Al-Matareya",
        "Al-Marg",
        "Al-Khanka",
        "Al-Qanatir",
        "Al-Qusayr",
        "Al-Qusiyya",
        "Al-Qurnah",
    ]

    for i, city in enumerate(cities, 1):
        factories.append(
            Factory.objects.create(name=f"Factory {i} - {city}", location=city)
        )

    # Generate 50 products with default image
    print("Creating products...")
    products = []
    product_types = [
        "Milk",
        "Bread",
        "Rice",
        "Sugar",
        "Salt",
        "Oil",
        "Flour",
        "Coffee",
        "Tea",
        "Juice",
        "Water",
        "Soda",
        "Chips",
        "Cookies",
    ]
    brands = [
        "Premium",
        "Classic",
        "Gold",
        "Royal",
        "Fresh",
        "Natural",
        "Deluxe",
        "Special",
        "Elite",
        "Superior",
    ]

    default_image = get_default_image()
    used_product_names = set()

    i = 1
    while len(products) < 50:
        product_type = random.choice(product_types)
        brand = random.choice(brands)
        size = random.choice(["Small", "Medium", "Large", "Family Size"])
        name = f"{brand} {product_type} #{i} - {size}"

        if name not in used_product_names:
            products.append(
                Product.objects.create(
                    name=name,
                    quantity=random.randint(100, 5000),
                    critical_level=random.randint(50, 200),
                    image=default_image,
                )
            )
            used_product_names.add(name)
            i += 1

    # Generate 50 supermarkets
    print("Creating supermarkets...")
    supermarkets = []
    areas = [
        "Downtown",
        "Uptown",
        "West District",
        "East District",
        "North District",
        "South District",
        "Central",
        "Marina",
        "Garden City",
        "New Cairo",
        "6th October",
        "Maadi",
        "Zamalek",
        "Heliopolis",
        "Nasr City",
        "Dokki",
        "Mohandessin",
        "Giza",
        "Haram",
        "Faisal",
        "Shobra",
        "Ain Shams",
        "El Marg",
        "Helwan",
        "15th May",
        "El Shorouk",
        "El Rehab",
        "Madinaty",
        "El Obour",
        "Sheikh Zayed",
    ]

    chains = [
        "Carrefour",
        "Spinneys",
        "Metro",
        "Hyperone",
        "Seoudi",
        "BIM",
        "Kazyon",
        "Alfa Market",
        "Royal House",
        "Fresh Food Market",
    ]

    # Create a set to track used names
    used_names = set()

    # Ensure we create exactly 50 supermarkets with unique names
    i = 1
    while len(supermarkets) < 50:
        chain = random.choice(chains)
        area = random.choice(areas)
        name = f"{chain} #{i} - {area}"

        if name not in used_names:
            supermarkets.append(Supermarket.objects.create(name=name, location=area))
            used_names.add(name)
            i += 1

    # Generate shipments and orders
    print("Creating shipments and orders...")
    today = timezone.now().date()

    # Create 100 shipments (2 per factory)
    for factory in factories:
        for _ in range(2):
            # Create unconfirmed shipment first
            shipment = Shipment.objects.create(
                factory=factory,
                receive_date=today - timedelta(days=random.randint(1, 30)),
                created_by=manager,
                confirmed=False,  # Start as unconfirmed
            )

            # Add 5-8 random products to each shipment
            selected_products = random.sample(products, random.randint(5, 8))
            for product in selected_products:
                ShipmentItem.objects.create(
                    shipment=shipment,
                    product=product,
                    quantity=random.randint(50, 1000),
                )

            # Now confirm the shipment after adding all items
            shipment.confirmed = True
            shipment.save()

    # Create 150 orders (3 per supermarket)
    print("Creating orders...")
    for supermarket in supermarkets:
        for _ in range(3):
            try:
                # Create unconfirmed order first
                order = Order.objects.create(
                    supermarket=supermarket,
                    created_by_user=manager,
                    status=Order.PENDING,
                )

                # Add 4-7 random products to each order
                available_products = [
                    p for p in products if p.quantity >= 50
                ]  # Filter products with enough stock
                if (
                    len(available_products) >= 4
                ):  # Make sure we have enough products to create an order
                    selected_products = random.sample(
                        available_products,
                        random.randint(4, min(7, len(available_products))),
                    )

                    for product in selected_products:
                        # Ensure we don't exceed available stock
                        available_stock = product.quantity
                        if (
                            available_stock >= 50
                        ):  # Minimum threshold for creating an order
                            order_quantity = random.randint(
                                10, min(50, available_stock // 2)
                            )

                            OrderItem.objects.create(
                                order=order, product=product, quantity=order_quantity
                            )

                            # Update product stock
                            product.quantity -= order_quantity
                            product.save()

                    # Only confirm if order has items
                    if OrderItem.objects.filter(order=order).exists():
                        order.status = Order.CONFIRMED
                        order.save()
                    else:
                        # Clean up order if we couldn't add items
                        order.delete()
                        print(
                            f"Skipped order for {supermarket.name} - insufficient stock"
                        )

                else:
                    # Clean up order if we couldn't add items
                    order.delete()
                    print(f"Skipped order for {supermarket.name} - insufficient stock")

            except ValueError as e:
                print(f"Error creating order for {supermarket.name}: {str(e)}")
                continue

    print("\nDatabase seeded successfully!")
    print("Created records:")
    print(f"Factories: {Factory.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Supermarkets: {Supermarket.objects.count()}")
    print(f"Shipments: {Shipment.objects.count()}")
    print(f"Shipment Items: {ShipmentItem.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Order Items: {OrderItem.objects.count()}")


if __name__ == "__main__":
    clean_database()
    seed_database()
