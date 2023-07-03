from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(emailverification)
admin.site.register(Courier)
admin.site.register(CourierImage)
admin.site.register(Complaint)
admin.site.register(ContactUs)