from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.api.sensor_device import RobotDevice, DeviceType
from fiware_ngsi_api.api.device_groups import NgsiGroups
from fiware_ngsi_api.api.entities import NgsiEntities

import json
import time


API_KEY = "1234"
SENSOR_TYPE = DeviceType.ROBOT
ROBOT_ID = "001"

if __name__ == "__main__":
    config = NgsiConfiguration("../conf/settings.conf")
    client = NgsiApiClient(configuration=config)

    ngsi_group = NgsiGroups(
        type=SENSOR_TYPE,
        api_key=API_KEY,
        api_client=client
    )

    ngsi_group.create()

    robot_001 = RobotDevice(ROBOT_ID, client, ngsi_group)

    nsgi_entities = NgsiEntities(api_client=client)

    response = nsgi_entities.update_existing_entity_attributes(
        entity_id="urn:ngsi-ld:Robot:001",
        body={
            "state": {
                "type": "enum",
                "value": {
                    "val": "HIGH"
                }
            }
        },
        fiware_service="openiot",
        fiware_service_path="/"
    )

    print("Updating current entity! \n", response.data)

    response = nsgi_entities.list_entities(
        type="Robot",
        attrs="state",
        options="keyValues",
        fiware_service="openiot",
        fiware_service_path="/"
    )

    response = json.loads(response.data)

    print("Listing all current entities! \n", response)
