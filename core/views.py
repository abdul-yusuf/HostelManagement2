from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render, redirect, reverse
from .models import *

from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'core/room_list.html', {'rooms': rooms})


def home_page(request):
    return render(request, 'core/index.html')


# Admin Dashboard
@login_required
def admin_dashboard(request):
    user = request.user
    if user.role == 'admin':
        # return redirect('login')  # Redirect non-admin users
        total_rooms = Room.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_payments = Payment.objects.aggregate(Sum('amount'))
        context = {
            'total_rooms': total_rooms,
            'total_students': total_students,
            'total_payments': total_payments,
        }
        return render(request, 'admin/dashboard.html', context)

    elif user.role == 'student':
        # return redirect('login')
        if user.studentprofile.room:
            if user.studentprofile.payment.get_queryset().all():
                if user.studentprofile.payment.get_queryset().filter(is_payed=False):
                    return redirect(reverse('make_payment'))
            else:
                return redirect(reverse('make_payment'))
            announcements = Announcement.objects.all().order_by('-date_posted')[:5]
            payments = Payment.objects.filter(student=request.user.studentprofile)
            complaints = Complaint.objects.filter(student=request.user.studentprofile).order_by('-date_filed')[:5]
            context = {
                'announcements': announcements,
                'payments': payments,
                'complaints': complaints,
            }
            return render(request, 'student/dashboard.html', context)
        else:
            return redirect(reverse('space_view'))

    elif user.role == 'manager':
        recent_complaints = Complaint.objects.filter(status='pending').order_by('-date_filed')[:5]
        available_rooms = Room.objects.filter(occupied__lt=F('capacity'))
        context = {
            'recent_complaints': recent_complaints,
            'available_rooms': available_rooms,
        }
        return render(request, 'manager/dashboard.html', context)
    # print(context)
    return render(request, 'core/index.html')


# Manage Users
def manage_users(request):
    if request.user.role != 'admin':
        return redirect('login')
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})


# Manage Rooms
def manage_rooms(request):
    if request.user.role != 'admin':
        return redirect('login')
    rooms = Room.objects.all()
    return render(request, 'admin/manage_rooms.html', {'rooms': rooms})


# View Reports
def view_reports(request):
    if request.user.role != 'admin':
        return redirect('login')
    # Logic for generating reports
    # Get the current date and time
    now = timezone.now()

    # Calculate the date 7 days from now
    seven_days_from_now = now + timedelta(days=7)
    recent_complaints = Announcement.objects.filter(date_posted__gte=seven_days_from_now)[:5]
    context = {
        'reports': recent_complaints,
    }
    return render(request, 'admin/view_reports.html')


# Hostel Manager Dashboard
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('login')
    recent_complaints = Complaint.objects.filter(status='pending').order_by('-date_filed')[:5]
    available_rooms = Room.objects.filter(occupied__lt=F('capacity'))
    context = {
        'recent_complaints': recent_complaints,
        'available_rooms': available_rooms,
    }
    return render(request, 'manager/dashboard.html', context)


# Manage Complaints
def manage_complaints(request):
    if request.user.role != 'manager':
        return redirect('login')
    complaints = Complaint.objects.all().order_by('-date_filed')
    return render(request, 'manager/manage_complaints.html', {'complaints': complaints})


def view_detail_complaint(request, id):
    if request.user.role != 'manager':
        return redirect('login')
    complaints = Complaint.objects.get(id=id)
    return render(request, 'manager/view_complaints.html', {'complaint': complaints})


def resolve_complaint(request, id):
    if request.user.role != 'manager':
        return redirect('login')
    complaints = Complaint.objects.get(id=id)
    if complaints.status == 'pending':
        complaints.status = 'resolved'
        complaints.save()
        messages.success(request, f'Successfully Resolved Complaint with ID:{id}')
    else:
        messages.success(request, f'Complaint with ID:{id} was already reloved')
    return redirect(reverse('manage_complaints'))


# Allocate Rooms
def allocate_rooms(request):
    if request.user.role != 'manager':
        return redirect('login')
    rooms = Room.objects.filter(occupied__lt=F('capacity'))
    students_without_rooms = StudentProfile.objects.filter(room=None)
    if request.method == 'POST':
        try:
            student = StudentProfile.objects.get(id=request.POST.get('student'))
            room = Room.objects.get(id=request.POST.get('room'))
            student.room = room
            student.save()
            return redirect(reverse('dashboard'))
        except Exception as e:
            print(e)
            pass
    context = {
        'rooms': rooms,
        'students': students_without_rooms,
    }
    return render(request, 'manager/allocate_rooms.html', context)


# View Payments
def view_payments(request):
    if request.user.role != 'manager':
        return redirect('login')
    payments = Payment.objects.all().order_by('-date_paid')
    return render(request, 'manager/view_payments.html', {'payments': payments})


# Student Dashboard
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    announcements = Announcement.objects.all().order_by('-date_posted')[:5]
    payments = Payment.objects.filter(student=request.user.studentprofile)
    complaints = Complaint.objects.filter(student=request.user.studentprofile).order_by('-date_filed')[:5]
    context = {
        'announcements': announcements,
        'payments': payments,
        'complaints': complaints,
    }
    return render(request, 'student/dashboard.html', context)


# Make Payment
def make_payment(request):
    if request.user.role != 'student':
        return redirect('login')
    payments = Payment.objects.filter(student=request.user.studentprofile, is_payed=False)

    try:
        context = {
            'payment': payments[0]
        }
    except Exception as e:
        print(e)
        context = {
            'payment': payments
        }

    if request.method == 'POST':
        # Handle payment logic here
        print(payments, payments[0].is_payed)
        payment = Payment.objects.get(id=payments[0].id)
        payment.is_payed = True
        payment.save()
        return redirect(reverse('dashboard'))
        # print(payments,payments[0].is_payed, dir(payments[0]))

    return render(request, 'student/make_payment.html', context=context)


# File Complaint
def file_complaint(request):
    if request.user.role != 'student':
        return redirect('login')
    if request.method == 'POST':
        complaint_text = request.POST.get('complaint_text')
        Complaint.objects.create(student=request.user.studentprofile, complaint_text=complaint_text)
        return redirect('dashboard')
    return render(request, 'student/file_complaint.html')


# View Announcements
def view_announcements(request):
    if request.user.role != 'student':
        return redirect('login')
    announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'student/view_announcements.html', {'announcements': announcements})


def book_space_view(request):
    if request.user.role != 'student':
        return redirect('login')
    space = Room.objects.not_occupied_rooms()
    return render(request, 'student/book_room.html', {'rooms': space})


def add_announcement(request):
    return render(request, 'student/book_room.html', {'rooms': space})
