import csv
from django.shortcuts import render
from .models import Product
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def import_csv(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file, 'Тип')
            empexceldata = pd.read_csv("." + excel_file, encoding='utf-8')
            # empexceldata = pd.read_csv(myfile, header=None)
            # empexceldata = pd.read_csv('ml-100k/u.data', usecols=[0, 1, 2, 3], names=excel_file,
            #                            encoding='latin-1', delim_whitespace=True, header=None)
            # empexceldata.columns = features

            # empexceldata = pd.read_csv(excel_file, names=["name"])
            # empexceldata.columns = features

            print(type(empexceldata), "Данные")
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                # fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                obj = Product.objects.create(id=dbframe.id, name=dbframe.name)
                                             # , animal=dbframe.animal,
                                             # brand=dbframe.brand, category=dbframe.category)
                obj.save()
            return render(request, 'importexcel.html', {'uploaded_file_url': uploaded_file_url})
    except Exception as identifier:
        print(identifier)
    return render(request, 'importexcel.html', {})


def export_csv(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="DB_info.xlsx"'
        writer = csv.writer(response)
        # writer.writerow(['Данные о продукте'])  #Название заголовка в таблице
        writer.writerow(['id', 'name', 'animal', 'brand', 'category', 'options'])
        users = Product.objects.all().values_list('id', 'name', 'animal__name', 'brand__name', 'category__name', 'options__id')
        for user in users:
            writer.writerow(user)
        return response
    return render(request, 'exportexcel.html')