from .httpclient import *

class ImporterService:
    BASE_URL = "https://swapi.dev/"
    PEOPLE_URL = BASE_URL + "api/people/{id}"

    def getItem(id):
        id = str(id)
        service_url = ImporterService.PEOPLE_URL.format(id=id)
        return HttpClient.get(service_url)

    def saveItem(self):
        return HttpClient.get(BASE_URL)


