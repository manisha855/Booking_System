from django.urls import path
from . import views

urlpatterns = [
    #admin role
    path('examtypes/', views.examtype_list, name='examtype_list'),
    path('exam-type/', views.home_exam_type, name='home_exam_type'),
    path('find-city/', views.home_exam_city, name='home_city'),
    path('find-test/', views.home_find_test, name='home_find_test'),
    path('book-test/', views.home_book_test, name='home_book_test'),
    
    #User Role
    path('', views.root_redirect, name='root'), 
    path('home/', views.home, name='home'), 
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    #Booking for students
    path('booking_form/', views.booking_form, name='booking_form'),
    path('booking/', views.booking_list, name='booking_list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name="booking_edit"),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'), 
    path('booking_payment', views.booking_payment, name='booking_payment'),

    #profile creations
    path('profile_create/', views.profile_create, name='profile_create'),
    path('profile/', views.profile_list, name='profile_list'),
    path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),

    #Admin add the exam type
    path('exam-type/create/', views.create_exam_type, name='create_exam_type'),
    path('examtype/', views.exam_type_list, name='exam_type_list'),
    path('exam/detail/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exam/edit/<int:pk>/', views.examtype_edit, name='exam_edit'),
    path('exam/delete/<int:pk>/', views.exam_delete, name='exam_delete'),

    #admin role to schedules the exam 
    path('schedules/', views.test_schedules_list, name='test_schedules_list'),
    path('schedules/create/', views.test_schedules_create, name='test_schedules_create'),
    path('schedules/<int:pk>/', views.test_schedules_detail, name='test_schedules_detail'),
    path('schedules/<int:pk>/edit/', views.test_schedules_update, name='test_schedules_update'),
    path('schedules/<int:pk>/delete/', views.test_schedules_delete, name='test_schedules_delete'),

    #For tranction
    path('payment/', views.payment, name='payment'),

    # khalti url
    path('initiate/<int:booking_id>/', views.initkhalti, name='initiate'),
    path('payment/', views.payment, name='payment'),
    path('initkhalti/<int:booking_id>/', views.initkhalti, name='initkhalti'),
    path('verify/', views.verifykhalti, name='verifykhalti'),

]
