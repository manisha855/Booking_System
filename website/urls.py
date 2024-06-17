from django.urls import path
# from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from . import views

urlpatterns = [
    #admin role
    path('examtypes/', views.examtype_list, name='examtype_list'),
    path('exam-type/', views.home_exam_type, name='home_exam_type'),
    path('find-city/', views.home_exam_city, name='home_city'),
    path('book-test/', views.home_book_test, name='home_book_test'),
    path('generate-calendar/', views.generate_calendar, name='generate_calendar'),

    path('find-test/', views.home_find_test, name='home_find_test'),
    
    #User Role
    path('', views.root_redirect, name='root'), 
    path('home/', views.home, name='home'), 
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),  

    # path('reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('reset-password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset-password/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    #Booking for students
    path('booking_form/', views.booking_form, name='booking_form'),
    path('booking/', views.booking_list, name='booking_list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name='booking_edit'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),

    path('edit_mobile_email/<int:pk>/', views.edit_mobile_email, name='edit_mobile_email'),

    #profile creations
    # path('profile_create/', views.profile_create, name='profile_create'),
    # path('profile/', views.profile_list, name='profile_list'),
    # path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    # path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    # path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),

    #Admin add the exam type
    path('exam-type/create/', views.create_exam_type, name='create_exam_type'),
    path('examtype/', views.exam_type_list, name='exam_type_list'),
    path('exam/detail/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exam/edit/<int:pk>/', views.examtype_edit, name='exam_edit'),
    path('exam/delete/<int:pk>/', views.exam_delete, name='exam_delete'),

    #For tranction
    path('payment/', views.payment, name='payment'),
    path('history/', views.history, name='history'),

    # khalti url
    path('initiate/<int:booking_id>/', views.initkhalti, name='initiate'),
    path('payment/', views.payment, name='payment'),
    path('initkhalti/<int:booking_id>/', views.initkhalti, name='initkhalti'),
    path('verify/', views.verifykhalti, name='verifykhalti'),

]
