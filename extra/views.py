from django.shortcuts import render
from extra.forms import FeedbackForm
from extra.models import Feedback
from django.http import HttpResponse


def feedback_home(request):
    form = FeedbackForm()

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            subject = request.POST.get("subject")
            email = request.POST.get("email")
            message = request.POST.get("message")
            feedback = Feedback.objects.create(
                name=name, subject=subject, email=email, message=message)

            context = {
                'name': name,
                'subject': subject,
                'message': message,
                'email': email,
            }
            return render(request, 'extra/feedback.html', {'context': context})
        else:
            # print(form.errors)
            # print("Error in form")
            return render(request, 'extra/feedback.html', {'form': form})

    else:
        # print(form)
        form = FeedbackForm()

    return render(request, 'extra/feedback.html', {'form': form})


def github_home(request):
    return render(request, 'extra/github.html')


def faq(request):
    return render(request, 'extra/faq.html')


def privacy_policy(request):
    """Loads the homepage."""
    return render(request, 'extra/privacy-policy.html', context)


def page_not_found(request, exception):
    """ Return 404 error page."""
    return render(request, 'extra/404.html', status=404)


def server_error(request):
    """ Return server error."""
    return render(request, 'extra/500.html', status=500)


def faq(request):
    return render(request, 'extra/faq.html')
