from ckeditor.fields import RichTextField
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.db import models


# модели которые относятся к товарам для продажи
class Product(models.Model):
    """Товары магазина"""
    POPULAR_CHOICES = (
        (0, 'Стандартный',),
        (1, 'Популярный',),
        (2, 'Очень популярный',),
    )
    name = models.CharField(verbose_name='Название товара', max_length=150, unique=True, blank=False, null=False)
    description = RichTextField(verbose_name='Описание товара', null=True, blank=True, config_name='default')
    features = RichTextField(verbose_name='Ключевые особенности', null=True, blank=True, config_name='default')
    composition = RichTextField(verbose_name='Состав', null=True, blank=True, config_name='default')
    additives = RichTextField(verbose_name='Пищевые добавки', null=True, blank=True, config_name='default')
    analysis = RichTextField(verbose_name='Гарантированный анализ', null=True, blank=True, config_name='default')
    date_added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    animal = models.ManyToManyField('Animal', related_name='products', verbose_name='Тип животного', blank=True)
    brand = models.ForeignKey('Brand', related_name='products', verbose_name='Бренд', on_delete=models.PROTECT,
                              null=True, blank=True)
    category = models.ForeignKey('Category', related_name='products', verbose_name='Категория',
                                 on_delete=models.PROTECT)
    min_price = models.DecimalField(verbose_name='Минимальная цена вариантов продукта', max_digits=8, decimal_places=2,
                                    null=True, blank=True)
    popular = models.IntegerField(verbose_name='Популярность', choices=POPULAR_CHOICES, default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'ТОВАРЫ'

    def __str__(self):
        return self.name

    # TODO: check it and make exceptions
    # def min_price_options(self):
    #     list_of_prices = []
    #     options = self.options.filter(partial=False).filter(is_active=True)
    #     print(options)
    #     if options:
    #         for option in self.options.all():
    #             list_of_prices.append(option.price)
    #         self.min_price = min(list_of_prices)
    #     elif not self.options.all():
    #         self.is_active = False
    #     else:
    #         self.min_price = self.options.price.first()

    # def save(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     # animals = ''
    #     # for pet in self.animal.all():
    #     #     animals += pet.name
    #     # self.unique_name = f'{animals} {self.category.name} {self.brand.name} {self.name}'
    #     self.min_price_options()
    #     super(Product, self).save()

    def product_options(self):
        return self.options.count()

    product_options.short_description = 'Доступные фасовки'


class ProductImage(models.Model):
    """Изображение товара"""
    product = models.ForeignKey('Product', related_name='images', verbose_name='Изображение товара',
                                on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение товара', blank=True, null=True,
                              upload_to='photos_products/Y/M/')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'ИЗОБРАЖЕНИЕ ТОВАРА'

    def __str__(self):
        return str(self.product.name)


class Units(models.Model):
    """Единицы измерения"""
    unit_name = models.CharField(max_length=50, verbose_name='Название Ед. измерения')

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = 'Еденица измерения'
        verbose_name_plural = 'ЕДИНИЦЫ ИЗМЕРЕНИЯ'


class ProductOptions(models.Model):
    """Доступные фасовки для товара(разные фасовки по весу, объёму и тд. ...)"""
    # UNIT_CHOICES = (
    #     (0, 'шт.',),
    #     # (1, 'литр'),
    #     (1, 'на вес',),
    # )
    article_number = models.CharField(verbose_name='Артикул товара', max_length=200, unique=True, blank=True, null=True)
    product = models.ForeignKey('Product', related_name='options', on_delete=models.CASCADE, verbose_name='Варианты')
    partial = models.BooleanField(verbose_name='На развес', default=False)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    size = models.CharField(verbose_name='Объём упаковки', max_length=50, blank=False, null=False)
    stock_balance = models.PositiveIntegerField(verbose_name='Остаток на складе')
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, blank=True,
                                        null=True)  # TODO: later remove blank and null TRUE

    units = models.ForeignKey('Units', related_name='prods', verbose_name='Единица измерения', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name, self.article_number}'

    class Meta:
        verbose_name = 'Вариант фасовки'
        verbose_name_plural = 'ВАРИАНТЫ ФАСОВКИ'
        ordering = ('partial', 'size',)

    # def save(self, *args, **kwargs):
    #     # if self.partial:
    #     #     self.size = '1000'
    #     #     self.unit = 1
    #     super(ProductOptions, self).save(*args, **kwargs)
    #     instance = Product.objects.get(id=self.product_id)
    #     instance.save()


class Animal(models.Model):
    """Доступные типы животных для поиска товаров"""
    name = models.CharField(verbose_name='Название животного', max_length=20, unique=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, upload_to='photos_animal/Y/M/')

    class Meta:
        verbose_name = 'Тип животного'
        verbose_name_plural = 'ТИПЫ ЖИВОТНЫХ'

    def __str__(self):
        return self.name

    def count_prod(self):
        return self.products.count()

    count_prod.short_description = 'Количество товаров'


class Brand(models.Model):
    """Бренды товаров доступные в магазине"""
    name = models.CharField(verbose_name='Название бренда', max_length=250, unique=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, upload_to='photos_brand/Y/M/')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'БРЕНДЫ'

    def __str__(self):
        return self.name

    def count_prod(self):
        return self.products.count()

    count_prod.short_description = 'Количество товаров'


class Category(models.Model):
    """Категории товаров"""
    name = models.CharField(verbose_name='Название категории', max_length=30, blank=False, null=False, unique=True)
    is_active = models.BooleanField(verbose_name='Активно', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'КАТЕГОРИИ'

    def __str__(self):
        return self.name

    def count_prod(self):
        return self.products.count()

    count_prod.short_description = 'Количество товаров'


# модели которые не относятся к товарам для продажи
class Article(models.Model):
    """Полезная статьи"""
    title = models.CharField(verbose_name='Название статьи', max_length=200)
    animals = models.ForeignKey(Animal, verbose_name='Название животного', on_delete=models.PROTECT)
    description = RichTextField(verbose_name='Описание статьи', config_name='custom')
    image = models.ImageField(verbose_name='Изображение', blank=True, upload_to='photos_article/Y/M/')
    time_read = models.CharField(verbose_name='Время чтения статьи', max_length=50)
    date_added = models.DateField(verbose_name='Дата добавления статьи', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    class Meta:
        verbose_name = 'Полезная статья'
        verbose_name_plural = 'ПОЛЕЗНЫЕ СТАТЬИ'
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def body_description(self):
        return f"%s..." % (self.description[:200],)

    body_description.short_description = 'Описание статьи'


class Comments(models.Model):
    """Отзыв о магазине"""
    name_author = models.CharField(verbose_name='Автор отзыва', max_length=100)
    body_of_comment = models.TextField(verbose_name='Содержание отзыва')
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, null=True, blank=True)
    name_animal = models.CharField(verbose_name='Имя питомца', max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    published = models.BooleanField(verbose_name='Опубликовано', default=False)

    class Meta:
        verbose_name = 'Отзыв о магазине'
        verbose_name_plural = 'ОТЗЫВЫ О МАГАЗИНЕ'
        ordering = ['-date_added']

    def __str__(self):
        return f'Отзыв от {self.name_author}, номер телефона {self.phone_number}'

    def body_description(self):
        return f"%s..." % (self.body_of_comment[:200],)

    body_description.short_description = 'Описание статьи'


class InfoShop(models.Model):
    """Информация о магазине - адрес, телефон, ст.метро и тд."""
    address = models.CharField(verbose_name='Адрес магазина', max_length=100, blank=True, null=True)
    metro = models.CharField(verbose_name='Станция метро', max_length=50, blank=True, null=True)
    time_weekdays = models.CharField(verbose_name='Время работы (будние)', max_length=50, blank=True, null=True)
    time_weekend = models.CharField(verbose_name='Время работы (выходные)', max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    social = models.TextField(verbose_name='Социальная сеть', help_text='Ссылка на страницу', blank=True, null=True)
    maps = models.TextField(verbose_name='Расположение на карте', help_text='Ссылка с яндекс карты (размер 670х374)',
                            blank=True)
    description_shop = RichTextField(verbose_name='Описание статьи', config_name='custom')
    published = models.BooleanField(verbose_name='Опубликовано', default=True)

    class Meta:
        verbose_name = 'О магазине'
        verbose_name_plural = 'О МАГАЗИНЕ'

    def __str__(self):
        return f'{self.address}, {self.metro}'


class Consultation(models.Model):
    """Консультация"""
    name = models.CharField(verbose_name='Имя', max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    date_added = models.DateTimeField(verbose_name='Дата обращения', auto_now_add=True)

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'КОНСУЛЬТАЦИЯ'

    def __str__(self):
        return f'{self.name}: {self.phone}'


class Customer(models.Model):
    """Покупатели"""
    customer_name = models.TextField(verbose_name='Имя покупателя', max_length=50, blank=True, null=True)
    phone_number = models.TextField(verbose_name='Номер телефона', max_length=13, blank=True, null=True, unique=True)
    first_order_date = models.DateTimeField(verbose_name='Дата первого заказа', auto_now_add=True)

    # TODO: Нужны ли ещё поля для учёта статистики

    class Meta:
        verbose_name = 'ПОКУПАТЕЛЬ'
        verbose_name_plural = 'ПОКУПАТЕЛИ'
        ordering = ('first_order_date',)

    def __str__(self):
        return f'{self.customer_name}: {self.phone_number}'


class Order(models.Model):
    """Заказы"""
    PAID_CHOICES = (
        (1, 'Да',),
        (0, 'Нет',),
    )
    customer = models.ForeignKey('Customer', verbose_name='Покупатель', related_name='order', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Время создания заказа', auto_now_add=True)
    paid = models.IntegerField(verbose_name='Оплачен', choices=PAID_CHOICES, default=0)

    # TODO: добавить цену на весь заказ?
    # TODO добавить кол-во товаров в заказе?

    class Meta:
        verbose_name = 'ЗАКАЗ'
        verbose_name_plural = 'ЗАКАЗЫ'
        ordering = ('-created',)

    def __str__(self):
        return f'Покупатель: {self.customer.customer_name}. Телефон: {self.customer.phone_number}. Заказ оплачен: {self.get_paid_display()}'


class OrderItem(models.Model):
    """Заказанные товары"""
    order = models.ForeignKey('Order', related_name='items', verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey('ProductOptions', to_field='article_number', verbose_name='Товар',
                                related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # TODO: нужна ли цена и надо ли просчитывать тут заказ

    def __str__(self):
        return 'Описание товара'
        # return f'{self.order}. Колличество товаров:{self.quantity}'

    class Meta:
        verbose_name = 'ЗАКАЗАННЫЙ ТОВАР'
        verbose_name_plural = 'ЗАКАЗАННЫЕ ТОВАРЫ'


# class MyAdminSite(AdminSite):
#     """Сортировка полей в Admin-Django"""
#     def get_app_list(self, request):
#         app_dict = self._build_app_dict(request)
#         app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
#         # TODO если надо сортировать по имени
#         # for app in app_list:
#         #    app['models'].sort(key=lambda x: x['name'])
#         return app_list
