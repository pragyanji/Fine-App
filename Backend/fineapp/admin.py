from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Fine)
admin.site.register(NotificationLog)
admin.site.register(ViolationType)
admin.site.register(PoliceOfficer)
admin.site.register(FineStatistics)