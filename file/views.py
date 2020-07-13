import math, random, re
import smtplib
from datetime import datetime
from django.conf import settings
from django.contrib import messages, auth
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.template import RequestContext
from .models import Register

from django.core.mail import send_mail


# Create your views here.

def genrateOTP():
    digits = '0123456789'
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


otp = genrateOTP()
time = datetime.now()
print(time)


def home(request):
    return render(request, 'index.html')


def register(request):
    data = {'msg': '', 'success': ''}
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confrimpassword = request.POST['confrimpassword']
        user_type = request.POST.get('user_type', False)
        address = request.POST['address']
        contact = request.POST['contact']
        # print("=================================================================="+str(user_type))
        if user_type == "":
            data['msg'] = 'user_type cannot be empty'
            return JsonResponse(data)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)  # compiling regex
        mat = re.search(pat, password)  # searching regex
        # validating conditions
        if mat:
            pass #data['msg'] = 'Password is valid'  # messages.info(request, "Password is valid.")
        else:
            data['msg'] =' Password must be 6-20 character long <br> must contain an uppercase & lowecase & number & a special character'  # messages.info(request, "Password invalid !!")
            return JsonResponse(data)
            # return redirect('/register')
        if password == confrimpassword:
            if Register.objects.filter(email=email).exists():
                data['msg'] = 'email already exist '  # messages.info(request,'email already exist')
                return JsonResponse(data)
                # return redirect('register')
            elif Register.objects.filter(username=username).exists():
                data['msg'] = 'username already exists'  # messages.info(request,'username already exists')
                return JsonResponse(data)
                # return redirect('register')
            else:
                register_object = Register.objects.create(email=email, name=name, username=username, password=password,
                                                          user_type=user_type, address=address, contact=contact)
                register_object.save()

                data['success'] = 'registered successfully <br> your id : ' + str(
                    Register.objects.last().id)  # messages.info(request,'registered successfully')
                # messages.info(request,'your id: '+str(Register.objects.last().id))
        else:
            data['msg'] = 'password not matching'  # messages.info(request,'password not matching')
            return JsonResponse(data)
            # return redirect('register')

    else:
        return render(request, 'registration.html')
    return JsonResponse(data)  # return redirect('register')


def profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        resultsets = Register.objects.all()
        print(resultsets)
        for resultset in resultsets:
            if (resultset.username == username) and (resultset.password == password) and resultset.user_type == '1':
                messages.info(request, 'logged in as student')
                request.session['username'] = resultset.username
                request.session['userid'] = resultset.id
                return redirect('/user/home')
            elif (resultset.username == username) and (resultset.password == password) and (resultset.user_type == '2'):
                messages.info(request, 'logged in as department')
                request.session['username'] = resultset.username
                request.session['userid'] = resultset.id
                return redirect('/qr/home')
        else:

            messages.info(request, 'Invalid Credentials')
            return redirect('profile')

    else:
        return render(request, 'login.html')


def contact(request):
    return render(request, 'contact.html')


def forgetpass(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        # send_mail(subject,message,from_email,to_list,fail_silently=True)
        subject = '@no reply otp for password reset'
        message = 'please verify the otp to reset your password : ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return redirect('/changepass')

    else:
        return render(request, 'forget.html')


def changepass(request):
    if request.method == 'POST':
        recived_otp = request.POST['otp']
        userid = request.POST['userid']
        password = request.POST['password']
        confrimpassword = request.POST['confrimpassword']
        timer = datetime.now() - time
        timelimit = str(timer).split(':')
        print('timer====' + str(timer))
        if (int(timelimit[1]) < 10):
            if (recived_otp == otp):
                if (password == confrimpassword):
                    register_obj = Register.objects.get(id=userid)
                    register_obj.password = password
                    register_obj.save()
                    print('timer====' + str(timer))
                    return HttpResponse('password changed successfully')
                else:
                    messages.info(request, 'password does not match in confrim password')
            else:
                messages.info(request, 'otp entered is not correct')
        else:
            messages.info(request, 'otp expired')
        return redirect('/changepass')
    else:
        return render(request, 'changepass.html')
