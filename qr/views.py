from django.shortcuts import render,redirect,HttpResponse
import qrcode
from .models import update
from django.apps import apps
from django.contrib import messages
from functools import wraps
import cv2
import numpy as np
from pyzbar.pyzbar import decode
Register=apps.get_model('file','Register')
Path=apps.get_model('user','Path')
Department=apps.get_model('user','Department')
# Create your views here.

def login_decorator(orignal_func):
    @wraps(orignal_func)
    def wrapper(request,*args,**kwargs):
        username=request.session.get('username')
        if( username is not None):
           return orignal_func(request,*args,**kwargs)
        else:
            return redirect('/login')
    return wrapper

def afterlogin_decorator(orignal_func):
    @wraps(orignal_func)
    def wrapper(request,*args,**kwargs):
        userid=request.session['userid']
        register_obj=Register.objects.get(id=userid)
        user_type=register_obj.user_type
        if(user_type=='1'):
            url=request.get_full_path().split('/')
            if(url[1]== 'qr'):
                return redirect('/user/home')
            else:
                return orignal_func(request,*args,**kwargs)
        else:
            return orignal_func(request, *args, **kwargs)
    return wrapper

@afterlogin_decorator
@login_decorator
def home(request):
    if request.method=='POST':
        file_id=request.POST['file_id']
        try:
          resultset=update.objects.get(id=file_id)
          if(resultset.image_qr is not None):
              return render(request,'deptprofile.html',{'resultset':resultset,'username':request.session['username']})
          else:
              messages.info(request,'please genrete Qr')
        except:
            messages.info(request,'file id not exists genrate QR')


    else:
       return render(request,'deptprofile.html',{'username':request.session['username']})


@afterlogin_decorator
@login_decorator
def genrateqr(request):

    if request.method=='POST':
        userid=request.POST['userid']
        department=request.POST['department']
        status=request.POST['status']
        est_days=request.POST['range']
        file_type=request.POST['file_type']
        resultsets=update.objects.all()
        file_id=resultsets.last().id+1
        url='http://127.0.0.1:8000/qr/update/'+str(file_id)+"/"+str(department)+"/"
        qr=qrcode.make(url)
        img_location='media/pics/'+str(file_id)+".png"
        qr.save(img_location)
        try:
           update_object = update.objects.create(id=file_id,status=status, department=department, est_days=est_days,image_qr='pics/' + str(file_id) + ".png", User_id_id=userid,file_type=file_type)
           update_object.save()
           show_image=update.objects.get(id=resultsets.last().id)
           messages.info(request,'file status updates successfully')
           messages.info(request,'file id: '+str(file_id))
           messages.info(request, 'file type: ' + str(file_type))
           return render(request,'genrateqr.html',{'update':show_image })
        except:
            messages.info(request,'unable to create qr')
            return redirect('/qr/genrateqr')


    else:
        return render(request,'genrateqr.html')

@afterlogin_decorator
@login_decorator
def scanqr(request):
    count=0
    cap=cv2.VideoCapture(0)#this 0 is id
    cap.set(3,640)#setting width cap.set(width_id,width)
    cap.set(3, 640)#setting height cap.set(height_id,height)
    while count==0 :
        success,img=cap.read()
        for qrcode in decode(img):
            mydata = qrcode.data.decode('utf-8')
            print('mydata='+str(mydata))
            messages.info(request,mydata)
            count=count+1
        cv2.imshow('Result',img)
        cv2.waitKey(1)#this 1ms wait

    cap.release()
    cv2.destroyAllWindows()
    return redirect(mydata)

    return HttpResponse('qr not able scanned')


@afterlogin_decorator
@login_decorator
def updatefile(request,id,department):

        obj=update.objects.get(id=id)
        path=Path.objects.get(id=obj.file_type)
        l=list(path.dept_sequence)
        #l.info(request,l)
        return render(request,'update.html',{'id':id,'department':department,'file_type':obj.file_type})

@afterlogin_decorator
@login_decorator
def status(request,file_id):
      if request.method=='POST':
        department = request.POST['department']
        est_days = request.POST['range']
        status = request.POST['status']
        resultset = update.objects.get(id=file_id)
        path_obj=Path.objects.get(id=resultset.file_type)
        l=list(path_obj.dept_sequence)
        print(l)
        for i in l:
            print(i)
            department_obj=Department.objects.get(id=i)
            print(department)
            print(department_obj.dept_name)
            if(department.lower()==department_obj.dept_name.lower()):
                resultset.status = status
                resultset.department = department
                resultset.est_days = est_days
                try:
                  resultset.save()
                  messages.info(request, 'file updated successfully')
                  return redirect('/qr/home' )
                except Exception as e:
                  messages.info(request,'file not updated  something went wrong '+e)
                  return redirect('/qr/status/'+file_id)
        messages.info(request,'department not exists in path of file')
        return redirect('/qr/status/' + file_id)
      else:

            obj = update.objects.get(id=file_id)
            path = Path.objects.get(id=obj.file_type)
            return render(request,'update.html',{'id':file_id,'file_type':obj.file_type})

@login_decorator
def logout(request):
    if request.method=='POST':
       if  'yesbtn' in request.POST:
          try:
              del request.session['username']
              del request.session['userid']
          except:
              messages.info(request,'not able to logout')
       else:
           return redirect('/qr/home')

    return render(request,'logout.html')