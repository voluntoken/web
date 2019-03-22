from django.contrib import admin
from .models import business, coupon, transaction_stub, total_support_stub
# Register your models here.

admin.site.register(business)
admin.site.register(coupon)
admin.site.register(transaction_stub)
admin.site.register(total_support_stub)