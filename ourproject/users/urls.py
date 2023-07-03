from django.contrib import admin
from django.urls import path, register_converter
from users import views
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from .converter import DecimalConverter


register_converter(DecimalConverter, 'float')
urlpatterns = [
  
    path("",views.getstarted,name='getstarted'),
    path("login/",views.login1,name="login"),
    path("verify_email",views.verify_email,name="verify_email"),
    re_path(r'^register1/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<token>\w+)/$', views.confirmedemail, name='confirmedemail'),
    
    path("home/",views.home,name="home"),
    path("register_staff/",views.register_s,name="register_staff"),
    path('profile',views.profile1,name="profile"),
    
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),

    path('send_courier/', views.send_courier, name='send_courier'),
    path("view_courier_sent", views.courier_sent, name="sent_courier"),

    path('view_couriers/', views.view_couriers, name='view_couriers'),
    path("view_courier_recieved",views.view_accepted_courier,name="accepted_courier"),

    path('upload_courier_image/<str:courier_id>/', views.upload_courier_image, name='upload_courier_image'),



    path('view_images_uploaded/<int:courier_id>',views.view_images_uploaded,  name='view_upload_img'),
    path('view_images_uploaded_s/<int:id>',views.view_images_uploaded_s,name='view_upload_img_s'),

    path('view_all_couriers',views.view_all_courier,name='all_courier'),
    path('view_courier_details/<str:courier_id>',views.view_courier_details,name='view_courier_details'),
    path('update_courier/<str:courier_id>',views.update_courier,name='update_courier'),


    path('payment/<float:price>/<int:id1>/',views.payment,name="payment"),
    path('thankyou/<int:courier_id>',views.thankyou,name="thankyou"),

    path('accept_for_delivery',views.Accept_courier_For_destination,name='for_delivery'),
    path('accepted_for_delivery',views.Accepted_courier_For_destination,name='accepted_for_delivery'),
    path('mark_reached/<int:courier_id>',views.mark_destination_status,name='Mark_destination'),

    path('view_all_users',views.all_users,name="all_users"),
    path('logout',views.logout1,name='logout'),
    path('chatbot',views.chatbot,name='chatbot'),
    path('register_complaint',views.reg_complaint,name="send_complaint"),
    path('view_complaints',views.view_complaints,name="view_complaint"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

