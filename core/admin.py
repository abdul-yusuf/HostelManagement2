from django.contrib import admin
from .models import User, Room, StudentProfile, Payment, Complaint, Announcement

admin.site.register(User)
admin.site.register(Room)
admin.site.register(StudentProfile)
admin.site.register(Payment)
admin.site.register(Complaint)
admin.site.register(Announcement)