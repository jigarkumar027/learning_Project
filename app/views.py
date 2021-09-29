from django.shortcuts import render,redirect
from .models import *
from random import randint
from .forms import *
from .utils import *
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
import socket
socket.getaddrinfo('localhost',8080)
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    try: 
        if request.session['id'] or request.session['email']:
            if request.POST['role'] == 'Student' :
                email = request.POST['email']
                user = User.objects.get(Email = email)
                name = user.Username

                return render(request,'app/index.html',{'name':name})
            else:
                return render(request,'app/index.html')
        else:
            return render(request,'app/index.html')
    except:
        form = myform()
        return render(request,'app/index.html',{'form':form})

def indexTutor(request):
    return render(request,'app/Tutor/index-2.html')

def registerpage(request):
    return render(request,'app/registerstudent.html')

def loginstudent(request):
    return render(request,'app/loginstudent.html')
    

def TutorRegister(request):
    return render(request,'app/TutorRegister.html')

def registerstudent(request):
    try:

       
        if request.POST['role'] == 'Student':
            role = request.POST['role']
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['psw']
            cpassword = request.POST['psw-repeat']
            contact = request.POST['contact']

            echeck = User.objects.filter(Email = email)
            if echeck:
                msg = 'User already Excist'
                return render(request,'app/registerstudent.html',{'msg':msg})

            else:
                if password == cpassword :
                    otp = randint(10000,99999)
                    ddata = User.objects.create(Username=name,Email = email,Password = password,Role = role,OTP=otp)
                    email_subject = "Student email : Account Vericication"
                    sendmail(email_subject,'mail_template',email,{'name':name,'otp':otp,'link':'http://localhost:8000/register/'})    
                        
                    sdata = Student.objects.create(user_id=ddata,Contact = contact)
                    return render(request,'app/otpvarify.html',{'email':email,'OTP':otp})
                else:
                    msg = 'Please Provide same Password'
                    return render(request,'app/registerstudent.html',{'msg':msg})

    except:
        return render(request,'app/registerstudent.html')


def otpstudent(request):
    hotp = request.POST['otp_var']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email = email)
    if user:
        uotp = user.OTP
        print(uotp)
        cotp = otp
        print(cotp)
        if str(uotp) == str(cotp):
            print('************************')
            print('varified')
            return render(request,'app/loginstudent.html')
        else:
            msg = 'OTP does Not match'
            return render(request,'app/otpvarify.html',{'msg':msg})
    else:
        message = 'User Does Not Exist'
        return render(request,'app/registerstudent.html',{'msg':message})

def loginvarifyS(request):
    if request.POST['role'] == 'Student' :
        email = request.POST['email']
        password = request.POST['psw']
        try:
            user = User.objects.get(Email = email)
        except:
            msg = 'please register yourself'
            return render(request,'app/registerstudent.html',{'msg':msg})

        if user:
            if user.Password == password and user.Role == 'Student':
                request.session['Role'] = user.Role
                request.session['id'] = user.id
                request.session['Password'] = user.Password
                request.session['Username'] = user.Username
                request.session['Email'] = user.Email
                name = user.Username
                return render(request,'app/index.html' ,{'name':name})
            else:
                msg = 'please provide valid password'
                return render(request,'app/loginstudent.html' ,{'msg':msg})

        else:
            return render(request,'app/registerstudent.html')

def student_profile(request):
    sid = request.session['id']
    try:
        sdata = Student.objects.get(user_id_id = sid)
        print(sdata)
        return render(request,'app/student_profile.html',{"key1":sdata})
    except:
        return render(request,'app/student_profile.html')

def student_data(request,pk):
    udata = User.objects.get(id = pk)
    if request.session['Email']:
        if udata.Role == "Student":
            sdata = Student.objects.get(user_id=udata)
            sdata.Firstname = request.POST['firstname']
            sdata.Lastname = request.POST['lastname']
            sdata.Email = request.POST['email']
            sdata.Contact = request.POST['contact']
            sdata.Address = request.POST['address']
            sdata.Gender = request.POST['gender']
            sdata.Qaulification = request.POST['qualification']
            sdata.DOB = request.POST['DOB']
            sdata.Country = request.POST['country']
            sdata.State = request.POST['state']
            sdata.City = request.POST['city']
            try:
                sdata.Profile_Pic = request.FILES['Pic']
                sdata.save()     
                name = udata.Username
                return render(request,'app/index.html',{'name':name})
            except:
                sdata.save()     
                name = udata.Username
                return render(request,'app/index.html',{'name':name})

def studentlogout(request):
    del request.session['Email'] 
    del request.session['Password'] 
    del request.session['id']
    request.session.modified = True
    #message = "Please login yourself" 
    return render(request,"app/index.html") 

def Tutorlogin(request):
    return render(request,'app/Tutorlogin.html')

def loginTutor_data(request):

    if request.POST['role'] == "Tutor":
        email = request.POST['email']
        password = request.POST['password']
        try :

            user = User.objects.get(Email=email)
            if user:
                if user.Password == password and user.Role == "Tutor":
                    stu = Tutor.objects.get(user_id=user)
                    request.session['Role'] = user.Role
                    request.session['id']  = user.id
                    request.session['Password'] = user.Password
                    request.session['Username'] = user.Username
                    request.session['Email'] = user.Email
                    
                    
                    return render(request,'app/Tutor/index-2.html')
                else:
                    message = "Please Provide valid Email Or Password"
                    return render(request,"app/TutorLogin.html",{'msg':message})
            else:
                message = "Please Register yourself"
                return render(request,"app/TutorRegister.html",{'msg':message})
        except :
            message = "Please Register yourself"
            return render(request,"app/TutorRegister.html",{'msg':message})
    else:
        print("Student")


def registerT(request):
    role = request.POST['role']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    contact = request.POST['contact']

    user = User.objects.filter(Email=email)
    if user:
        message = "User already Exist"
        return render(request,"app/TutorRegister.html",{'msg':message})
    else:
        if password == cpassword:
                otp = randint(10000,99999)
                newuser = User.objects.create(Username=username,Email=email,Password=password,Role=role,OTP=otp)   
                newstudent = Tutor.objects.create(user_id=newuser,Contact=contact)
                return render(request,"app/otpvarifyTutor.html",{'email':email})
        else:
                message = "Password and Cpassword not Match"
                return render(request,"app/TutorRegister.html",{'msg':message})

def OtpvarifyTotor(request):
    gotp = request.POST['gotp']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email=email)
    if user:
        a = user.OTP
        b = otp
        if str(a) == str(b):
            print('varified')
            return render(request,'app/Tutorlogin.html')
        else:
            message = "OTP doesnot MATCH"
            return render(request,"app/otpvarifyTutor.html",{'msg':message})
    else:
        message = "User Desnot Exist"
        return render(request,"app/TutorRegister.html",{'msg':message})

     
def addcourse(request):
    id = request.session['id']
    userd = User.objects.get(id = id)
    if userd.is_active == True:

        catdata = Category.objects.all()
        print('*****************************************')
        print(catdata)
        return render(request,'app/Tutor/add-courses.html',{'catname':catdata})
    else:
        return render(request,'app/Tutor/index-2.html')

def coursedata(request):
    id = request.session['id']
    tid = Tutor.objects.get(user_id = id)
    cname = request.POST['category'] 
    print('*************')
    print(cname)
    catid = Category.objects.get(id=cname)
    coursename = request.POST['coursename']
    coursedetail = request.POST['coursedetail']
    coursecode = request.POST['coursecode']
    cduration = request.POST['cduration']
    cprice = request.POST['cprice']
    cTechnology = request.POST['cTechnology']
    cPre_Requirment = request.POST['cPre_Requirment']
    cpic = request.FILES['cpic']
    cdata = Course.objects.create(Tutor_id = tid,Category_id = catid,Name = coursename,Code = coursecode,Description = coursedetail,Duration=cduration,Price=cprice,Technology=cTechnology,Pre_Requirment=cPre_Requirment,course_pic=cpic)
    return render(request,'app/Tutor/index-2.html')

def tutorlogout(request):
    del request.session['Email'] 
    del request.session['Password'] 
    del request.session['id']
    request.session.modified = True
    return render(request,"app/index.html") 

def shopgrid(request):
    try:
        if request.session['id'] and request.session['Email']:
            print(request.session['Username'])
            cdata = Course.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata})
    except:

        cdata = Course.objects.all()
        return render(request,'app/shop-grid.html',{'course':cdata})

    
def class_grid(request):
    try:
        if request.session['id'] and request.session['Email']:
            print(request.session['Username'])
            cdata = Course.objects.all()
            return render(request,'app/class-grid.html',{'course':cdata})
    except:
        cdata = Course.objects.all()
        return render(request,'app/class-grid.html',{'course':cdata})
    #return render(request,'app/class-grid.html')

def course_detail(request,pk):
    cdata = Course.objects.get(id=pk)
    return render(request,'app/class-details.html',{'course':cdata})


def admin(request):
    return render(request,'app/admin/index.html')

def cart(request,pk):
    try: 
        if request.session['id'] and request.session['Email']:
            if request.session['Role'] == 'Tutor':
                msg = "Please Login Yourself First as Student"
                cdata = Course.objects.all()
                return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
            sid = request.session['id']
            print(sid)
            print('LOGIN-----------------------')
            # print(pk)
            #1. sid = student
            sdata = Student.objects.get(user_id=sid)
            #2. pk = course_data 
            cdata = Course.objects.get(id = pk)
            print(cdata)
            try:
                ddata = Cart.objects.get(Course_id = cdata)
                msg = "The Item Is Already Added"
                cdata = Course.objects.all()
                return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
            except:
                
                cartdata = Cart.objects.create(Course_id = cdata,Student_id = sdata,total = cdata.Price,subtotal = cdata.Price)
                print('*/*/*/*/*/*/*/*/*/*///*')
                cartd = Cart.objects.filter(Student_id=sdata)
                
                tprice = 0
                for i in cartd:
                    tprice += i.total
                return render(request,'app/cart.html',{'cdata':cartd,'tprice':tprice})
        else:
            msg = "Please Login Yourself First"
            print('********##############***********')
            cdata = Course.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
    except:
        msg = "Please Login Yourself First"
        print('********##############***********')
        cdata = Course.objects.all()
        return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})


    
def cart_gen(request):
    try:
        if request.session['id'] and request.session['Email']:
                if request.session['Role'] == 'Tutor':
                    msg = "Please Login Yourself First as Student"
                    cdata = Course.objects.all()
                    return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
                sid = request.session['id']
                print(sid)
                print('LOGIN-----------------------')
                #1. sid = student
                sdata = Student.objects.get(user_id=sid)
                print(sdata)
                #2. pk = course_data 
                cartd = Cart.objects.filter(Student_id=sdata)
                print(cartd)
                tprice = 0
                for i in cartd:
                    print(i)
                    tprice += i.total


                return render(request,'app/cart.html',{'cdata':cartd,'tprice':tprice,'msg':''})
        else:
            msg = "Please Login Yourself First"
            print('********##############***********')
            cdata = Course.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
    except:
        msg = "Please Login YourselF First"
        print('********##############***********')
        return render(request,'app/index.html',{'msg':msg})

def cremove(request,pk):
    cd = Cart.objects.get(id=pk).delete()
    #dcdata = cd.objects.delete()
    cartd = Cart.objects.all()
    return render(request,'app/cart.html',{'cdata':cartd})

def checkout(request):
    sid = request.session['id']
    sdata = Student.objects.get(user_id=sid)
    print('******************',sdata)
    cartd = Cart.objects.filter(Student_id=sdata)
    tprice = 0
    for i in cartd:
        print(i)
        tprice += i.total
    request.session['Total'] = tprice
    return render(request,'app/checkout.html',{'sdata':sdata,'cartdetail':cartd,'tprice':tprice})

####### pay ##################################################
def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        print('-************')
        #amount = int(request.POST['sub_total'])
        amount =request.session['Total']
        print(amount)
        #amount = int(pk)
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print('*/*/*/*/*/*/*/')
        print(err)
        return render(request, 'app/cart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)

def welcome(request):
    # all_doc = User.objects.all()
    msg = 'Time Out'
    sid = request.session['id']
    print(sid)
    print('LOGIN-----------------------')
    #1. sid = student
    sdata = Student.objects.get(user_id=sid)
    #2. pk = course_data 
    cartd = Cart.objects.filter(Student_id=sdata)
    tprice = 0
    for i in cartd:
        tprice += i.total


    return render(request,'app/cart.html',{'cdata':cartd,'tprice':tprice,'msg':msg})
        

