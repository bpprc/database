from datetime import datetime, time, timedelta

from celery import shared_task
from django.core.mail import send_mail

from extra.models import Feedback
from namingalgorithm.models import UserSubmission


@shared_task
def run_needle(filename):
    try:
        align = submit_single_sequence.align.run_bug(filename)
        return align
    except IOError as e:
        print(e)


def trigger_email_everyday():
    #name, email = extract_email()
    sequence_message = """Dear Dr.Neil Crickmore and Dr.Colin Berry,
There is a new sequence submission in the database. Please check the database admin page for more details."""

    send_mail(
        subject="New Submission for the database",
        message=sequence_message,
        from_email="bpprc.database@gmail.com",
        recipient_list=[
            "sureshcbt@gmail.com",
            "n.crickmore@sussex.ac.uk",
            "Berry@cardiff.ac.uk",
        ],
        fail_silently=False,
    )


def trigger_email_everyday_feedback():
    sequence_message = """Dear Dr.Neil Crickmore and Dr.Colin Berry,
There is a new feedback in the database page. Please check the database admin Feedback page for more details."""

    send_mail(
        subject="New Feedback for the database",
        message=sequence_message,
        from_email="bpprc.database@gmail.com",
        recipient_list=[
            "sureshcbt@gmail.com",
            "n.crickmore@sussex.ac.uk",
            "Berry@cardiff.ac.uk",
        ],
        fail_silently=False,
    )


def trigger_email_bpprc_SSL_status():
    sequence_message = """Dear Dr.Neil Crickmore and Dr.Colin Berry,
    There is a new feedback in the database page. Please check the bpprc site SSL certification status. It appears not secure"""

    send_mail(
        subject="BPPRC SSL status",
        message=sequence_message,
        from_email="bpprc.database@gmail.com",
        recipient_list=["sureshcbt@gmail.com"],
        fail_silently=False,
    )


def trigger_email_camtech_SSL_status():
    sequence_message = """Dear Dr.Neil Crickmore and Dr.Colin Berry,
    There is a new feedback in the database page. Please check the camtech database site SSL certification status. It appears not secure"""

    send_mail(
        subject="camtech database SSL status",
        message=sequence_message,
        from_email="bpprc.database@gmail.com",
        recipient_list=["sureshcbt@gmail.com"],
        fail_silently=False,
    )


def feedback():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    return Feedback.objects.filter(
        uploaded__gte=datetime.date(today_start),
        uploaded__lte=datetime.date(today_end),
    )


def filter_by_date():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    return UserSubmission.objects.filter(
        uploaded__gte=datetime.date(today_start),
        uploaded__lte=datetime.date(today_end),
    )


def extract_email():
    name, email = ''
    id = UserSubmission.objects.latest('id')
    if id.submittersname:
        name = id.submittersname
    if id.submittersemail:
        email = id.submittersemail
    return name, email


@shared_task
def run():
    print("I am the email job")
    if filter_by_date():
        # Model.objects.latest('field')
        trigger_email_everyday()
    if feedback():
        trigger_email_everyday_feedback()


# https://medium.com/@yedjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7
# def sleep_sometime():
#     schedule.run_pending()
#     time.sleep(60)
#
# schedule.every().day.at("17:25").do(check_new_submission())


@shared_task
def check_bpprc_ssl_status():
    print("I check the SSL status of bpprc site")
    import requests

    try:
        requests.get("https://www.bpprc.org", verify=True)
    except SSLError:
        trigger_email_bpprc_SSL_status()


@shared_task
def check_camtech_ssl_status():
    print("I check the SSL status of bpprc site")
    import requests

    try:
        requests.get("https://camtech-bpp.ifas.ufl.edu/", verify=True)
    except SSLError:
        trigger_email_camtech_SSL_status()
