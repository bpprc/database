"""Predicts the name for the submitted pesticidal proteins ."""


import tempfile
import textwrap
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from naming_package import run_data
from namingalgorithm.models import UserSubmission
from .forms import UserSubmissionForm, SendEmailForm
from django.core.mail import send_mail


def send_mail(required):
    email_text = send_mail(
        subject="New Submission",
        message="There is a new sequence submission.",
        from_email=['bpprc.database@gmail.com'],
        recipient_list=['sureshcbt@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse(f"Email sent to {email_text} members")


def is_admin(user):
    """Check the user is admin staff."""
    return user.is_staff


@user_passes_test(is_admin)
def naming_algorithm(request):
    """If the user is admin staff, show the naming html page."""
    return render(request, 'namingalgorithm/naming_home.html')


def submit_home(request):
    context = {
        'form': UserSubmissionForm,
    }
    return render(request, 'namingalgorithm/submit_update.html', context)


def submit(request):
    """Submit the sequence for the naming purpose through user form."""
    if request.method == "POST":
        print("hi")
        form = UserSubmissionForm(request.POST)
        # formset = ToxicToFormSet(request.POST)
        # print(form)
        if form.is_valid():
            # post = form.save()

            # print("formset", formset)
            form.save()

            return render(request, 'namingalgorithm/view.html', {'form': form})
        else:
            # print("form", form)
            print(form.errors)
            print("Error in form")
            # print("formset", formset)

    else:
        form = UserSubmissionForm()
    #     formset = ToxicToFormSet()
    # helper = ToxicFormSetHelper()

    return render(request, 'namingalgorithm/submit.html', {'form': form})


def run_align(request):
    """Submit the sequence for the naming purpose."""
    data = request.GET.get('fulltextarea')
    format_data = textwrap.fill(data, 80)
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
    with open(tmp_seq.name, 'wb') as temp:
        temp.write(format_data.encode())
        tmp_seq.close()

    align = run_data.predict_name.run_bug(tmp_seq.name)
    user_submission = UserSubmission.objects.get(
        id=request.GET.get('submission_id'))
    user_submission.alignresults = align
    user_submission.save()
    return HttpResponseRedirect('/admin/namingalgorithm/usersubmission/')


def align_results(request):
    """Submit the sequence for the naming purpose."""
    submission_id = request.GET.get('submission_id')
    submission = UserSubmission.objects.get(id=submission_id)
    align = submission.alignresults
    context = {
        'align': align
    }
    return render(request, 'bestmatchfinder/needle.html', context)


def run_naming_algorithm(request):
    """Submit the sequence for the naming purpose."""
    data = request.GET.get('fulltextarea')
    format_data = textwrap.fill(data, 80)
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
    with open(tmp_seq.name, 'wb') as temp:
        temp.write(data.encode())
        tmp_seq.close()

    align, percentageidentity, category, predicted_name, name = run_data.predict_name.run_bug(
        tmp_seq.name)
    user_submission = UserSubmission.objects.get(
        id=request.GET.get('submission_id'))
    user_submission.predict_name = predicted_name
    user_submission.save()

    context = {
        'category': category,
        'predicted_name': predicted_name,
        'name': name,
        'align': align
    }
    return render(request, 'namingalgorithm/needle.html', context)


def contactView(request):
    if request.method == 'GET':
        form = SendEmailForm()
    else:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            submittersname = form.cleaned_data['submittersname']
            submittersemail = form.cleaned_data['submittersemail']
            proteinname = form.cleaned_data['proteinname']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          ['sureshcbt@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "namingalgorithm/email.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
