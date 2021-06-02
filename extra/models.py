from django.db import models
from django.utils import timezone


TYPES_CHOICES = (
    ('emailed', 'Emailed'),
    ('pending', 'Pending'),
)


class Feedback(models.Model):
    """ """

    name = models.CharField(max_length=75, null=True, blank=True)
    subject = models.CharField(max_length=75, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=False)
    message = models.TextField(blank=True, null=False)
    uploaded = models.DateTimeField("Uploaded", default=timezone.now)
    contact_status = models.CharField(
        choices=TYPES_CHOICES, default=TYPES_CHOICES[1][1], max_length=10)

    def __str__(self):
        return "New Feedback " + self.email

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"


class Links(models.Model):
    """ """

    name = models.CharField(max_length=500)
    description = models.TextField(default="None")
    link = models.TextField()

    class Meta:
        verbose_name = "Add External Link"
        verbose_name_plural = "Add External Links"
        ordering = ("name",)

    def __str__(self):
        return self.name
