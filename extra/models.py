from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    """ """
    name = models.CharField(max_length=75, null=True, blank=True)
    subject = models.CharField(max_length=75, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=False)
    message = models.TextField(blank=True, null=False)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)

    def __str__(self):
        return 'New Feedback ' + self.email

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = "Feedback"
