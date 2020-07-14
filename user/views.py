from django.shortcuts import render,redirect
from django.apps import apps
from django.contrib import messages
from functools import wraps
import cv2
from pyzbar.pyzbar import decode
from .models import Department,Path
# Create your views here.
Register=apps.get_model('file','Register')
update=apps.get_model('qr','update')

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
        if(user_type=='2'):
            url = request.get_full_path().split('/')
            print(request.get_full_path())
            print(url)
            if (url[1] == 'user'):
                return redirect('/qr/home')
            else:
                return orignal_func(request,*args,**kwargs)
        else:
            return orignal_func(request, *args, **kwargs)

    return wrapper

@afterlogin_decorator
@login_decorator
def home(request):
    if request.method=='POST':
       resultsets=update.objects.filter(User_id_id=request.session['userid'])
       return render(request, 'studprofile.html', {'username': request.session['username'],'resultsets':resultsets})
    else:
        return render(request,'studprofile.html',{'username':request.session['username']})

# @afterlogin_decorator
# @login_decorator
# def scanqr(request):
#     count=0
#     cap=cv2.VideoCapture(0)#this 0 is id
#     cap.set(3,640)#setting width cap.set(width_id,width)
#     cap.set(3, 640)#setting height cap.set(height_id,height)
#     while count==0 :
#         success,img=cap.read()
#         for qrcode in decode(img):
#             mydata = qrcode.data.decode('utf-8').split('/')
#             print(mydata)
#             messages.info(request,mydata)
#             count=count+1
#         cv2.imshow('Result',img)
#         cv2.waitKey(1)#this 1ms wait
#     cap.release()
#     cv2.destroyAllWindows()
#     return redirect('/user/'+str(mydata[5])+'/'+str(mydata[6]))
#
#     return HttpResponse('qr not able scanned')

@afterlogin_decorator
@login_decorator
def view(request):
    id=request.session['userid']
    resultset=update.objects.get(id=id)
    return render(request,'view.html',{'username':request.session['username'],'resultset':resultset})

@afterlogin_decorator
@login_decorator
def path(request):
      if request.method=='POST':
        count=0
        file_id=request.POST['file_id']
        update_object=update.objects.get(id=file_id)
        path_object=Path.objects.get(id=update_object.file_type)
        defined_path=path_object.dept_sequence
        l=list(defined_path)
        for i in l:
            department_object = Department.objects.get(id=i)
            if(update_object.department.lower()==department_object.dept_name.lower()):
               break
            count += 1
        if(update_object.status=='done'):
            count+=1
        print('count= '+str(count))
        for i in l:
            department_object = Department.objects.get(id=i)
            if(count>0):
              messages.success(request,department_object.dept_name,extra_tags='active')
              count-=1
            else:
                messages.success(request, department_object.dept_name, extra_tags='deactive')
        return redirect('/user/vfpath')

      else:
          resultsets = update.objects.filter(User_id_id=request.session['userid'])
          return render(request,'track.html',{ 'resultsets': resultsets})
