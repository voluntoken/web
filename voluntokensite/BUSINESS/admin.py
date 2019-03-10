from django.contrib import admin
from .models import businesses, coupon, transaction_stub
# Register your models here.

admin.site.register(businesses)
admin.site.register(coupon)
admin.site.register(transaction_stub)