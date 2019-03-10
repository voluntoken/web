from django.contrib import admin
from .models import orgs, events, checks_stub, event_registration_stub
# Register your models here.

admin.site.register(orgs)
admin.site.register(events)
admin.site.register(checks_stub)
admin.site.register(event_registration_stub)