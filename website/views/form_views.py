from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Book, CustomUser
from ..forms import BookForm, MobileEmailForm
from .examtype_views import ExamType
from .examdate_views import ExamDate

#bookinfg form crud
@login_required
def booking_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            return redirect('booking_detail', pk=book.pk)
        else:
            print(form.errors)  # Print form errors to console for debugging
    else:
        form = BookForm()
    
    exam_types = ExamType.objects.all()
    exam_dates = ExamDate.objects.all()  # Define exam_dates

    return render(request, 'booking/booking_form.html', {'form': form, 'exam_types': exam_types, 'exam_dates': exam_dates})

@login_required
def booking_list(request):
    user_role = None
    categorized_bookings = {}

    if request.user.is_authenticated:
        user_role = request.user.role
        
        # Fetch all bookings ordered by created_at descending
        if user_role == 'admin':
            all_bookings = Book.objects.all().order_by('-created_at')
        else:
            all_bookings = Book.objects.filter(created_by=request.user).order_by('-created_at')

        # Get distinct creators of the fetched bookings
        creators = CustomUser.objects.filter(book__in=all_bookings).distinct()

        # Categorize bookings by creator
        categorized_bookings = {creator: all_bookings.filter(created_by=creator) for creator in creators}

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