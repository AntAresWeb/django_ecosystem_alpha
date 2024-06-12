from io import BytesIO
from random import randint
from PIL import Image as PilImage, ImageDraw
from django.core.files import File
from django.core.management.base import BaseCommand

from products.models import (
    Category,
    Image,
    Product,
    ShoppingCart,
    Subcategory,
    User
)


def generate_image():
    width, height = 60, 40
    image = PilImage.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    coordinates = (
        randint(0, width // 2 - 1),
        randint(0, height // 2 - 1),
        randint(width // 2, width - 1),
        randint(height // 2, height - 1)
    )
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    draw.rectangle(coordinates, color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return buffer


class Command(BaseCommand):
    help = 'Заполнение таблиц БД тестовыми значениями'

    def get_random_object(self, model):
        count = model.objects.count()
        return model.objects.all()[randint(0, count - 1)]

    def handle(self, *args, **kwargs):
        self.stdout.write('Начато заполнение БД тестовыми значениями')
        Category.objects.all().delete()
        Image.objects.all().delete()
        Product.objects.all().delete()
        ShoppingCart.objects.all().delete()
        Subcategory.objects.all().delete()
        User.objects.filter(username__icontains='User').delete()

        self.stdout.write('Заполняются таблица пользователей')
        for i in range(3):
            user = User(
                email=f'user_{i}@fake.fk',
                username=f'User_{i}'
            )
            user.set_password('12345')
            user.save()

        self.stdout.write('Заполняются таблицы категорий и подкатегорий')
        for i in range(5):
            category = Category(
                name=f'Категория {i}',
                slug=f'cateory_{i}'
            )
            category.save()
            for j in range(randint(3, 5)):
                subcategory = Subcategory(
                    category=category,
                    name=f'Подкатегория-{i}-{j}',
                    slug=f'subcat_{i}_{j}'
                )
                subcategory.save()

        self.stdout.write('Заполняtтся таблица продуктов')
        for i in range(10):
            product = Product(
                subcategory=self.get_random_object(Subcategory),
                slug=f'product_{i}',
                name=f'Продукт № {i}',
                price=randint(100, 1000)
            )
            product.save()

        self.stdout.write('Заполняtтся таблица корзин')
        users = User.objects.filter(username__icontains='User')
        for owner in users:
            for i in range(randint(3, 10)):
                quantity = randint(1, 100)
                product = self.get_random_object(Product)
                try:
                    shoppingcart = ShoppingCart.objects.get(
                        owner=owner, product=product
                    )
                    shoppingcart.quantity += quantity
                except ShoppingCart.DoesNotExist:
                    shoppingcart = ShoppingCart(
                        owner=owner,
                        product=product,
                        quantity=quantity
                    )
                shoppingcart.save()

        self.stdout.write('Заполняtтся таблица изображений')
        products = Product.objects.all()
        for product in products:
            for i in range(3):
                file = File(generate_image())
                product_image = Image(product=product)
                product_image.file.save(
                    f'image-{product.slug}-{i}.jpg', file, save=True
                )
                product_image.save()
