"""Predicts the name for the submitted pesticidal proteins ."""


import tempfile
import textwrap
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from naming_package import run_data
from database.models import PesticidalProteinDatabase, PesticidalProteinPrivateDatabase
from namingalgorithm.models import UserSubmission
from .forms import UserSubmissionForm, SendEmailForm
from django.core.mail import send_mail


def is_admin(user):
    """Check the user is admin staff."""
    return user.is_staff


@user_passes_test(is_admin)
def naming_algorithm(request):
    """If the user is admin staff, show the naming html page."""
    return render(request, 'newwebpage/naming_home.html')


def submit_home(request):
    context = {
        'form': UserSubmissionForm,
    }
    return render(request, 'newwebpage/submit_update.html', context)


def submit(request):
    """Submit the sequence for the naming purpose through user form."""
    if request.method == "POST":
        form = UserSubmissionForm(request.POST)
        # formset = ToxicToFormSet(request.POST)
        # print(form)
        if form.is_valid():
            # print("formset", formset)
            form.save()

            return render(request, 'newwebpage/view.html', {'form': form})
        # else:
        #     print(form.errors)
        #     print("Error in form")
            # print("formset", formset)
    else:
        form = UserSubmissionForm()
    #     formset = ToxicToFormSet()
    # helper = ToxicFormSetHelper()

    return render(request, 'newwebpage/submit.html', {'form': form})


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


def _trigger_email_everyday(submittersname, submittersemail, accession, message):
    recipient_list = []
    recipient_list.append(submittersemail)
    send_mail(
        subject=accession,
        message=message,
        from_email='bpprc.database@gmail.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )


def contact_email(request):
    if request.method == 'GET':
        form = SendEmailForm(initial=request.GET.dict())
    else:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            submittersname = form.cleaned_data['submittersname']
            submittersemail = form.cleaned_data['submittersemail']
            accession = form.cleaned_data['accession']
            message = form.cleaned_data['message']
            try:
                _trigger_email_everyday(
                    submittersname, submittersemail, accession, message)
                form.save()
            except:
                return HttpResponse('Invalid header found.')

            context = \
                {'submittersname': submittersname,
                 'submittersemail': submittersemail}
            return render(request, "namingalgorithm/email_success.html", context)
    return render(request, "namingalgorithm/email.html", {'form': form})


def success_email(request):
    return HttpResponse('Success! Your message sent. See SendEmail for the list of emails')


# def cloneUserSubmission(request):
#     id = request.GET['id']
#     model = request.GET['model']
#     instance = UserSubmission.objects.get(id=id)
#     created_model = None
#
#     if model == 'private':
#         try:
#             created_model = PesticidalProteinPrivateDatabase.objects.create(
#                 submittersname=instance.submittersname,
#                 submittersemail=instance.submittersemail,
#                 name=instance.name,
#                 sequence=instance.sequence,
#                 bacterium=instance.bacterium,
#                 bacterium_textbox=instance.bacterium_textbox,
#                 taxonid=instance.taxonid,
#                 year=instance.year,
#                 accession=instance.accession,
#                 partnerprotein=instance.partnerprotein,
#                 partnerprotein_textbox=instance.partnerprotein_textbox,
#                 toxicto=instance.toxicto,
#                 nontoxic=instance.nontoxic,
#                 dnasequence=instance.dnasequence,
#                 pdbcode=instance.pdbcode,
#                 publication=instance.publication,
#                 comment=instance.comment,
#                 admin_comments=instance.admin_comments,
#             )
#         except psycopg2.errors.NotNullViolation:
#             return HttpResponse("Name cannot be empty", status=400)
#     else:
#         created_model = PesticidalProteinDatabase.objects.create(
#             submittersname=instance.submittersname,
#             submittersemail=instance.submittersemail,
#             name=instance.name,
#             sequence=instance.sequence,
#             bacterium=instance.bacterium,
#             bacterium_textbox=instance.bacterium_textbox,
#             taxonid=instance.taxonid,
#             year=instance.year,
#             accession=instance.accession,
#             partnerprotein=instance.partnerprotein,
#             partnerprotein_textbox=instance.partnerprotein_textbox,
#             toxicto=instance.toxicto,
#             nontoxic=instance.nontoxic,
#             dnasequence=instance.dnasequence,
#             pdbcode=instance.pdbcode,
#             publication=instance.publication,
#             comment=instance.comment,
#             admin_comments=instance.admin_comments,
#         )
#
#     return HttpResponse(created_model.id)
