
from celery import shared_task
from namingalgorithm.models import UserSubmission
from django.core.mail import send_mail
from datetime import timedelta, datetime, time


@shared_task
def run_needle(filename):
    try:
        align = submit_single_sequence.align.run_bug(filename)
        return align
    except IOError as e:
        print(e)


def trigger_email_everyday():
    sequence_message = '''Dear Dr.Neil Crickmore and Dr.Colin Berry,
There is a new sequence submission in the database. Please check the database admin page for more details.'''

    send_mail(
        subject="New Submission for the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com',
                        'n.crickmore@sussex.ac.uk', 'Berry@cardiff.ac.uk'],
        fail_silently=False,
    )


def filter_by_date():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    return UserSubmission.objects.filter(uploaded__gte=datetime.date(today_start),
                                         uploaded__lte=datetime.date(today_end))


@shared_task
def run():
    print("I am the email job")
    if filter_by_date():
        trigger_email_everyday()

# https://medium.com/@yedjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7
# def sleep_sometime():
#     schedule.run_pending()
#     time.sleep(60)
#
# schedule.every().day.at("17:25").do(check_new_submission())
