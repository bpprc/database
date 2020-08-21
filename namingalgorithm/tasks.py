
from celery import shared_task
from namingalgorithm.models import UserSubmission
from django.core.mail import send_mail
from datetime import date


@shared_task
def run_needle(filename):
    try:
        align = submit_single_sequence.align.run_bug(filename)
        return align
    except IOError as e:
        print(e)


def trigger_email_everyday():
    sequence_message = "The bot is monitoring the sequence submission in the bpprc database for a day. If there is a new submission you will be notified through this email."

    send_mail(
        subject="New Sequence submission on the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com'],
        fail_silently=False,
    )


@shared_task
def check_new_submission():
    print('i am fine now')
    # yesterday = date.today() - timedelta(days=1)
    # submission_yesterday = UserSubmission.objects.filter(data__range=[
    #                                                      yesterday])
    # startdate = date.today()
    # startdate = start.strftime('%y%m%d')
    # enddate = startdate + timedelta(days=1)
    # enddate = end.strftime('%y%m%d')
    submission = UserSubmission.objects.filter(
        uploaded__gte=date.today())

    if submission:
        trigger_email_everyday()

# https://medium.com/@yedjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7
# def sleep_sometime():
#     schedule.run_pending()
#     time.sleep(60)
#
# schedule.every().day.at("17:25").do(check_new_submission())
