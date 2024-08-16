from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    # path('payment/', views.payment, name='payment'),
    # path('complaint/', views.complaint, name='complaint'),
    # Add more URLs as needed

    path('', views.home_page, name='home'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),

    # Admin URLs
    # path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('view-reports/', views.view_reports, name='view_reports'),

    # Hostel Manager URLs
    # path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/manage-complaints/', views.manage_complaints, name='manage_complaints'),
    path('manager/complaints/<int:id>/', views.view_detail_complaint, name='view_complaint'),
    path('manager/complaints/resolve/<int:id>/', views.resolve_complaint, name='resolve_complaint'),
    path('manager/allocate-rooms/', views.allocate_rooms, name='allocate_rooms'),
    path('manager/view-payments/', views.view_payments, name='view_payments'),

    # Student URLs
    # path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/make-payment/', views.make_payment, name='make_payment'),
    path('student/file-complaint/', views.file_complaint, name='file_complaint'),
    path('student/view-announcements/', views.view_announcements, name='view_announcements'),
    path('student/bed-space/', views.book_space_view, name='space_view'),
]