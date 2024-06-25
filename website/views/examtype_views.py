from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import ExamTypeForm
from ..models import ExamType

@login_required
def exam_list(request):
    examtypes = ExamType.objects.all()
    return render(request, 'examtype/exam_list.html', {'examtypes': examtypes})

@login_required
def examtype_detail(request, pk):
    examtype = get_object_or_404(ExamType, pk=pk)
    return render(request, 'examtype/exam_details.html', {'examtype': examtype})

@login_required
def examtype_create(request):
    if request.method == 'POST':
        form = ExamTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examdate_create')
    else:
        form = ExamTypeForm()
    return render(request, 'examtype/exam_type.html', {'form': form})

@login_required
def examtype_update(request, pk):
    examtype = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        form = ExamTypeForm(request.POST, instance=examtype)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamTypeForm(instance=examtype)
    return render(request, 'examtype/exam_type.html', {'form': form})

@login_required
def examtype_delete(request, pk):
    examtype = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        examtype.delete()
        return redirect('exam_list')
    return render(request, 'examtype/examtype_confirm_delete.html', {'examtype': examtype})
