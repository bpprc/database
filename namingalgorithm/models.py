from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class AbstractModel(models.Model):
    submittersname = models.CharField(max_length=25, null=True, blank=True)
    submittersemail = models.EmailField(max_length=70, null=True, blank=False)
    name = models.CharField(max_length=25, null=True, blank=True)
    sequence = models.TextField(null=True, blank=False)
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    bacterium_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    taxonid = models.CharField(max_length=25, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    accession = models.CharField(max_length=25, blank=True, null=False)
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
    terms_conditions = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, default="1", null=False, blank=True)
    admin_comments = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    user_provided_proteinname = models.CharField(max_length=105, blank=True, null=False)

    class Meta:
        abstract = True
        ordering = ('-uploaded',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class UserSubmission(AbstractModel):
    pass


class Archive(AbstractModel):
    pass


def save_archive(sender, instance, **kwargs):
    archive = Archive()
    archive.submittersname = instance.submittersname
    archive.submittersemail = instance.submittersemail
    archive.name = instance.name
    archive.sequence = instance.sequence
    archive.bacterium = instance.bacterium
    archive.bacterium_textbox = instance.bacterium_textbox
    archive.taxonid = instance.taxonid
    archive.year = instance.year
    archive.accession = instance.accession
    archive.partnerprotein = instance.partnerprotein
    archive.partnerprotein_textbox = instance.partnerprotein_textbox
    archive.toxicto = instance.toxicto
    archive.nontoxic = instance.nontoxic
    archive.dnasequence = instance.dnasequence
    archive.pdbcode = instance.pdbcode
    archive.publication = instance.publication
    archive.comment = instance.comment
    archive.uploaded = instance.uploaded
    archive.alignresults = instance.alignresults
    archive.predict_name = instance.predict_name
    archive.terms_conditions = instance.terms_conditions
    archive.admin_user = instance.admin_user
    archive.admin_comments = instance.admin_comments
    archive.save()


class SendEmail(models.Model):
    submittersname = models.CharField(max_length=25, null=True, blank=True)
    submittersemail = models.EmailField(max_length=70, null=True, blank=False)
    name = models.CharField(max_length=25, null=True, blank=True)
    message = models.TextField(null=True, blank=True)


def _trigger_email_everyday():

    sequence_message = "The bot is monitoring the sequence submission in the bpprc database for a day. If there is a new submission you will be notified through this email."

    send_mail(
        subject="New Sequence submission in the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com'],
        fail_silently=False,
    )


def save_post(sender, instance, **kwargs):
    sequence_message = '''Dear Dr.Neil Crickmore and Dr.Colin Berry,
There is a new sequence submission in the database. Please check the database admin page for more details.'''

    send_mail(
        subject="New Submission for the database",
        message=sequence_message,
        from_email='bpprc.database@gmail.com',
        recipient_list=['sureshcbt@gmail.com','ruchirjd@gmail.com'],
        fail_silently=False,
    )


post_save.connect(save_archive, sender=UserSubmission)
post_save.connect(save_post, sender=UserSubmission)
