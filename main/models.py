from ckeditor.fields import RichTextField
from django.db import models


# модели которые относятся к товарам для продажи

class Product(models.Model):
    """Товары магазина"""
    unique_name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    name = models.CharField(verbose_name='Название товара', max_length=150, blank=False, null=False)  # unique=True?
    description = RichTextField(verbose_name='Описание товара', null=True, blank=True)
    features = RichTextField(verbose_name='Ключевые особенности', null=True, blank=True)
    composition = RichTextField(verbose_name='Состав', null=True, blank=True)
    additives = RichTextField(verbose_name='Пищевые добавки', null=True, blank=True)
    analysis = RichTextField(verbose_name='Гарантированный анализ', null=True, blank=True)
    date_added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    image = models.ManyToManyField('ProductImage', verbose_name='Изображение товара', blank=True)
    animal = models.ManyToManyField('Animal', related_name='products', verbose_name='Тип животного', blank=True)
    brand = models.ForeignKey('Brand', related_name='products', verbose_name='Бренд', on_delete=models.PROTECT,
                              null=True, blank=True)
    category = models.ForeignKey('Category', related_name='products', verbose_name='Категория',
                                 on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'ТОВАРЫ'

    def __str__(self):
        return self.name

    def product_options(self):
        return self.options.count()

    product_options.short_description = 'Доступные фасовки'



    # def save(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     animals = ''
    #     for pet in self.animal.all():
    #         animals += pet.name
    #     self.unique_name = f'{animals} {self.category.name} {self.brand.name} {self.name}'
    #     super(Product, self).save()

    # def body_description(self):
    #     return u"%s..." % (self.description[:150],)
    #
    # body_description.short_description = 'Описание товара'


class ProductImage(models.Model):
    """Изображение товара"""
    image = models.ImageField(verbose_name='Изображение товара', blank=True, upload_to='photos_products/Y/M/')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'ИЗОБРАЖЕНИЕ ТОВАРА'

    # def __str__(self):
    #     return str(self.image)


class ProductOptions(models.Model):
    """Доступные фасовки для товара(разные фасовки по весу, объёму и тд. ...)"""
    article_number = models.CharField(verbose_name='Артикул товара', max_length=200, unique=True, blank=True, null=True)
    product = models.ForeignKey('Product', related_name='options', on_delete=models.PROTECT, verbose_name='Варианты')
    partial = models.BooleanField(verbose_name='На развес', default=False)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)  # 10 / 21/ 50 за 1 кг
    size = models.CharField(verbose_name='Объём/Масса/Штук', max_length=50, blank=False,
                            null=False)  # CharField = "150гр." / = 1кг / 500грамм
    stock_balance = models.PositiveIntegerField(verbose_name='Остаток на складе')
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, blank=True,
                                        null=True)  # TODO: later remove blank and null TRUE

    class Meta:
        verbose_name = 'Вариант фасовки'
        verbose_name_plural = 'ВАРИАНТЫ ФАСОВКИ'

    def __str__(self):
        return f'{self.product.name}, На развес {self.partial}, {self.size}, {self.price}, {self.stock_balance}'


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


# остальные модели для отзывов, статей и тд.

class Article(models.Model):
    title = models.CharField(verbose_name='Название статьи', max_length=200)
    animals = models.ForeignKey(Animal, verbose_name='Название животного', on_delete=models.PROTECT)
    description = RichTextField(verbose_name='Описание статьи')
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
        return u"%s..." % (self.description[:150],)

    body_description.short_description = 'Описание статьи'


# TODO: поля изменить в зависимости от формы отзыва
class Comments(models.Model):
    name_author = models.CharField(verbose_name='Автор отзыва', max_length=100)
    body_of_comment = models.TextField(verbose_name='Содержание отзыва')
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    date_added = models.DateField(verbose_name='Дата добавления отзыва', auto_now=True)
    published = models.BooleanField(verbose_name='Опубликовано', default=False)

    class Meta:
        verbose_name = 'Отзыв о магазине'
        verbose_name_plural = 'ОТЗЫВЫ О МАГАЗИНЕ'
        ordering = ['-date_added']

    def __str__(self):
        return f'Отзыв от {self.name_author}, номер телефона {self.phone_number}'


class Info(models.Model):
    """Информация о магазине - адрес, телефон, ст.метро и тд."""
    address = models.CharField(verbose_name='Адрес магазина', max_length=100, blank=True, null=True)
    metro = models.CharField(verbose_name='Станция метро', max_length=50, blank=True, null=True)
    time_weekdays = models.CharField(verbose_name='Время работы (будни)', max_length=50, blank=True, null=True)
    time_weekend = models.CharField(verbose_name='Время работы (выходные)', max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    social = models.TextField(verbose_name='Социальная сеть', help_text='Вставить ссылку страницы социальной сети',
                              blank=True, null=True)
    maps = models.TextField(verbose_name='Расположение на карте',
                            help_text='Вставить скрипт-ссылку с яндекс карты (размер 670х374)', blank=True)
    published = models.BooleanField(verbose_name='Опубликовано', default=True)

    class Meta:
        verbose_name = 'Информацию о магазине'
        verbose_name_plural = 'ИНФОРМАЦИЯ О МАГАЗИНЕ'

    def __str__(self):
        return f'Адрес: {self.address}, телефон: {self.phone_number}'
