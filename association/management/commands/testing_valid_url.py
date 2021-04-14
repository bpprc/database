from django.core.management.base import BaseCommand
from association.models import Association
import requests


def doi2bib(doi):
    """
    Return a bibTeX string of metadata for a given DOI.
    """

    url = "http://dx.doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return r.text


def return_final_url(url_link):
    response = requests.get(url_link)
    finalurl = ''
    if response.history:
        for resp in response.history:
            print(resp)
        finalurl = response.url
    return finalurl


class Command(BaseCommand):
    help = 'Prints inactive urls (404)'

    def handle(self, *args, **kwargs):
        for item in Association.objects.all():
            base_url = "https://doi.org/"
            url = base_url + item.publication
            print('url', url)
            finalurl = return_final_url(url)
            print("finalurl", finalurl)

            response = requests.get(finalurl, cookies=cookies)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print("HTTPError")
                print("Name", item.name)
                print("publication", item.publication)
