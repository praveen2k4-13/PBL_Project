from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import Subject, Staff, StudentResult
from .forms import EditResultForm
from django.urls import reverse


class EditResultView(View):
    template_name = "staff_template/edit_student_result.html"

    def get(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, admin=request.user)
        form = EditResultForm()
        # Limit subjects to those taught by this staff
        form.fields['subject'].queryset = Subject.objects.filter(staff=staff)
        context = {
            'form': form,
            'page_title': "Edit Student's Result"
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, admin=request.user)
        form = EditResultForm(request.POST)
        # Limit subjects again for validation
        form.fields['subject'].queryset = Subject.objects.filter(staff=staff)
        context = {
            'form': form,
            'page_title': "Edit Student's Result"
        }
        if form.is_valid():
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            test = form.cleaned_data['test']
            exam = form.cleaned_data['exam']
            result, created = StudentResult.objects.get_or_create(student=student, subject=subject)
            result.test = test
            result.exam = exam
            result.save()
            if created:
                messages.success(request, "Result created successfully.")
            else:
                messages.success(request, "Result updated successfully.")
            return redirect(reverse('edit_student_result'))
        else:
            messages.warning(request, "Please correct the errors below.")
        return render(request, self.template_name, context)
