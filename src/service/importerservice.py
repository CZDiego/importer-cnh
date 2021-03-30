from .httpclient import *
from variables import IMPORTER_SERVICE_VARIABLES

class ImporterService:
    BASE_URL = IMPORTER_SERVICE_VARIABLES.get("BaseURL")
    IMPORT_CONTENT_URL = BASE_URL + IMPORTER_SERVICE_VARIABLES.get("ImporterURL")

    def saveItem(data):
        print(ImporterService.IMPORT_CONTENT_URL)
        return HttpClient.post(ImporterService.IMPORT_CONTENT_URL, data)


