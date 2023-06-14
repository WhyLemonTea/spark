# from django.shortcuts import render
#
# # Create your views here.
# def upload(request):
#     return render(request,'utils/upload.html')

from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, HttpResponse
from dj import settings
from book.models import Book
import os

def handle_upload_file(name,file):
    path = os.path.join(settings.BASE_DIR, 'uploads')
    fileName = path+'/' + name
    print(fileName)
    with open(fileName, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    insertToSQL(fileName)
#0  1         2   +  3   +  4       5          6    7
#1,我不是药神,"徐峥,周一围,王传君",2018-07-05,9.6,img

def insertToSQL(fileName):
    txtfile = open(fileName, 'r', encoding='utf-8')
    for line in txtfile.readlines():
        try:
            bookinfo = line.split(',')
            a = bookinfo[0]
            b = bookinfo[1]
            c1 = bookinfo[2]
            c2=bookinfo[3]
            c3=bookinfo[4]
            c=c1[1:-1]+','+c2+','+c3[:-1]
            d = bookinfo[5]
            e= bookinfo[6]
            f= bookinfo[7]

            try:
                # bk_entry = book(name=name, price=price, url=url, publish=publish, rating=rating)
                # bk_entry.save()
                Book.objects.create(name=b, publish=c, introduction=d, rating=e, cover=f)
            except:
                print('save error' + id)
        except:
            print('read error ')



def importBookData(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse('None File uploads !')
        else:
            name = file.name
            handle_upload_file(name, file)
            return redirect(reverse('index'))
    return render(request, 'utils/upload.html')




if __name__ == '__main__':
    pass
