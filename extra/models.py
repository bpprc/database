from django.db import models


class Feedback(models.Model):
    """ """
    name = models.CharField(max_length=75, null=True, blank=True)
    subject = models.CharField(max_length=75, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=False)
    message = models.TextField(blank=True, null=False)
