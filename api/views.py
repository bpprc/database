from django.shortcuts import render
from api.forms import NeedleAPIForm
from database.models import PesticidalProteinDatabase
# from api import emboss_needle


def needle_api(request):
    # use 127.0.0.1:8000/home_api
    response = requests.get('http://ip-api.com/json/128.227.118.11')
    geodata = response.json()
    return render(request, 'api/home_api.html', {
        'ip': geodata
    })


def needle_api_form(request):
    form = NeedleAPIForm()
    return render(request, 'api/best_match_finder_database.html', {'form': form})


def needle_api_run(request):
    """ This runs bestmatchfinder from the database."""
    if request.method == 'POST':
        form = NeedleAPIForm(request.POST)
        print(form)
