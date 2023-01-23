from fiware_ngsi_api.api.entities import NgsiEntities
from fiware_ngsi_api.api.services import NgsiService
from fiware_ngsi_api.api.devices import NgsiDevice
from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration

from enum import Enum

import json
import yaml
import os


class AbstractModelTypes(Enum):
    Robot = 1
    RobotKPI = 2
    Warehouse = 3
    WarehouseFloor = 4
    WarehouseKPI = 5
    Room = 6
    Rack = 7
    Self = 8
    Slot = 9
    Pallet = 10
    Parcel = 11


def is_response_valid(status):
    if int(status / 100) == 2:
        return True

    return False


class AbstactEntity(NgsiEntities):
    MODEL_PATH_PREFIX = "../../data-models/"

    def __init__(self, api_client: NgsiApiClient, model_type: AbstractModelTypes, entity_id: int, service="openiot", service_path="/"):
        # pass the given parameters
        self._abstract_model = {}
        self._api_client = api_client
        self._model_type = model_type
        self._entity_id = entity_id
        self._service = service
        self._service_path = service_path

        # initialize base ngsi entity api
        super(AbstactEntity, self).__init__(api_client)

        self._service_api = NgsiService(self._api_client)
        self._device_api = NgsiDevice(self._api_client)

    def synchronize(self):
        self._load_abstract_model()

    @property
    def model_type(self):
        return self.model_type

    @model_type.setter
    def model_type(self, new_type):
        self._model_type = new_type

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, new_id: int):
        self._entity_id = new_id

    def get_attr_names(self):
        if not 'attributes' in self._abstract_model:
            return []

        return list(self._abstract_model['attributes'].keys())

    def attr_exists(self, attr):
        if not 'attributes' in self._abstract_model:
            return False

        if not attr in self._abstract_model['attributes']:
            return False

        return True

    def get_full_entity_id(self):
        return f"urn:ngsi-ld:{self._model_type.name}:{self._entity_id}"

    def _load_abstract_model(self):
        # check if a valid abstract type was given
        if not self._model_type in AbstractModelTypes:
            print(
                f"Error: Abstract model {self._model_type} is not registered.")

            return

        # create files full path
        file_name = f"{self._model_type.name.lower()}.yaml"
        full_path = AbstactEntity.MODEL_PATH_PREFIX + file_name

        if os.path.exists(full_path):
            with open(full_path, "r") as stream:
                try:
                    self._abstract_model = yaml.safe_load(
                        stream)[f"{self._model_type.name}"]
                    print(self._abstract_model)
                except yaml.YAMLError as e:
                    print(f"Caught error when parsing yaml file: {e}")
                except KeyError as e:
                    print(f"Caught Key value error: {e}")
        else:
            raise IOError("Invalid settings path!")

    def get_attr(self, attr: str, key_values: bool = True):
        # check that attr exists in model
        if not self.attr_exists(attr):
            print("Attr not in model")
            return {}

        # try to load it from fiware
        try:
            response = self.retrieve_entity_attributes(
                entity_id=self.get_full_entity_id(),
                type=self._model_type.name,
                attrs=attr
            )

            if is_response_valid(response.status):
                response_data = json.loads(response.data)[attr]

                if key_values:
                    return response_data['value']

                return response_data
        except Exception as e:
            print(f"Error occured when trying to get attr: {e}")

        return {}

    def set_attr(self, attr: str, value):
        # check that attr exists in model
        if not self.attr_exists(attr):
            print("Attr not in model")
            return False

        request_data = {
            attr: {
                "type": self._abstract_model['attributes'][attr]['type'],
                "value": value
            }
        }

        # try to write it to fiware
        try:
            response = self.update_existing_entity_attributes(
                entity_id=self.get_full_entity_id(),
                type=self._model_type.name,
                body=request_data
            )

            if is_response_valid(response.status):
                return True

            return False
        except Exception as e:
            print(f"Error occured when trying to get attr: {value.keys()}")
            return False


if __name__ == "__main__":
    config = NgsiConfiguration("../../conf/settings.conf")
    client = NgsiApiClient(configuration=config)

    robot_entity = AbstactEntity(client, AbstractModelTypes.Robot, 1)
    robot_entity.synchronize()

    id = robot_entity.get_full_entity_id()
    print(id)

    pose = robot_entity.get_attr("pose")
    print(pose)

    r = robot_entity.set_attr("pose", {"x": 1, "y": 4, "th": 0.7})
    print(r)

    pose = robot_entity.get_attr("pose", False)
    print(pose)

    pos_exists = robot_entity.attr_exists("pos")
    print(pos_exists)

    attrs_list = robot_entity.get_attr_names()
    print(attrs_list)
