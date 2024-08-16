from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models import F, ExpressionWrapper, BooleanField, When, Case, Value


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Hostel Manager'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # Add this to avoid conflict
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Unique related_name to avoid conflict
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )
    # Add this to avoid conflict
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Unique related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user',
    )


class RoomManager(models.Manager):
    def occupied_rooms(self):
        return self.annotate(
            is_occupied=ExpressionWrapper(
                F('capacity') - F('occupied') == 0,
                output_field=BooleanField()
            )
        ).filter(is_occupied=True)

    def not_occupied_rooms(self):
        return self.annotate(
            is_not_occupied=Case(
                When(capacity__gt=F('occupied'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).filter(is_not_occupied=True)

class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('dormitory', 'Dormitory'),
    )
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField(default=1)
    occupied = models.IntegerField(default=0)
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    objects = RoomManager()

    @property
    def status(self):
        # try:
        if self.capacity-self.occupied == 0:
            return 'occupied'
        # except Exception as e:
        #     print(e)
        #     return 'not occupied'
        return 'not occupied'

    @property
    def space(self):
        return self.capacity-self.occupied

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)


class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_payed = models.BooleanField(default=False)
    date_paid = models.DateField(auto_now_add=True)
    receipt_number = models.CharField(max_length=20)


class Complaint(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('resolved', 'Resolved')), default='pending')
    date_filed = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
