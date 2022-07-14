import csv
from django.shortcuts import render
from .models import Product, Category, Brand, Animal, ProductOptions
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def import_csv(request):
    """Загрузка файла в базу данных"""
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            empexceldata = pd.read_csv("." + excel_file, encoding='utf-8')
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                # animal = Animal.objects.get(name=dbframe.brand)
                brand = Brand.objects.get(name=dbframe.brand)
                category = Category.objects.get(name=dbframe.category)
                # product = Product.objects.get_or_create(name=dbframe.name, animal_id=animal.id, brand_id=brand.id, category_id=category.id)
                product = Product.objects.update_or_create(name=dbframe.name, brand_id=brand.id, category_id=category.id)
                print(product, 'Объект')

                # pro = ProductOptions.objects.get(name=dbframe.options)
                # productoptions = ProductOptions.objects.update_or_create(article_number=dbframe.article_number, price=dbframe.price,)
                # print(productoptions, 'Опции')


            return render(request, 'importexcel.html', {'uploaded_file_url': uploaded_file_url})
    except Exception as identifier:
        print(identifier)
    return render(request, 'importexcel.html', {})


def export_csv(request):
    """Получение файла из базы данных"""
    if request.method == 'POST':
        response = HttpResponse(content_type='')
        response['Content-Disposition'] = 'attachment; filename="DB.xlsx"'  # Название файла для отправки
        writer = csv.writer(response)
        writer.writerow(['article_number', 'name', 'animal', 'brand', 'category', 'price']) #, 'stock_balance'
        # writer.writerow(['Артикул', 'Название товара', 'Тип животного', 'Бренд', 'Категория', 'Цена', 'Остаток'])
        users = Product.objects.all().values_list('options__article_number', 'name', 'animal__name', 'brand__name',
                                                  'category__name', 'options__price') #, 'options__stock_balance')
        for user in users:
            writer.writerow(user)
        return response
    return render(request, 'exportexcel.html')
