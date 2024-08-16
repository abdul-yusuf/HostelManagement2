from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'core/room_list.html', {'rooms': rooms})


def home_page(request):
    return render(request, 'core/index.html')


# Admin Dashboard
@login_required
def admin_dashboard(request):
    # print(request.user.role)
    if request.user.role == 'admin':
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

    elif request.user.role == 'student':
            # return redirect('login')
        announcements = Announcement.objects.all().order_by('-date_posted')[:5]
        payments = Payment.objects.filter(student=request.user.studentprofile)
        complaints = Complaint.objects.filter(student=request.user.studentprofile).order_by('-date_filed')[:5]
        context = {
            'announcements': announcements,
            'payments': payments,
            'complaints': complaints,
        }
        return render(request, 'student/dashboard.html', context)
    elif request.user.role == 'manager':
        recent_complaints = Complaint.objects.filter(status='pending').order_by('-date_filed')[:5]
        available_rooms = Room.objects.filter(occupied__lt=F('capacity'))
        context = {
            'recent_complaints': recent_complaints,
            'available_rooms': available_rooms,
        }
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


# Allocate Rooms
def allocate_rooms(request):
    if request.user.role != 'manager':
        return redirect('login')
    rooms = Room.objects.filter(occupied__lt=F('capacity'))
    students_without_rooms = User.objects.filter(role='student', studentprofile__room__isnull=True)
    context = {
        'rooms': rooms,
        'students_without_rooms': students_without_rooms,
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
    if request.method == 'POST':
        # Handle payment logic here
        pass
    return render(request, 'student/make_payment.html')


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
