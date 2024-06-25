from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import ExamDate
from ..forms import ExamDateForm

# Views for ExamDate
@login_required
def examdate_list(request):
    examdates = ExamDate.objects.all()
    return render(request, 'examdate/date_list.html', {'examdates': examdates})

@login_required
def examdate_detail(request, pk):
    examdate = get_object_or_404(ExamDate, pk=pk)
    return render(request, 'examdate/date_details.html', {'examdate': examdate})

@login_required
def examdate_create(request):
    if request.method == 'POST':
        form = ExamDateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examdate_list')
    else:
        form = ExamDateForm()
    return render(request, 'examdate/examdate_form.html', {'form': form})

@login_required
def examdate_update(request, pk):
    examdate = get_object_or_404(ExamDate, pk=pk)
    if request.method == 'POST':
        form = ExamDateForm(request.POST, instance=examdate)
        if form.is_valid():
            form.save()
            return redirect('examdate_list')
    else:
        form = ExamDateForm(instance=examdate)
    return render(request, 'examdate/examdate_form.html', {'form': form})

@login_required
def examdate_delete(request, pk):
    examdate = get_object_or_404(ExamDate, pk=pk)
    if request.method == 'POST':
        examdate.delete()
        return redirect('examdate_list')
    return render(request, 'examdate/examdate_confirm_delete.html', {'examdate': examdate})
