from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class UserSubmission(models.Model):

    submittersname = models.CharField(max_length=25, null=True, blank=True)
    submittersemail = models.EmailField(max_length=70, null=True, blank=False)
    proteinname = models.CharField(max_length=25, null=True, blank=True)
    proteinsequence = models.TextField(null=True, blank=False)
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    bacterium_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    taxonid = models.CharField(max_length=25, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    accessionnumber = models.CharField(max_length=25, blank=True, null=False)
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    toxicto = models.CharField(max_length=250, blank=True, null=False)
    nontoxic = models.CharField(max_length=250, blank=True, null=False)
    dnasequence = models.TextField(null=True, blank=False)
    pdbcode = models.CharField(max_length=10, blank=True, null=False)
    publication = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)
    # date = models.DateField(default=timezone.now, blank=True)

    class Meta:
        ordering = ('submittersemail',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


def save_post(sender, instance, **kwargs):
    sequence_message = "The bot is monitoring the sequence submission in the bpprc database for a day. If there is a new submission you will be notified through this email."

    send_mail(
        subject="New Submission for the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com', 'Berry@cardiff.ac.uk'],
        fail_silently=False,
    )


def _trigger_email_everyday():

    sequence_message = "The bot is monitoring the sequence submission in the bpprc database for a day. If there is a new submission you will be notified through this email."

    send_mail(
        subject="New Sequence submission in the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com', 'n.crickmore@sussex.ac.uk'],
        fail_silently=False,
    )


post_save.connect(save_post, sender=UserSubmission)
