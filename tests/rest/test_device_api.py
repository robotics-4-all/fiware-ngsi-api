from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration

from fiware_ngsi_api.api.services import NgsiService
from fiware_ngsi_api.api.devices import NgsiDevice

import json

API_KEY = "1234abcd"


if __name__ == "__main__":
    config = NgsiConfiguration(file_path="../../conf/settings.conf")
    api_client = NgsiApiClient(configuration=config)

    service_api = NgsiService(api_client=api_client)
    device_api = NgsiDevice(api_client=api_client)

    # create a new service
    response = service_api.create(api_key=API_KEY, type="Robot")

    # create a new device
    attrs = {
        "test1": {
            "type": "test1",
            "val": 1
        },
        "test2": {
            "type": "test2",
            "val": 1
        }
    }

    response = device_api.create(id=1, type="test", attrs=attrs)

    # update the device
    new_attrs = {
        "test1": 3
    }

    response = device_api.update(id=1, type="test", new_attrs=new_attrs)

    # list the device
    response = device_api.list(id=1, type="Robot")
    response_msg = json.loads(response.data)
    print("Device: ", response_msg)

    # # list al devices
    response = device_api.list()
    response_msg = json.loads(response.data)
    print("Devices: ", response_msg)

    # # delete the device
    response = device_api.delete(id="Robotundefined")

    # # delete the newly created service
    response = service_api.delete(api_key=API_KEY)
