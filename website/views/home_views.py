from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth import login as auth_login  
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from ..forms import SignUpForm, SignUpSubForm, UserLoginForm,ContactForm
from ..models import CustomUser, Book, Transaction
import requests
from django.http import HttpResponse
from django.http import JsonResponse
import calendar
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from .examtype_views import ExamType
from .examdate_views import ExamDate

# Create your views here.
def index(request):
    return render(request, 'webapp/index.html')

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

#Home Redirect
@login_required
def home(request):
    # Retrieve all exam types and exam dates
    exam_types = ExamType.objects.all()
    exam_dates = ExamDate.objects.all()

    # Separate exam types based on test_type attribute
    paper_exam = exam_types.filter(test_type='paper').first()
    computer_exam = exam_types.filter(test_type='computer').first()
    visa_exam = exam_types.filter(test_type='visa').first()
    lifeskill_exam = exam_types.filter(test_type='lifeskill').first()

    # Count number of students, partners, and booked exams
    student_count = CustomUser.objects.filter(role='student').count()
    partner_count = CustomUser.objects.filter(role='partner').count()
    exam_booked_count = Book.objects.count()

    # Construct context dictionary to pass to template
    context = {
        'paper_exam': paper_exam,
        'computer_exam': computer_exam,
        'visa_exam': visa_exam,
        'lifeskill_exam': lifeskill_exam,
        'exam_types': exam_types,
        'exam_dates': exam_dates,
        'student_count': student_count,
        'partner_count': partner_count,
        'exam_booked_count': exam_booked_count,
    }

    return render(request, 'home.html', context)


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

#Password Reset
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')

#Register user list for admin view only
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = CustomUser.objects.all()  
    user_role = None
    
    if request.user.is_authenticated:
        user_role = request.user.role 
    
    context = {
        'users': users,
        'user_role': user_role,
    }
    
    return render(request, 'admin/user_list.html', context)

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

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('index')  # Redirect to the same URL after form submission
    else:
        form = ContactForm()

    return render(request, 'webapp/contact_us.html', {'form': form})

#Register the student from admin & partner portal
@login_required
def sub_register_student(request):
    if request.method == 'POST':
        form = SignUpSubForm(request.POST)
        if form.is_valid():
            form.save(registered_by=request.user)  
            return redirect('booking_form')
    else:
        form = SignUpSubForm()
    
    return render(request, 'webapp/sub_register_student.html', {'form': form})

#Registed list the student from admin & partner portal
@login_required
def sub_register_student_list(request):
    if request.user.is_superuser:
        # Admin can view all students registered by admins and partners
        students = CustomUser.objects.filter(role='student').exclude(registered_by=None)
    elif request.user.role == 'partner':
        # Partner can only view students they registered
        students = CustomUser.objects.filter(registered_by=request.user, role='student').exclude(registered_by=None)
    else:
        # Handle unauthorized access or redirect to appropriate view
        return HttpResponse("Unauthorized access", status=403)

    context = {
        'students': students
    }
    return render(request, 'webapp/user_list.html', context)



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
# @login_required
# def create_exam_type(request):
#     if request.method == 'POST':
#         form = ExamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('exam_type_list')  # Redirect to a URL where you list all exam types
#     else:
#         form = ExamForm()
#     return render(request, 'exam/exam_type.html', {'form': form})

# @login_required
# def exam_type_list(request):
#     exam_types = ExamType.objects.all()
#     return render(request, 'exam/exam_list.html', {'exam_types': exam_types})

# @login_required
# def exam_detail(request, pk):
#     exam_type = get_object_or_404(ExamType, pk=pk)
#     return render(request, 'exam/exam_details.html', {'exam_type': exam_type})

# @login_required
# def examtype_edit(request, pk):
#     examtype = get_object_or_404(ExamType, pk=pk)
#     if request.method == 'POST':
#         form = ExamForm(request.POST, instance=examtype)
#         if form.is_valid():
#             form.save()
#             return redirect('examtype_list')
#     else:
#         form = ExamForm(instance=examtype)
#     return render(request, 'exam/exam_type.html', {'form': form})

# @login_required
# def exam_delete(request, pk):
#     exam_type = get_object_or_404(ExamType, pk=pk)
#     exam_type.delete()
#     return redirect('exam/examtype_list')

#For Transaction
@login_required
def payment(request):
    booking = Book.objects.first()  
    if booking:
        return render(request, 'transaction/payment.html', {'booking': booking})
    else:
        return HttpResponse("No booking found")
    
# def history(request):
#     transactions = Transaction.objects.all()
#     return render(request, 'transaction/history.html', {'transactions': transactions})
    

# @login_required
# def initkhalti(request, booking_id):
#     booking = get_object_or_404(Book, pk=booking_id)
#     exam_type = booking.exam_type
#     amount = exam_type.newest_fee
    
#     url = "https://a.khalti.com/api/v2/epayment/initiate/"
#     return_url = "http://127.0.0.1:8000/verify/"
#     purchase_order_id = request.POST.get('purchase_order_id')

#     # Convert PhoneNumber object to string
#     phone_number = str(booking.mobileno)

#     payload = {
#         "return_url": return_url,
#         "website_url": "http://127.0.0.1:8000",
#         "amount": amount,
#         "purchase_order_id": purchase_order_id,
#         "purchase_order_name": "test",
#         "customer_info": {
#             "name": booking.name,
#             "email": booking.email,
#             "phone": phone_number  # Use the string representation of PhoneNumber
#         }
#     }

#     headers = {
#         'Authorization': 'key b53d9c64376448d4b1e190ba4916e6b3',
#         'Content-Type': 'application/json',
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         response_data = response.json()
#         print(response_data)  # Optionally print the response for debugging

#         # Redirect to the payment_url returned from Khalti
#         return redirect(response_data['payment_url'])

#     except requests.RequestException as e:
#         # Handle any exceptions that occur during the request
#         return JsonResponse({'error': str(e)}, status=500) 
      
# @login_required
# def verifykhalti(request):
#     pidx = request.GET.get('pidx')
#     status = request.GET.get('status')
#     transaction_id = request.GET.get('transaction_id')
#     tidx = request.GET.get('tidx')
#     amount = request.GET.get('amount')
#     total_amount = request.GET.get('total_amount')
#     mobile = request.GET.get('mobile')
#     purchase_order_id = request.GET.get('purchase_order_id')
#     purchase_order_name = request.GET.get('purchase_order_name')

#     if not pidx:
#         return JsonResponse({'error': 'pidx parameter is missing'}, status=400)

#     # Convert amount and total_amount to decimal
#     try:
#         amount = float(amount)
#         total_amount = float(total_amount)
#     except (ValueError, TypeError):
#         return JsonResponse({'error': 'Invalid amount format'}, status=400)

#     # Save the transaction data to the database
#     transaction = Transaction(
#         pidx=pidx,
#         status=status,
#         transaction_id=transaction_id,
#         tidx=tidx,
#         amount=amount,
#         total_amount=total_amount,
#         mobile=mobile,
#         purchase_order_id=purchase_order_id,
#         purchase_order_name=purchase_order_name,
#     )
#     transaction.save()

#     context = {
#         'transaction': {
#             'pidx': pidx,
#             'status': status,
#             'transaction_id': transaction_id,
#             'tidx': tidx,
#             'amount': amount,
#             'total_amount': total_amount,
#             'mobile': mobile,
#             'purchase_order_id': purchase_order_id,
#             'purchase_order_name': purchase_order_name,
#         }
#     }

#     if status == 'Completed':
#         return render(request, 'transaction/verify.html', context)
#     else:
#         context['error'] = 'Transaction not completed'
#         return render(request, 'transaction/verify.html', context)


import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from ..utils import generate_token

def payment_form(request):
    return render(request, 'payments/connectips_form.html')

def initiate_payment(request):
    if request.method == 'POST':
        txn_id = f'txn-{int(datetime.datetime.now().timestamp())}'
        txn_date = datetime.datetime.now().strftime('%d-%m-%Y')
        txn_amt = request.POST['txn_amt']
        reference_id = request.POST['reference_id']
        remarks = request.POST['remarks']
        particulars = request.POST['particulars']
        
        data = {
            'MERCHANTID': settings.CONNECTIPS_MERCHANT_ID,
            'APPID': settings.CONNECTIPS_APP_ID,
            'APPNAME': settings.CONNECTIPS_APP_NAME,
            'TXNID': txn_id,
            'TXNDATE': txn_date,
            'TXNCRNCY': 'NPR',
            'TXNAMT': txn_amt,
            'REFERENCEID': reference_id,
            'REMARKS': remarks,
            'PARTICULARS': particulars,
        }
        
        token = generate_token(data)
        data['TOKEN'] = token
        print(data)  # Print the data for debugging purposes
        # Save transaction in database
        Transaction.objects.create(
            txn_id=txn_id,
            txn_date=datetime.datetime.strptime(txn_date, '%d-%m-%Y'),
            txn_amt=txn_amt,
            reference_id=reference_id,
            remarks=remarks,
            particulars=particulars
         )
        
        context = {
            'connectips_url': f"{settings.CONNECTIPS_BASE_URL}/connectipswebgw/loginpage",
            'merchant_id': data['MERCHANTID'],
            'app_id': data['APPID'],
            'app_name': data['APPNAME'],
            'txn_id': data['TXNID'],
            'txn_date': data['TXNDATE'],
            'txn_amt': data['TXNAMT'],
            'reference_id': data['REFERENCEID'],
            'remarks': data['REMARKS'],
            'particulars': data['PARTICULARS'],
            'token': data['TOKEN'],
        }
        
        return render(request, 'payments/connectips_redirect.html', context)
    
    return redirect('payment_form')


import requests
from django.http import JsonResponse
from django.conf import settings
from ..models import Transaction
from ..utils import generate_token

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import Transaction
from ..utils import generate_token  # Ensure you have a utility function to generate the token

def validate_transaction(request):
    txn_id = request.GET.get('TXNID')
    if not txn_id:
        return JsonResponse({'error': 'TXNID not provided'}, status=400)

    # Fetch the transaction amount from the database
    transaction = get_object_or_404(Transaction, txn_id=txn_id)
    txn_amt = transaction.txn_amt

    # Prepare data for token generation
    data = {
        'MERCHANTID': settings.CONNECTIPS_MERCHANT_ID,
        'APPID': settings.CONNECTIPS_APP_ID,
        'REFERENCEID': txn_id,
        'TXNAMT': txn_amt,
    }

    # Generate the token
    token = generate_token(data)
    
    # Authentication credentials
    auth = (settings.CONNECTIPS_APP_ID, settings.CONNECTIPS_PASSWORD)
    
    # Payload for the validation request
    payload = {
        'merchantId': settings.CONNECTIPS_MERCHANT_ID,
        'appId': settings.CONNECTIPS_APP_ID,
        'referenceId': txn_id,
        'txnAmt': txn_amt,
        'token': token,
    }

    # Send the request to ConnectIPS
    response = requests.post(
        f"{settings.CONNECTIPS_BASE_URL}/connectipswebws/api/creditor/validatetxn",
        auth=auth,
        json=payload
    )

    # Parse the response JSON
    response_data = response.json()
    
    # Update the transaction status in the database
    if response_data.get('status') == 'SUCCESS':
        transaction.status = 'SUCCESS'
    else:
        transaction.status = 'FAILED'
    transaction.save()
    
    # Prepare the context for the template
    context = response_data

    # Render the appropriate template based on the transaction status
    if response_data.get('status') == 'SUCCESS':
        return render(request, 'transactionResponse/success.html', context)
    else:
        return render(request, 'transactionResponse/failure.html', context)
