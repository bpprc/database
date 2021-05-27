from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            "That’s your subject",
            "That’s your message body",
            "ruchirjd@gmail.com",
            ["sureshcbt@gmail.com"],
            fail_silently=False,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "That’s your subject")
        self.assertEqual(
            mail.outbox[0].body, "That’s your message body"
        )
