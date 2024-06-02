from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth import login as auth_login  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserLoginForm, BookForm, ProfileForm, ExamForm, TestSchedulesForm
from .models import CustomUser, Book, Profile, ExamType, TestSchedules
import requests
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Transaction

# Create your views here.
#IELTS test fees in Nepal
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

@login_required
def home_find_test(request):
    selected_city = request.GET.get('city', 'Nepal')  # Get the selected city from the query parameter
    return render(request, 'home/home_find_test.html', {'selected_city': selected_city})

@login_required
def home_book_test(request):
    test_LRW = TestSchedules.objects.filter(test_type='LRW').first()
    test_listen = TestSchedules.objects.filter(test_type='Listening').first()
    return render(request, 'home/home_book_test.html', {'test_LRW': test_LRW, 'test_listen': test_listen})

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
    exam_types = ExamType.objects.all()  # Retrieve all exam types

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
    return render(request, "login.html", {'form': form})

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
    
    return render(request, 'register.html', {'form': form})

#form crud
@login_required
def booking_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.creator = request.user  
            book.save()
            return redirect('profile_create')
    else:
        form = BookForm()
    return render(request, 'booking/booking_form.html', {'form': form})

@login_required
def booking_list(request):
    if request.user.is_authenticated:  # Check if user is authenticated
        if request.user.role == 'admin':  # Check if user is an admin
            bookings = Book.objects.all()  # Show all bookings for admin
        else:
            bookings = Book.objects.filter(creator=request.user)  # Show bookings created by the user
    else:
        bookings = []  # If user is not authenticated, return empty queryset
    
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Book, pk=pk)
    return render(request, 'booking/booking_details.html', {'booking': booking})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking/booking_detail', pk=booking.pk)
    else:
        form = BookForm(instance=booking)
    return render(request, 'booking/booking_edit.html', {'form': form})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')  # Redirect to the booking list page after deletion
    else:
        # Handle the case where the request method is not POST
        return redirect('booking/booking_list') 

@login_required    
def booking_payment(request):
    return render(request, 'booking/booking_payment.html')    

#Profile CRUD
@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.creator = request.user
            profile.save()
            return redirect('payment')  # Redirect to the blank view
        else:
            print("Form errors:", form.errors)  # This line helps in debugging
            messages.error(request, 'Failed to create profile. Please check the errors.')
    else:
        form = ProfileForm()
    return render(request, 'profile/profile_create.html', {'form': form})

@login_required
def profile_list(request):
    if request.user.is_authenticated:
        print("User Role:", request.user.role)  # Debugging statement
        if request.user.role == 'admin':
            profiles = Profile.objects.all()
        else:
            profiles = Profile.objects.filter(creator=request.user)
        print("Filtered Profiles:", profiles)  # Debugging statement
    else:
        profiles = []
    
    return render(request, 'profile/profile_list.html', {'profiles': profiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profile/profile_details.html', {'profile': profile})

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to profile detail page or any other page
            return redirect('profile_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile/profile_edit.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully.')
        return redirect('profile_list')
        
    return render(request, 'profile/profile_delete.html', {'profile': profile})

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

#Test schedule CRUD
@login_required
def test_schedules_create(request):
    if request.method == 'POST':
        form = TestSchedulesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_schedules_list')
    else:
        form = TestSchedulesForm()
    
    return render(request, 'test/test_form.html', {'form': form})

# Test schedule list view
@login_required
def test_schedules_list(request):
    test_schedules = TestSchedules.objects.all()
    return render(request, 'test/test_list.html', {'test_schedules': test_schedules})

# Test schedule detail view
@login_required
def test_schedules_detail(request, pk):
    test_schedule = get_object_or_404(TestSchedules, pk=pk)
    return render(request, 'test/test_details.html', {'object': test_schedule})

# Test schedule update view
@login_required
def test_schedules_update(request, pk):
    test_schedule = get_object_or_404(TestSchedules, pk=pk)
    if request.method == 'POST':
        form = TestSchedulesForm(request.POST, instance=test_schedule)
        if form.is_valid():
            form.save()
            return redirect('test_schedules_list')  # Correct redirection to the test_schedules_list URL name
    else:
        form = TestSchedulesForm(instance=test_schedule)
    return render(request, 'test/test_form.html', {'form': form, 'object': test_schedule})

@login_required
def test_schedules_delete(request, pk):
    test_schedule = get_object_or_404(TestSchedules, pk=pk)
    if request.method == 'POST':
        # Perform deletion logic here
        test_schedule.delete()
        return redirect('test/test_schedules_list')  # Redirect after deletion
    # If the request method is not POST, render a confirmation page
    return render(request, 'test/test_schedule_delete_confirmation.html', {'test_schedule': test_schedule})


#For Transaction
@login_required
def payment(request):
    booking = Book.objects.first()  
    if booking:
        return render(request, 'payment.html', {'booking': booking})
    else:
        return HttpResponse("No booking found")

@login_required
def initkhalti(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    exam_type = booking.exam_type
    amount = exam_type.newest_fee
    

    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = "http://127.0.0.1:8000/verify/"  
    purchase_order_id = request.POST.get('purchase_order_id')

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": booking.name,
            "email": booking.email,
            "phone": booking.phone
        }
    })

    print(return_url)
    print(booking.name)
    print(booking.email)
    print(booking.phone)
    print(purchase_order_id)
    print(amount)

    headers = {
        'Authorization': 'key b53d9c64376448d4b1e190ba4916e6b3',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])
   

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
        return render(request, 'verify.html', context)
    else:
        context['error'] = 'Transaction not completed'
        return render(request, 'verify.html', context)



