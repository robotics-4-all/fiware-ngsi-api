from fiware_ngsi_api.api.devices import NgsiDevice
from fiware_ngsi_api.api.services import NgsiServices
from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient
from yaml.loader import SafeLoader
import yaml
import os


class RobotAPI:
    ENTITY_TYPE = 'Robot'

    def __init__(self, api_client, file_path, service, service_path):
        self._service = service
        self._service_paht = service_path

        if not os.path.exists(file_path):
            print('Invalid Path!')

        with open(file_path) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(data)

        self.id = data['Robots']['id']

        print(self.id)

        self._service = NgsiServices(
            api_client, type=RobotAPI.ENTITY_TYPE, api_key=24546)

        print(self._service.list())


if __name__ == "__main__":
    API_KEY = "1234"
    SENSOR_TYPE = "Robot"
    ROBOT_ID = "001"

    if __name__ == "__main__":
        config = NgsiConfiguration("../../conf/settings.conf")
        client = NgsiApiClient(configuration=config)

        robot = RobotAPI(client, '../../data-models/robot.yaml', 1, 2)
