from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth import login as auth_login  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm, UserLoginForm, BookForm,MobileEmailForm, ExamForm
from .models import CustomUser, Book, ExamType
import requests
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Transaction
import calendar
from datetime import date

# Create your views here.
#IELTS test fees in Nepal 
def generate_calendar(request):
    # Fetch all exam types
    exam_types = ExamType.objects.all()

    # Extract exam dates
    exam_dates = [exam_type.test_date for exam_type in exam_types]

    # Get the current year
    current_year = date.today().year

    # Prepare the calendars for display
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    calendar_first_half = []
    calendar_second_half = []

    # Generate the calendar for the first 6 months and second 6 months
    for month in range(1, 13):
        month_calendar = cal.formatmonth(current_year, month)
        if month <= 6:
            calendar_first_half.append(month_calendar)
        else:
            calendar_second_half.append(month_calendar)

    context = {
        'calendar_first_half': calendar_first_half,
        'calendar_second_half': calendar_second_half,
        'exam_dates': exam_dates,
    }

    return render(request, 'home/calendar.html', context)


@login_required
def examtype_list(request):
    examtypes = ExamType.objects.all()
    return render(request, 'home.html', {'examtypes': examtypes})

@login_required
def home_exam_type(request):
    # Your view logic here
    return render(request, 'home/home_exam_type.html')

@login_required
def home_exam_city(request):
    # Your view logic here
    city_names = ExamType.objects.values_list('city_name', flat=True).distinct()
    return render(request, 'home/home_city.html', {'city_names': city_names})

#Now used
@login_required
def home_find_test(request):
    exam_types = ExamType.objects.all() 

    context = {
        'exam_types': exam_types,
    }
    return render(request, 'home/home_find_test.html', context)

@login_required
def home_book_test(request):
    return render(request, 'home/home_book_test.html')

#Root Redirect
@login_required
def root_redirect(request):
    return redirect('register')

# Home 
@login_required
def home(request):
    paper_exam = ExamType.objects.filter(test_type='paper').first()
    computer_exam = ExamType.objects.filter(test_type='computer').first()
    visa_exam = ExamType.objects.filter(test_type='visa').first()
    lifeskill_exam = ExamType.objects.filter(test_type='lifeskill').first()
    exam_types = ExamType.objects.all()

    return render(request, 'home.html', {
        'paper_exam': paper_exam,
        'computer_exam': computer_exam,
        'visa_exam': visa_exam,
        'lifeskill_exam': lifeskill_exam,
        'exam_types': exam_types,
    })

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the dashboard after successful login
                return redirect('home')
            else:
                # User authentication failed
                messages.error(request, "Invalid username or password.")
        else:
            # Form validation failed
            messages.error(request, "Form validation failed. Please check the form data.")
    else:
        form = UserLoginForm()
    
    # If the request method is GET or form is invalid, render the login form
    return render(request, "webapp/login.html", {'form': form})

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'webapp/password_reset.html'
#     email_template_name = 'webapp/password_reset_email.html'  
#     success_url = reverse_lazy('password_reset_done')

def logout_user(request):
    logout(request)
    # messages.success(request, "You have been logged out.")
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
            else:
                user = form.save(commit=False)
                user.role = form.cleaned_data['role']
                user.save()
                login(request, user)  # Automatically log in the user after registration
                messages.success(request, "You have successfully registered!")
                return redirect('home')  # Redirect to the home page after registration
        else:
            messages.error(request, "Form validation failed. Please check the form data.")
    else:
        form = SignUpForm()
    
    return render(request, 'webapp/register.html', {'form': form})

#form crud
@login_required
def booking_form(request):
    # Fetch all exam types for the form
    exam_types = ExamType.objects.all()
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user  # Assign the creator
            book.save()
            # Debugging print to check if the redirect is being reached
            print(f"Redirecting to booking_detail with pk={book.pk}")
            # Redirect to the booking_detail page with the created booking's pk
            return redirect('booking_detail', pk=book.pk)
        else:
            # Debugging: Print form errors to understand why it's not valid
            print(form.errors)
    else:
        form = BookForm()
    
    return render(request, 'booking/booking_form.html', {'form': form, 'exam_types': exam_types})

@login_required
def booking_list(request):
    user_role = None
    categorized_bookings = {}

    if request.user.is_authenticated:
        user_role = request.user.role
        if user_role == 'admin':
            all_bookings = Book.objects.all()
        else:
            all_bookings = Book.objects.filter(created_by=request.user)

        creators = CustomUser.objects.filter(book__in=all_bookings).distinct()
        categorized_bookings = {creator: Book.objects.filter(created_by=creator) for creator in creators}

    return render(request, 'booking/booking_list.html', {
        'categorized_bookings': categorized_bookings,
        'user_role': user_role
    })

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Book, pk=pk)
    return render(request, 'booking/booking_details.html', {'booking': booking})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    
    # Check if the user is admin or partner
    if not request.user.is_superuser and request.user.role != 'partner':
        # Redirect to some error page or handle unauthorized access
        return redirect('booking_list')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_detail', pk=booking.pk)  
    else:
        form = BookForm(instance=booking)
    
    return render(request, 'booking/booking_edit.html', {'form': form, 'booking': booking})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    
    # Check if the user is admin or partner
    if not request.user.is_superuser and request.user.role != 'partner':
        # Redirect to some error page or handle unauthorized access
        return redirect('booking_list')

    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')  # Redirect to the booking list page after deletion
    else:
        # Handle the case where the request method is not POST
        return redirect('booking_list')  
    
#for students
@login_required
def edit_mobile_email(request, pk):
    booking = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = MobileEmailForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_detail', pk=pk)  # Redirect to booking detail page after saving
    else:
        form = MobileEmailForm(instance=booking)

    return render(request, 'booking/booking_details.html', {'form': form, 'booking': booking})

#Profile CRUD
# @login_required
# def profile_create(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.creator = request.user
#             profile.save()
#             messages.success(request, 'Profile created successfully.')
#             return redirect('payment')
#         else:
#             messages.error(request, 'Failed to create profile. Please check the errors.')
#     else:
#         form = ProfileForm()
#     return render(request, 'profile/profile_create.html', {'form': form})

# @login_required
# def profile_list(request):
#     if request.user.is_authenticated:
#         if request.user.role == 'admin':
#             profiles = Profile.objects.all()
#         else:
#             profiles = Profile.objects.filter(creator=request.user)
#     else:
#         profiles = []
    
#     return render(request, 'profile/profile_list.html', {'profiles': profiles})

# @login_required
# def profile_detail(request, pk):
#     profile = get_object_or_404(Profile, pk=pk)
#     return render(request, 'profile/profile_details.html', {'profile': profile})

# @login_required
# def profile_edit(request, pk):
#     profile = get_object_or_404(Profile, pk=pk)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('profile_list')
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, 'profile/profile_edit.html', {'form': form, 'profile': profile})

# @login_required
# def delete_profile(request, pk):
#     profile = get_object_or_404(Profile, pk=pk)
#     if request.method == 'POST':
#         profile.delete()
#         messages.success(request, 'Profile deleted successfully.')
#         return redirect('profile_list')
        
#     return render(request, 'profile/profile_delete.html', {'profile': profile})

#Add exam type by admin
@login_required
def create_exam_type(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_type_list')  # Redirect to a URL where you list all exam types
    else:
        form = ExamForm()
    return render(request, 'exam/exam_type.html', {'form': form})

@login_required
def exam_type_list(request):
    exam_types = ExamType.objects.all()
    return render(request, 'exam/exam_list.html', {'exam_types': exam_types})

@login_required
def exam_detail(request, pk):
    exam_type = get_object_or_404(ExamType, pk=pk)
    return render(request, 'exam/exam_details.html', {'exam_type': exam_type})

@login_required
def examtype_edit(request, pk):
    examtype = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=examtype)
        if form.is_valid():
            form.save()
            return redirect('examtype_list')
    else:
        form = ExamForm(instance=examtype)
    return render(request, 'exam/exam_type.html', {'form': form})

@login_required
def exam_delete(request, pk):
    exam_type = get_object_or_404(ExamType, pk=pk)
    exam_type.delete()
    return redirect('exam/examtype_list')

#For Transaction
@login_required
def payment(request):
    booking = Book.objects.first()  
    if booking:
        return render(request, 'transaction/payment.html', {'booking': booking})
    else:
        return HttpResponse("No booking found")
    
def history(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/history.html', {'transactions': transactions})
    

@login_required
def initkhalti(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    exam_type = booking.exam_type
    amount = exam_type.newest_fee
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = "http://127.0.0.1:8000/verify/"
    purchase_order_id = request.POST.get('purchase_order_id')

    # Convert PhoneNumber object to string
    phone_number = str(booking.mobileno)

    payload = {
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": booking.name,
            "email": booking.email,
            "phone": phone_number  # Use the string representation of PhoneNumber
        }
    }

    headers = {
        'Authorization': 'key b53d9c64376448d4b1e190ba4916e6b3',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        print(response_data)  # Optionally print the response for debugging

        # Redirect to the payment_url returned from Khalti
        return redirect(response_data['payment_url'])

    except requests.RequestException as e:
        # Handle any exceptions that occur during the request
        return JsonResponse({'error': str(e)}, status=500) 
      
@login_required
def verifykhalti(request):
    pidx = request.GET.get('pidx')
    status = request.GET.get('status')
    transaction_id = request.GET.get('transaction_id')
    tidx = request.GET.get('tidx')
    amount = request.GET.get('amount')
    total_amount = request.GET.get('total_amount')
    mobile = request.GET.get('mobile')
    purchase_order_id = request.GET.get('purchase_order_id')
    purchase_order_name = request.GET.get('purchase_order_name')

    if not pidx:
        return JsonResponse({'error': 'pidx parameter is missing'}, status=400)

    # Convert amount and total_amount to decimal
    try:
        amount = float(amount)
        total_amount = float(total_amount)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid amount format'}, status=400)

    # Save the transaction data to the database
    transaction = Transaction(
        pidx=pidx,
        status=status,
        transaction_id=transaction_id,
        tidx=tidx,
        amount=amount,
        total_amount=total_amount,
        mobile=mobile,
        purchase_order_id=purchase_order_id,
        purchase_order_name=purchase_order_name,
    )
    transaction.save()

    context = {
        'transaction': {
            'pidx': pidx,
            'status': status,
            'transaction_id': transaction_id,
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': purchase_order_name,
        }
    }

    if status == 'Completed':
        return render(request, 'transaction/verify.html', context)
    else:
        context['error'] = 'Transaction not completed'
        return render(request, 'transaction/verify.html', context)



