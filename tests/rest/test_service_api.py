from fiware_ngsi_api.api.services import NgsiServices
from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration

import json

API_KEY = "1234abcd"


if __name__ == "__main__":
    config = NgsiConfiguration(file_path="../conf/settings.conf")
    api_client = NgsiApiClient(configuration=config)

    service_api = NgsiServices(api_client=api_client)

    # create a new service
    response = service_api.create(api_key=API_KEY, type="test")

    # update the new service
    body = {
        "cbroker": "http://155.207.33.189:1026",
        "entity_type": "tested"
    }

    response = service_api.update(api_key=API_KEY, body=body)

    # list the available services
    response = service_api.list()
    available_services = json.loads(response.data)
    print("Available services: ", available_services)

    # delete the newly created service
    response = service_api.delete(api_key=API_KEY)
