from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import examtype_views, examdate_views , form_views,home_views


urlpatterns = [
    #admin role
    path('examtypes/', home_views.examtype_list, name='examtype_list'),
    path('exam-type/', home_views.home_exam_type, name='home_exam_type'),
    path('find-city/', home_views.home_exam_city, name='home_city'),
    path('book-test/', home_views.home_book_test, name='home_book_test'),
    path('generate-calendar/', home_views.generate_calendar, name='generate_calendar'),
    path('find-test/', home_views.home_find_test, name='home_find_test'),
    # path('users/', views.user_list, name='user_list'),
    
    #User Role
    path('', home_views.index, name='index'),
    path('home', home_views.home, name='home'),
    path('login/', home_views.login_user, name='login'),
    path('logout/', home_views.logout_user, name='logout'),
    path('register/', home_views.register_user, name='register'),
    path('contact/', home_views.contact_view, name='contact'),
    
    path('register-student/', home_views.sub_register_student, name='sub_register_student'), 
    path('students/', home_views.sub_register_student_list, name='sub_register_student_list'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Adim part examtypes
    path('exam_list/', examtype_views.exam_list, name='exam_list'),
    path('examtypes/<int:pk>/', examtype_views.examtype_detail, name='examtype_detail'),
    path('examtypes/create/', examtype_views.examtype_create, name='examtype_create'),
    path('examtypes/update/<int:pk>/', examtype_views.examtype_update, name='examtype_update'),
    path('examtypes/delete/<int:pk>/', examtype_views.examtype_delete, name='examtype_delete'), 

    # Adim part URLs for ExamDate
    path('examdates/', examdate_views.examdate_list, name='examdate_list'),
    path('examdates/<int:pk>/', examdate_views.examdate_detail, name='examdate_detail'),
    path('examdates/create/', examdate_views.examdate_create, name='examdate_create'),
    path('examdates/update/<int:pk>/', examdate_views.examdate_update, name='examdate_update'),
    path('examdates/delete/<int:pk>/', examdate_views.examdate_delete, name='examdate_delete'), 

    #Booked Exam Type & date by student
    # path('booking-exam/', bookedexam_views.booked_list, name='booked_list'),
    # path('booking-exam-create/', bookedexam_views.booked_type, name='booked_type'),
    # path('booking-exam/<int:pk>/', bookedexam_views.booked_detail, name='booked_detail'),
    # path('booking-exam/<int:pk>/edit/', bookedexam_views.booked_edit, name='booked_edit'),
    # path('booking-exam/<int:pk>/delete/', bookedexam_views.booked_delete, name='booked_delete'),

    #Booking for students
    path('booking-form-create/', form_views.booking_form, name='booking_form'),
    path('booking-form/', form_views.booking_list, name='booking_list'),
    path('booking-form/<int:pk>/', form_views.booking_detail, name='booking_detail'),
    path('booking-form/<int:booking_id>/edit/', form_views.edit_booking, name='booking_edit'),
    path('booking-form/<int:booking_id>/delete/', form_views.delete_booking, name='delete_booking'),

    path('edit_mobile_email/<int:pk>/', form_views.edit_mobile_email, name='edit_mobile_email'),

    #profile creations
    # path('profile_create/', views.profile_create, name='profile_create'),
    # path('profile/', views.profile_list, name='profile_list'),
    # path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    # path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    # path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),

    # path('exam-type/create/', views.create_exam_type, name='create_exam_type'),
    # path('examtype/', views.exam_type_list, name='exam_type_list'),
    # path('exam/detail/<int:pk>/', views.exam_detail, name='exam_detail'),
    # path('exam/edit/<int:pk>/', views.examtype_edit, name='exam_edit'),
    # path('exam/delete/<int:pk>/', views.exam_delete, name='exam_delete'),

    #For tranction
    path('payment/', home_views.payment, name='payment'),
    # path('history/', other_views.history, name='history'),

    # khalti url
    # path('initiate/<int:booking_id>/', other_views.initkhalti, name='initiate'),
    # path('payment/', other_views.payment, name='payment'),
    # path('initkhalti/<int:booking_id>/', other_views.initkhalti, name='initkhalti'),
    # path('verify/', other_views.verifykhalti, name='verifykhalti'),

#Transaction Of connectips
    path('connectips-payment/', home_views.payment_form, name='payment_form'),
    path('initiate-payment/', home_views.initiate_payment, name='initiate_payment'),
    path('transactionResponse/success/', home_views.validate_transaction, name='validate_transaction'),
    path('transactionResponse/failure/', home_views.validate_transaction, name='validate_transaction'),
]
