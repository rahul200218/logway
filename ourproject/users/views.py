from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import User,emailverification,Courier,CourierImage,Complaint,ContactUs
from django.contrib import messages
import string
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def getstarted(request):
    return render(request,"getstarted.html")


    

#verifying email
def verify_email(request):
    if request.method=="POST":
        email=request.POST.get('emailid')
       
       
        def generate_random_string(length=8):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string
        token=generate_random_string()
        confirm=emailverification.objects.filter(email=email)
        print(token,confirm)
        if not confirm:
            emailverification.objects.create(email=email,token=token)
            reset_url = f"{request.scheme}://{request.get_host()}/register1/{email}/{token}/"
            send_mail(
                    'Email verification',
                    f'Please click the following link to verify your email: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            messages.success(request, 'An email has been sent with instructions to verify your email.')
        elif confirm:
            veri=User.objects.filter(email=email)
            if veri:
                messages.error(request, 'This account is already registered.')
                return render(request,"verify_email.html")
            else:
                obj2=emailverification.objects.get(email=email)
                obj2.token=token
                obj2.save()
                
                print("yes",token,email)
                reset_url = f"{request.scheme}://{request.get_host()}/register1/{email}/{token}/"
                send_mail(
                    'Email verification',
                    f'Please click the following link to verify your email: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'An email has been sent with instructions to verify your email.')
            return render(request,"verify_email.html")
    return render(request,"verify_email.html")



#user registration
def confirmedemail(request,email,token):
    confirm=emailverification.objects.get(email=email,token=token)
    if confirm:
         if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")
            location=request.POST.get("location")

            if pass1 == pass2:
                print(name,email,pass1,pass2,location)
                user = User.objects.create_user(username=name, email=email, password=pass1,location=location)
                user.is_user = True
                user.save() 
                return redirect("login")
            else:
                messages.error(request,"incorrect")
         return render(request, "register.html",{'email':email})

#login
@csrf_protect
def login1(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("pass")
        user = authenticate(request, username=name, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f"successfully logged in as { request.user.username }")
            return redirect("home")
            
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")



#Home pages
@login_required
def home(request):
    if request.user.is_user:
        if request.method=="POST":
            name=request.POST.get('namebox')
            email=request.POST.get('emailbox')
            ph=request.POST.get('phone')
            des=request.POST.get('areabox')
            ob=ContactUs.objects.create(name=name,email=email,phone_number=ph,description=des)
            ob.save()
            messages.success(request,"Contact details sent")
        return render(request,"userhome.html")
    elif request.user.is_staff and not request.user.is_admin:
        if request.method=="POST":
            name=request.POST.get('namebox')
            email=request.POST.get('emailbox')
            ph=request.POST.get('phone')
            des=request.POST.get('areabox')
            ob=ContactUs.objects.create(name=name,email=email,phone_number=ph,description=des)
            ob.save()
            messages.success(request,"Contact details sent")
        return render(request,"staffhome.html")
    elif request.user.is_admin and request.user.is_staff:
        if request.method=="POST":
            name=request.POST.get('namebox')
            email=request.POST.get('emailbox')
            ph=request.POST.get('phone')
            des=request.POST.get('areabox')
            print(name,email,ph,des)
            ob=ContactUs.objects.create(name=name,email=email,phone_number=ph,description=des)
            ob.save()
            messages.success(request,"Contact details sent")
        return render(request, "adminhome.html")
    else:
        return redirect("login")
    
@login_required
def register_s(request):
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")
            location = request.POST.get("location")
            
            if pass1 == pass2:
                try:
                    user = User.objects.create_user(username=name, email=email, password=pass1, location=location)
                    user.is_staff = True
                    user.save()
                    messages.success(request, 'Registration successful!')
                except Exception as e:
                    messages.error(request, 'Registration failed: username already taken ')
            else:
                messages.error(request, 'Passwords do not match!')
                
        return render(request, "register_staff.html")

    


def profile1(request):
    if request.method=="POST":
        pf=request.FILES.get("new-profile")
        about=request.POST.get("abo")
        user=User.objects.get(id=request.user.id)
        user.profile=pf
        user.about=about
        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect("home")
    return render(request,"profile.html")



def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('reset_password')

        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        print(uid,token)
        reset_url = f"{request.scheme}://{request.get_host()}/reset_password_confirm/{uid}/{token}/"
        send_mail(
            'Password reset',
            f'Please click the following link to reset your password: {reset_url} By Team LOGWAY',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'An email has been sent with instructions to reset your password.')
        return redirect('reset_password')

    return render(request, 'reset_password.html')


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid token.')
        return redirect('login')
        
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')

            if password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect('login')

            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'new_password.html')

    else:
        messages.error(request, 'Invalid token.')
        return redirect('login')
    

#Send Courier
@login_required
def send_courier(request):
    if request.user.is_user:
        if request.method == 'POST':
            location = request.POST.get('place')
            phone_number = request.POST.get('cno')
            destination = request.POST.get('dplace')
            lattitude=request.POST.get('lattitude')
            longitude=request.POST.get('longitude')
            addess=request.POST.get('add')
            courier = Courier.objects.create(sender=request.user, location=location, phone_number=phone_number,destination=destination,lattitude=lattitude,longitude=longitude,destination_address=addess)
            print(location)
            courier.save()
            messages.success(request, 'Courier sent successfully')
            return redirect('send_courier')
        return render(request, 'send_courier.html')
    
def courier_sent(request):
    if request.user.is_user:
        couriers = Courier.objects.all()
        return render(request, 'view_courier_sent.html', {'couriers': couriers})
    
from django.utils import timezone

def view_couriers(request):
    if request.user.is_staff:
        if request.method == 'POST':
            courier_id = request.POST.get('courier_id')
            courier = Courier.objects.get(id=courier_id)
            location = courier.location
            courier.accepted_by = request.user
            t = timezone.localtime()
            print(t)
            courier.accepted_at = t
            courier.save()
            messages.success(request, 'Courier accepted successfully')
            return redirect('view_couriers')
        else:
            couriers = Courier.objects.filter(accepted_by__isnull=True)
            return render(request, 'view_courier.html', {'couriers': couriers})
    


def view_accepted_courier(request):
    if request.user.is_staff:
        if request.method == 'POST':
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print(latitude, longitude)
            

        couriers = Courier.objects.filter(accepted_by=request.user)
        nodata = "No couriers accepted"
        user = request.user

        if couriers:
            return render(request, 'view_courier_received.html', {'couriers': couriers, 'user': user})
        else:
            messages.error(request,"No couriers accepted")
            return render(request, 'view_courier_received.html', {'couriers': nodata})


def upload_courier_image(request, courier_id):
    courier = Courier.objects.get(id=courier_id)
    if request.user.is_staff:
        if request.method == 'POST':
           
            if CourierImage.objects.filter(courier=courier).exists():
                messages.error(request, 'Courier image has already been uploaded')
                return redirect('accepted_courier')

            image = request.FILES.get('image')
            price = request.POST.get('price')
            id1 = Courier.objects.get(id=courier_id)
            sent_by = id1.sender
            courier_image = CourierImage.objects.create(courier=courier, uploaded_by=request.user, image=image, price=price, sent_by_user=sent_by)
            courier_image.save()
            messages.success(request, 'Courier image uploaded successfully')
            return redirect('accepted_courier')
        else:
            return render(request, 'upload_courier_img.html', {'courier': courier})
    else:
        messages.error(request, 'You do not have permission to upload courier image')
        return redirect('accepted_courier')


from django.core.exceptions import ObjectDoesNotExist
def view_images_uploaded(request,courier_id):
        if request.user.is_user:
                try:
                    images = CourierImage.objects.get(courier_id=courier_id)
                    
                    if images is not None:
                    
                        return render(request, 'view_images_uploaded.html', {'courier': images})
                    else:
                        nodata="No Images uploaded by staff"
                        return render(request, 'view_images_uploaded.html', {'nodata':nodata })
                except ObjectDoesNotExist:
                        nodata="No Images uploaded by staff"
                        messages.error(request,"No images added by staff")
                        return render(request, 'view_images_uploaded.html', {'nodata':nodata })
    

                


def view_images_uploaded_s(request,id):
    if request.user.is_staff:
        try:
            images = CourierImage.objects.get(uploaded_by=request.user,courier=id)
            nodata="No Images uploaded by staff"
            if images is not None:
                    return render(request, 'view_images_uploaded_s.html', {'courier': images})
            else:
                    messages.error(request,"No images uploaded by you")
                    return render(request, 'view_images_uploaded_s.html', {'images':nodata })
        except ObjectDoesNotExist:
            messages.error(request,"No images uploaded by you")
            nodata="nothing here"
            return redirect("accepted_courier")



def view_all_courier(request):
        if request.user.is_admin:
                couriers = Courier.objects.all()
                nodata="No couriers present"
                if request.method=="POST":
                    id=request.POST.get("search")
                    ob=Courier.objects.filter(courier_id=id)
                    if ob:
                        return render(request, 'view_all_courier_admin.html', {'couriers': ob})
                    else:
                        messages.error(request,"No such courier")
                        return render(request, 'view_all_courier_admin.html', {'couriers': couriers})
                if couriers is not None:
                    return render(request, 'view_all_courier_admin.html', {'couriers': couriers})
                else:
                    return render(request, 'view_all_courier_admin.html', {'couriers':nodata })


def view_courier_details(request,courier_id):
    # courier = CourierImage.objects.get(courier_id=courier_id)
    if request.user.is_admin:
    #     return render(request, 'view_courier_details.html', {'courier': courier})
    # else:
    #     messages.error(request, 'You do not have permission to upload courier image')
    #     return redirect('view_all_couriers')
        try:
            images = CourierImage.objects.get(courier=courier_id)
            nodata="No Images uploaded by staff"
            if images is not None:
                    return render(request, 'view_courier_details.html', {'courier': images})
            else:
                    messages.error(request,"No images uploaded by staff")
                    return render(request, 'view_images_uploaded_s.html', {'images':nodata })
        except ObjectDoesNotExist:
            messages.error(request,"No images uploaded by staff")
            nodata="nothing here"
            return render(request, 'view_images_uploaded_s.html', {'images':nodata })


def update_courier(request, courier_id):
    courier_id = int(courier_id)
    couriers = Courier.objects.get(id=courier_id)
    accepted_by = couriers.accepted_by
    ch1 = couriers.checkpoint_1
    ch2 = couriers.checkpoint_2
    ch3 = couriers.checkpoint_3
    destination_staff = couriers.destination_received_by
    print(accepted_by, destination_staff)
    if request.method == "POST":
            # accept = request.POST.get('accepted')
            check_point_1 = request.POST.get('ch1')
            check_point_2 = request.POST.get('ch2')
            check_point_3 = request.POST.get('ch3')
            # desti = request.POST.get('destination')
            if check_point_1 is None:
                check_point_1 = ch1
            if check_point_2 is None:
                check_point_2 = ch2
            if check_point_3 is None:
                check_point_3 = ch3
            couriers.checkpoint_1 = check_point_1
            couriers.checkpoint_2 = check_point_2
            couriers.checkpoint_3 = check_point_3
            couriers.save()
            return redirect(request.path_info)
    return render(request, 'update_courier.html', {'couriers': couriers, 'check_point_1': ch1, 'check_point_2': ch2, 'check_point_3': ch3,'accepted_by':accepted_by,'destination_staff':destination_staff})
    

import razorpay
from users.apps import UsersConfig
from ourproject.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRETKEY


client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRETKEY))
client.set_app_details({"title": "users", "version": UsersConfig.version})
def payment(request,price,id1):
   
   
    DATA = {
    "amount": price*100,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    },
    'payment_capture':'1',

    }
   
    payment1=client.order.create(data=DATA)
    order_id = payment1['id']
    ob = Courier.objects.get(id=id1)
    ph=ob.phone_number
    
    context = {
    'amount': price*100,
    'api_key': RAZORPAY_API_KEY,
    'order_id': order_id,
    'id1':id1,
    'ph': ph,
    }

    
    return render(request,"payment.html",context)



@csrf_exempt
def thankyou(request,courier_id):
    payment1=Courier.objects.get(id=courier_id)
    if payment1:
        payment1.payment=True
        payment1.save()
        messages.success(request,"payment successfull")
        return redirect("home")
    return render(request,'thankyou.html')


def Accept_courier_For_destination(request):
    if request.user.is_staff:
        if request.method == 'POST':
            courier_id = request.POST.get('courier_id')
            courier = Courier.objects.get(id=courier_id)
            courier.destination_received_by= request.user
            courier.destination_received_at = timezone.localtime()
            courier.save()
            messages.success(request, 'Courier accepted successfully')
            return redirect('for_delivery')
        else:
            couriers = Courier.objects.filter(destination_received_by__isnull=True,checkpoint_3=True)
            return render(request, 'accept_courier_for_delivery.html', {'couriers': couriers})
            
    else:
        couriers = request.user.accepted_couriers.all()
        return render(request, 'accept_courier_for_delivery.html', {'couriers': couriers})
    


def Accepted_courier_For_destination(request):
     if request.user.is_staff:
                couriers = Courier.objects.filter( destination_received_by=request.user,status=False)
                nodata="No couriers accepted"
                if couriers is not None:
                    return render(request, 'view_accepted_courier_for_delivery.html', {'couriers': couriers,'request':request})
                else:
                    messages.error(request,"No couriers accepted for destination")
                    return redirect("for_delivery")
                


def mark_destination_status(request,courier_id):
    print(courier_id)
    if request.method=="POST":
        status=request.POST.get('status')
        print(status)
        courier=Courier.objects.get(id=courier_id)
        if status=="reached":
            courier.status=True
            courier.save()
            messages.success(request,"Marked as reached successfully")
            return redirect('home')
    return render(request,"mark_reached.html")




def all_users(request):
    if request.user.is_admin:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            print(user_id)
            ob=User.objects.get(id=user_id)
            ob2=emailverification.objects.filter(email=ob.email)
            if ob2:
                ob2.delete()
            ob.delete()
            messages.success(request, 'Deleted Successfully')
            return redirect('all_users')
        else:
            couriers = User.objects.filter(is_admin=False)
            return render(request, 'view_all_users2.html', {'couriers': couriers})
    


def logout1(request):
     logout(request)
     return redirect("login")


def chatbot(request):
    return render(request,"chatbot.html")


def reg_complaint(request):
    if request.user.is_user:
        if request.method=="POST":
            id=request.POST.get("id")
            issue=request.POST.get("issue")
            problem=request.POST.get("problem")
            ob=Complaint.objects.filter(error_courier_id=id)
            if ob:
                messages.error(request,"already complained")
                return render(request,"register_complaint.html")
            else:
                ob2=Courier.objects.filter(courier_id=id,sender=request.user)
                if not ob2:
                     messages.error(request,"no such courier")
                     return render(request,"register_complaint.html")
                else:
                    ob3=Complaint.objects.create(complaint_by=request.user,error_courier_id=id, description=problem,issue=issue)
                    ob3.save()
                    messages.success(request,"complaint sent successfully")
                    return render(request,"register_complaint.html")
        return render(request,"register_complaint.html")


def view_complaints(request):
    ob=Complaint.objects.all()
    if ob:
        return render(request,"view_complaints.html",{'complaint':ob})
    else:
        messages.error(request,"No complaints")
        return redirect("home")