from django.db import models
from django.contrib.postgres.fields import ArrayField


# модели которые относятся к товарам для продажи

class Product(models.Model):
    """Товары магазина"""
    UNIT_OF_MEASUREMENT_CHOICES = (
        ('кг.', 'кг.'),
        ('гр.', 'гр.'),
        ('л.', 'л.'),
        ('мл.', 'мл.'),
        ('шт.', 'шт.'),
    )
    name = models.CharField(verbose_name='Название товара', max_length=150, blank=False, null=False)
    image = ArrayField(models.ImageField(verbose_name='Изображение товара', blank=True, upload_to='photos_products/Y/M/'))
    description = models.TextField(verbose_name='Описание товара')
    features = models.TextField(verbose_name='Ключевые особенности')
    composition = models.TextField(verbose_name='Состав')
    additives = models.TextField(verbose_name='Пищевые добавки')
    analysis = models.TextField(verbose_name='Гарантированный анализ')
    unit = models.CharField(verbose_name='Единица измерения', max_length=10, choices=UNIT_OF_MEASUREMENT_CHOICES,
                            blank=False)
    date_added = models.DateField(verbose_name='Дата добавления', auto_now_add=True)
    # options = models.JSONField(verbose_name='Варианты товара')
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    animal = models.ForeignKey('Animal', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Animal(models.Model):
    """Доступные типы животных для поиска товаров"""
    name = models.CharField(verbose_name='Название животного', max_length=20)
    image = models.ImageField(verbose_name='Изображение животного', blank=True, upload_to='photos_animal/Y/M/')

    class Meta:
        verbose_name = 'Тип животного'
        verbose_name_plural = 'Типы Животных'

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Бренды товаров доступные в магазине"""
    name = models.CharField(verbose_name='Название бренда', max_length=100)
    image = models.ImageField(verbose_name='Изображение бренда', blank=True, upload_to='photos_brand/Y/M/')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'БРЕНДЫ'

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """Тип/типы товара"""
    name = models.CharField(verbose_name='Тип товара', max_length=30, blank=False, null=False)
    is_active = models.BooleanField(verbose_name='Активно', default=True)

    def __str__(self):
        return self.name


class ProductOptions(models.Model):
    """Доступные фасовки для товара(разные фасовки по весу, объёму и тд. ...)"""
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Продукт')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    size = models.PositiveIntegerField(verbose_name='Объём/Масса/Штук', blank=False, null=False)
    count = models.PositiveIntegerField(verbose_name='Остаток на складе')
    is_active = models.BooleanField(verbose_name='Активно', default=True)

    def __str__(self):
        return f'{self.product.name}, {self.size}, {self.price}, {self.count}'


# остальные модели для отзывов, статей и тд.

class Article(models.Model):
    animals = models.ForeignKey(Animal, verbose_name='Название животного', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='Название статьи', max_length=200)
    description = models.TextField(verbose_name='Описание статьи')
    image = models.ImageField(verbose_name='Изображение статьи', blank=True, upload_to='photos_article/Y/M/')
    time_read = models.CharField(verbose_name='Время чтения статьи', max_length=50)
    date_added = models.DateField(verbose_name='Дата добавления статьи', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    class Meta:
        verbose_name = 'Полезная статья'
        verbose_name_plural = 'ПОЛЕЗНЫЕ СТАТЬИ'
        ordering = ['-date_added']

    def __str__(self):
        return self.title


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

