from django.contrib import admin
from .models import org, event, checks_stub, event_registration_stub, event_hours_spent_stub
# Register your models here.

admin.site.register(org)
admin.site.register(event)
admin.site.register(checks_stub)
admin.site.register(event_registration_stub)
admin.site.register(event_hours_spent_stub)