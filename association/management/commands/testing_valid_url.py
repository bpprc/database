from django.core.management.base import BaseCommand
from association.models import Association
import requests
from requests.exceptions import MissingSchema


def doi2bib(doi):
    """
    Return a bibTeX string of metadata for a given DOI.
    """

    url = "http://dx.doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url)

    return r.text


def return_final_url(url_link):
    finalurl = ''
    try:
        response = requests.get(url_link)
        if response.history:
            for resp in response.history:
                print(resp)
            finalurl = response.url
        return finalurl
    except MissingSchema:
        # print("MissingSchema", url_link)
        return None


class Command(BaseCommand):
    help = 'Prints inactive urls (404)'
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    def handle(self, *args, **kwargs):
        for item in Association.objects.all():
            base_url = "https://doi.org/"
            url = base_url + item.publication
            # print('Testing this URL:', url)
            finalurl = return_final_url(url)

            if finalurl:
                # print("finalurl", finalurl)
                response = requests.get(finalurl, headers=self.headers)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print("HTTPError")
                    print("Name", item.name)
                    print("publication", item.publication)
                    pass
            else:
                print("Name", item.name)
                print("publication", item.publication)
                print("Something is wrong with link:", finalurl)
                pass
            # else:
            #     print("Name", item.name)
            #     print("publication", item.publication)
            #     pass
