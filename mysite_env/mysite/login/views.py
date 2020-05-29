from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib import messages
from .forms import captcha_form
from django.http import HttpResponse
from .models import registry,ticket,bought_ticket,admincode,modify
from datetime import datetime
from .send_sms import send_sms
from random import randint
import time

# Create your views here.

#创建登录界面函数，并且把网页返回给用户
def homepage(request):
    if request.GET.get('obj')is not None:
        context={'obj':request.GET.get('obj')}
        return render(request,'login/homepage.html',context)
    else:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/homepage.html', context)

def code_confirm(request):#根据用户输入的手机号给用户手机发送验证码
    if request.method=='GET':
        if time.time()>request.session.get('overtime',0):
            code = '%d' % randint(100000, 999999)#生成要发送的验证码
            request.session['code']=code
            request.session['resend_time'] = time.time()+60
            request.session['overtime'] = time.time() + 120
            phonenum=request.GET.get('phonenum') #获取用户输入的手机号
            print(phonenum)
            print(code)
            send_sms(str(phonenum),code) #给用户发送验证码
            info='验证码发送成功'
            return HttpResponse(info,content_type='text/text')
        else:
            info = '验证码发送失败'
            return HttpResponse(info, content_type='text/text')

def log_in(request):  #注意函数名不要和包重名
    if request.method=='POST':
        obj=registry.objects.filter(name=request.POST['name'],password=request.POST['password1'])#在数据库中验证用户名和密码是否匹配
        if obj.count()==0:
            form = captcha_form(request.POST)
            context = {'obj': request.POST['name'], 'form': form,'error':'用户名或密码错误(也可能未注册)!'}
            return render(request, "login/login.html",context)
        else:
            print(request.session.get('code'))
            if not request.session.get('code'):
                context={'obj':request.POST['name'],'error':"请先点击发送验证码"}
                print(context)
            elif time.time()>request.session['overtime']:
                context = {'obj': request.POST['name'], 'error': "验证码超时"}
                print(context)
            elif request.POST['code']!=str(request.session['code']):
                context = {'obj': request.POST['name'], 'error': "验证码输入错误"}
                print(context)
                return render(request, "login/login.html", context)  # 返回一个渲染网页给用户
            else:
                context = {'obj': request.POST['name'],'tip':'恭喜你登陆成功'}
                return render(request,"login/homepage.html",context) #点击提交时回到首页并且把用户名传给首页
    else:
        return render(request, "login/login.html")  #返回一个渲染网页给用户

def log_out(request):  #注意函数名不要和包重名

    return redirect("login:首页")

def register(request):  #注意函数名不要和包重名
    if request.method == 'POST':
        name=request.POST['name'] #不允许名字重复
        test =registry.objects.filter(name=name)

        if test.count()!=0:  #证明此时重名
            return render(request, "login/register.html",{'error':'该用户名已经存在!'})

        password1=request.POST['password1']
        password2 = request.POST['password2']

        if password2!=password1:
            return render(request, "login/register.html", {'error': '请输入两次相同的密码!'})

        email=request.POST['email']
        registry.objects.create(name=name,password=password1,email=email)
        obj =name
        context={'obj':obj}
        return render(request,'login/homepage.html',context)#传参过去注册之后自动登录进入主页
    return render(request,"login/register.html")


def user_center(request):#进入个人中心
    if request.GET.get('obj') is None:  # 证明此时用户还没有登陆
        context = {'error': '监测到您还未登录，请先登录。'}
        return render(request, 'login/user_center.html', context)
    obj=request.GET.get('obj')
    print(obj)
    #从数据库获取该用户的全部信息并且显示出来
    detail=registry.objects.filter(name=obj)
    context={'obj':obj,'detail':detail}
    print(detail)
    return render(request,'login/user_center.html',context)

def base(request):#进入首页
    return render(request,'login/base.html')


def edit_profile(request):#编辑个人信息
    if request.GET.get('obj') is None:  # 证明此时用户还没有登陆
        context = {'error': '监测到您还未登录，请先登录。'}
        return render(request, 'login/user_center.html', context)

    obj = request.GET.get('obj')
    print(obj)
    detail = registry.objects.filter(name=obj)  #filter可以用for遍历,get不行
    print(detail)
    if request.method=='GET':
        context = {'obj': obj , 'detail':detail}
        return render(request,'login/edit_profile.html',context)

    if request.method == 'POST':
        email=request.POST['email']
        password1=request.POST['password1']
        password2= request.POST['password2']
        if password1!=password2:
            context={'detail':detail,'obj':obj,'error':'请输入两次相同的密码。'}
            return render(request, 'login/edit_profile.html', context)
        else:
            oupdate=registry.objects.get(name=obj)
            oupdate.email=email
            oupdate.password1=password1
            oupdate.password2 = password2
            oupdate.save()
            context = {'detail': detail, 'obj': obj, 'tip': '恭喜你修改信息成功。'}
        return render(request, 'login/edit_profile.html',context )
    else:
        context = {'detail': detail, 'obj': obj}
    return render(request,'login/edit_profile.html',context)

@login_required(login_url='login:登录')
def change_password(request):#修改个人密码
    if request.method == 'POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect("login:登录") #改完密码一般要求重新登录
    else:
        form=PasswordChangeForm(user=request.user)
    context={'form': form,'user':request.user}
    return render(request,'login/change_password.html',context)

def ticket_information(request):
    if request.GET.get('obj') is None:  # 证明此时用户还没有登陆
        context = {'tip': '监测到您还未登录，请先登录。'}
        return render(request, 'login/ticket.html', context)
    obj = request.GET.get('obj')
    if request.method=='GET':
        obj=request.GET.get('obj')
        print(obj)
        #获取数据库ticket中的全部数据并显示出来
        detail=ticket.objects.all()
        context = {'obj': obj,'detail':detail}  # 获取用户名
        return render(request,'login/ticket.html',context)
    if request.method=='POST':
        src=request.POST['src']
        det=request.POST['det']
        date=request.POST['date']
        print(src)
        print(det)
        print(date)
        detail=ticket.objects.filter(src=src,det=det,date=date)
        if detail.count()==0:  #证明没有这条信息
            context = {'obj': obj, 'tip': '抱歉，当前没有查到该票信息'}  # 获取用户名
            return render(request, 'login/ticket.html', context)
        else:
            context = {'obj': obj,'detail':detail}  # 获取用户名
            return render(request,'login/ticket.html',context)

def buy_information(request):#进行详细的购买操作,进行车票表的改操作，在购买表增加一条新纪录
    if request.GET.get('obj') is None: #证明此时用户还没有登陆
        context={'tip':'监测到您还未登录，请先登录。'}
        return render(request,'login/ticket.html',context)

    print(request.GET.get('obj'))#用户名
    print(request.GET.get('tid'))#车票编号

    tid=request.GET.get('tid') #车号
    name = request.GET.get('obj')  # 用户名

    detail=ticket.objects.filter(id=tid)

    context = {'obj': name, 'tid':tid,'detail':detail}  # 获取用户名
    if request.method=='GET':
        return render(request, 'login/buy_information.html',context)

    if request.method=='POST':
        type=request.POST['kind']  #购买的票类型
        num=int(request.POST['num'])  #数量
        realname = request.POST['realname']#真实姓名
        idnum=request.POST['idnum']#身份证号
        tupdate=ticket.objects.get(id=tid)#获取ticket的信息
        print(tupdate.soft)
        #根据不同的类型修改票的数量
        if type=='软卧':
            tupdate.soft = int(tupdate.soft) - int(num)
            result=tupdate.soft
        elif type=='硬卧':
            tupdate.hard = int(tupdate.hard) - int(num)
            result = tupdate.soft
        else :
            tupdate.hardseat = int(tupdate.hardseat) - int(num)
            result = tupdate.soft

        if result >= 0:#证明购买成功
            tupdate.save()
            # 存入新表
            bought_ticket.objects.create(tid=tid, tname=tupdate.name, tsrc=tupdate.src, tdet=tupdate.det,
                                         tdate=tupdate.date, type=type, num=num, name=name, realname=realname,
                                         idnum=idnum,buytime=datetime.now())
            context = {'obj': name, 'tid':tid,'tip':"恭喜你买票成功"}  # 获取用户名
            return render(request, 'login/homepage.html', context)
        else:
            detail=ticket.objects.all()
            context = {'obj': name, 'tid': tid, 'tip': "该票已经卖完，请重新选择！",'detail':detail}  # 获取用户名
            return render(request, 'login/ticket.html', context) #重新返回车票信息网页





def bought_information(request):#查看到已经卖到的车票并能在这个页面进行退票
    obj=request.GET.get('obj')
    if request.GET.get('id') is None: #证明这个时候还没有点击退票操作
        print(request.GET.get('obj'))#用户名
         #获取数据库ticket中的全部数据并显示出来，在前端渲染然后进行退票操作
        detail=bought_ticket.objects.filter(name=obj)
        context = {'obj': obj, 'detail': detail}  # 获取用户名
        if detail.count()==0:
            tip='您还没有购买任何车票。'
            context = {'obj': obj,'detail':detail,'error':tip}  # 获取用户名
        return render(request,'login/bought.html',context)

    if request.GET.get('id') is not None:#此时已经点击了退票操作，进行退票
        #获取post请求中的id 加上之前获取到的obj，进行数据库的删除操作
        print("正在退票")
        id=request.GET.get('id')
        bought_ticket.objects.filter(name=obj,id=id).delete()
        detail = bought_ticket.objects.filter(name=obj) #重新获取数据库数据
        tip='恭喜您，您已成功退票。'
        context = {'obj': obj, 'detail': detail, 'tip': tip}  # 获取用户名
        return render(request, 'login/bought.html', context)

def ticket_change(request):#车票修改
    obj = request.GET.get('obj')
    if obj is None:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/ticket_change.html', context)

    if request.method == 'GET':
        context = {'obj': obj}
        return render(request, 'login/ticket_change.html', context)
        # 进一步判断该用户是不是管理员，如果是的话才能修改票务信息
    if request.method == 'POST':
        #在管理员校验码表中查找是否有对应改管理员的校验码，有的话核对用户输入校验码和自己的一样不
        getcode = request.POST['code']
        admin=admincode.objects.filter(name=obj)  #获取该条记录
        if admin.count()==0:  #证明这个人不是管理员
            context = {'obj': obj, 'error': '由于您不是管理员，无法进行操作。'}
            return render(request, 'login/ticket_change.html', context)
        else:
            admin = admincode.objects.get(name=obj)  # 获取该条记录由于filter无法指定特殊字段，而且此表中name算是主键
            code = admin.check  # 获取这个管理员的校验码
            if getcode == code:  # 身份校验成功
                detail = ticket.objects.all()
                context = {'obj': obj, 'tip': '恭喜您，身份校验成功。', 'detail': detail}
                return render(request, 'login/ticket_change.html', context)
            else:
                context = {'obj': obj, 'error': '很遗憾，身份校验失败。'}
                return render(request, 'login/ticket_change.html', context)


def ticket_delete(request):  #车票删除
    obj = request.GET.get('obj')
    if obj is None:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/ticket_change.html', context) #车票删除后实则返回在车票修改的界面

    tid=request.GET.get('tid')
    if request.method == 'GET':
        #在车票表中删除这个票，重新渲染该页面，在删除之前先把记录保存在修改表中
        modify.objects.create(name=obj,tid=tid,type='删除车票')
        ticket.objects.filter(id=tid).delete()#删除该票
        detail=ticket.objects.all()
        context = {'obj': obj, 'tip': '恭喜您，车票删除成功。', 'detail': detail}
        return render(request, 'login/ticket_change.html', context)


def ticket_detail_change(request):#针对某一车票的具体修改
    obj = request.GET.get('obj')
    tid = request.GET.get('tid')
    if obj is None:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/ticket_detail_change.html', context)
    detail=ticket.objects.filter(id=tid)
    context = {'obj': obj,'tid':tid,'detail':detail}

    if request.method=='GET':
         return render(request, 'login/ticket_detail_change.html', context)

    if request.method=='POST':
        t=ticket.objects.get(id=tid)
        name=request.POST['tname']
        src=request.POST['src']
        det=request.POST['det']
        date=request.POST['date']
        soft = request.POST['soft']
        softprice = request.POST['softprice']
        hard = request.POST['hard']
        hardprice = request.POST['hardprice']
        hardseat = request.POST['hardseat']
        hardseatprice = request.POST['hardseatprice']
        t.name=name
        t.src=src
        t.det=det
        t.date=date
        t.soft=soft
        t.softprice=softprice
        t.hard = hard
        t.hardprice = hardprice
        t.hardseat = hardseat
        t.hardseatprice = hardseatprice
        t.save()
        #打开修改表，将管理员名字和修改的车号，车型都记录下来
        modify.objects.create(name=obj,tid=tid,type='修改车票')
        context = {'obj': obj, 'tid': tid, 'detail': detail,'tip':'恭喜您，修改车票信息成功。'}
        return render(request, 'login/ticket_detail_change.html', context)


def ticket_create(request):#新增车票
    obj = request.GET.get('obj')
    if obj is None:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/ticket_create.html', context)

    if request.method=='GET':
        context = {'obj':obj}
        return render(request, 'login/ticket_create.html', context)

    if request.method == 'POST':
        name = request.POST['tname']
        src = request.POST['src']
        det = request.POST['det']
        date = request.POST['date']
        soft = request.POST['soft']
        softprice = request.POST['softprice']
        hard = request.POST['hard']
        hardprice = request.POST['hardprice']
        hardseat = request.POST['hardseat']
        hardseatprice = request.POST['hardseatprice']
        ticket.objects.create(name = name,src = src,det = det,date = date,soft = soft,softprice = softprice,hard = hard,hardprice = hardprice,hardseat = hardseat,hardseatprice = hardseatprice)
        tdetail=ticket.objects.last()#获取最近一条数据就是刚增加的车号
        tid=tdetail.id
        # 打开修改表，将管理员名字和修改的车号，车型都记录下来
        modify.objects.create(name=obj, tid=tid,type='新增车票')
        context = {'obj': obj, 'tip': '恭喜您，新增车票信息成功。'}
        return render(request, 'login/ticket_create.html', context)



def modify_detail(request):
    obj=request.GET.get('obj')
    if obj is not None:
        detail=modify.objects.filter(name=obj)
        if detail.count()==0:
            context={'obj':obj,'error':'当前查不到该您的修改记录或您不是管理员。'}
            return render(request,'login/modify_detail.html',context)
        else:
            #把这个管理员的信息也查出来
            admin=admincode.objects.filter(name=obj)
            context = {'obj': obj, 'tip': '该管理员的修改记录如下。','detail':detail,'admin':admin}
            return render(request, 'login/modify_detail.html', context)
    else:
        context = {'error': '注意，检测到您还未登录，请先登录'}
        return render(request, 'login/modify_detail.html', context)