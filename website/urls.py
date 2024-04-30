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
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'), 
    # parntner Registraion
    path('student/<int:pk>', views.student_record, name='student'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),

    path('booking_form/', views.booking_form, name='booking_form'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name="booking_edit"),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'), 
    path('booking_payment', views.booking_payment, name='booking_payment'),

    path('profile_create/', views.profile_create, name='profile_create'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),

    path('blank/', views.blank, name='blank'),
    # path('patner/', views.partner_index, name='patner'),
]
