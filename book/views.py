from django.shortcuts import render,redirect,HttpResponse,reverse
from django.contrib.auth import authenticate,login,logout
from book.reg_login_forms.rgister_forms import Req_From
from book.reg_login_forms.login import login_from
from book.models import BookUser,Book,hits
#静态首页

def index (request):
    book_list=Book.objects.alias()[:22]
    return render(request,'home/index.html',locals())

def detail(request, id):
    bk = Book.objects.get(id=id)
    currentuser=request.user.id
    if currentuser:
        try:
            hit=hits.objects.get(userid=currentuser, bookid=id)
            hit.hitnum += 1
            hit.save()
        except hits.DoesNotExist:
            hit2 = hits()
            hit2.userid = currentuser
            hit2.bookid = id
            hit2.hitnum += 1
            hit2.save()
            print(hit2)
        data = str(currentuser)+'\t'+str(id)+'\t'+str(1)
        from hdfs import Client
        from utils import tools
        hdfs_path='/book/movie.txt'
        client=Client('http://node1:9870')
        tools.append_to_hdfs(client, hdfs_path ,data+'\n')
        return render(request,'home/detail.html',locals())
    else:
        return redirect(reverse('login'))

    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    # else:
    #     return render(request,'home/detail.html',locals())

from recommed import recommed
import redis
pool=redis.ConnectionPool(host='192.168.10.10',port=6379)
redis_client=redis.Redis(connection_pool=pool)

def recommend_book(request):
    if  request.user.is_authenticated:
        userid=request.user.id
        recommed.getRecommendByUseriID(userid,10)
        recommed_result=redis_client.get(userid)
        print(recommed_result)
        booklist=str(recommed_result).split('|')
        if booklist[0]!='None':
            bookset=[]
            for book in booklist[:-1]:
                book_id=book.split(',')[1]
                bk_info=Book.objects.get(id=book_id)
                bookset.append(bk_info)
                print(book_id)
                print("推荐电影信息",bookset)
            return render(request,'home/recommend.html',locals())
        else:
            bookset=Book.objects.order_by("rating")[:10]
            return render(request,'home/recommend.html',locals())
    else:
        return redirect(reverse('login'))

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms_l=login_from()
            return render(request,'auth/login.html',locals())
        elif request.method == 'POST':
            forms_l=login_from(request.POST)
            if forms_l.is_valid():
                user=forms_l.cleaned_data['user']
                pwd=forms_l.cleaned_data['pwd']
                user1=authenticate(request,username=user,password=pwd)
                if user1:
                    login(request,user1)
                else:
                    pwderr='用户名密码错误'
                    return render(request,'auth/login.html',locals())
                return redirect(reverse('index'))
            else:
                captcharr = "验证码错误"
                return render(request,'auth/login.html',locals())
    else:
        return render(request,'home/index.html')


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms = Req_From()
            return render(request, 'auth/register.html', locals())
        elif request.method == 'POST':
            forms = Req_From(request.POST)
            if forms.is_valid():
                user = forms.cleaned_data['username']
                pwd = forms.cleaned_data['pwd']
                gender = forms.cleaned_data['gender']
                birthday = forms.cleaned_data['birthday']
                phone = forms.cleaned_data['phone']
                BookUser.objects.create_user(username=user,password=pwd,gender=gender,birthday=birthday,phone=phone)
                return redirect(reverse('login'))
            else:
                return render(request, 'auth/register.html', locals())
    else:
        return HttpResponse("您已登录")

def log_out(reqrest):
    logout(reqrest)
    return redirect(reverse('index'))