from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import BookExamType, CustomUser
from ..forms import BookTypeForm
from .examtype_views import ExamType
from .examdate_views import ExamDate

# Views for ExamDate
@login_required
def booked_type(request):
    if request.method == 'POST':
        form = BookTypeForm(request.POST)
        if form.is_valid():
            exam_type = form.cleaned_data['exam_type']
            exam_date = form.cleaned_data['exam_date']
            booking = BookExamType(user=request.user, exam_type=exam_type, exam_date=exam_date)
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('booking_form')
        else:
            messages.error(request, 'Form submission failed. Please correct errors below.')
    else:
        form = BookTypeForm()

    exam_types = ExamType.objects.all()
    exam_dates = ExamDate.objects.all()

    context = {
        'form': form,
        'exam_types': exam_types,
        'exam_dates': exam_dates,
    }
    return render(request, 'bookedexam/exam_selection.html', context)

@login_required
def booked_list(request):
    user_role = request.user.role
    categorized_bookings = {}

    # Fetch bookings based on user role
    if user_role == 'admin':
        all_bookings = BookTypeForm.objects.all().order_by('-created_at')
    else:
        all_bookings = BookTypeForm.objects.filter(created_by=request.user).order_by('-created_at')

    # Get distinct creators of the fetched bookings
    creators = CustomUser.objects.filter(book__in=all_bookings).distinct()

    # Categorize bookings by creator
    categorized_bookings = {creator: all_bookings.filter(created_by=creator) for creator in creators}

    # Fetch booked exam types for the authenticated user
    bookings = BookExamType.objects.filter(user=request.user)

    return render(request, 'bookedexam/booked_list.html', {
        'bookings': bookings,
        'categorized_bookings': categorized_bookings,
        'user_role': user_role
    })


@login_required
def booked_detail(request, pk):
    booking = get_object_or_404(BookExamType, pk=pk)
    return render(request, 'bookedexam/booked_details.html', {'booking': booking})

@login_required
def booked_edit(request, pk):
    booking = get_object_or_404(BookExamType, pk=pk)
    if request.method == 'POST':
        form = BookTypeForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('booked_list')
        else:
            messages.error(request, 'Form submission failed. Please correct errors below.')
    else:
        form = BookTypeForm(instance=booking)

    return render(request, 'bookedexam/exam_selection.html', {'form': form, 'booking': booking})

@login_required
def booked_delete(request, pk):
    booking = get_object_or_404(BookExamType, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
        return redirect('booked_list')
    return render(request, 'bookedexam/booked_delete_confirm.html', {'booking': booking})