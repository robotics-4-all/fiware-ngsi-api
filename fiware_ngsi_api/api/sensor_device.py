from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.api.device_groups import NgsiGroups
from enum import Enum

import json
import time


class DeviceType(str, Enum):
    ROBOT = 'Robot'


class DeviceCommand(object):
    def __init__(self, name):
        self.name = name
        self.type = "command"

    def to_json(self):
        return self.__dict__


class DeviceBase(object):
    RESOURCE_PATH_CREATE = ":4041/iot/devices"

    HTTP_INFO = [
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, id, type, api_client):
        self.id = id
        self.type = type

        self.attributes = []

        if api_client is None:
            api_client = NgsiApiClient()
        self.api_client = api_client

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @property
    def api_client(self):
        return self._api_client

    @api_client.setter
    def api_client(self, new_api_client):
        self._api_client = new_api_client

    def _create(self, service="openiot", service_path="/"):
        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        resource_path = DeviceBase.RESOURCE_PATH_CREATE

        query_params = {}

        try:
            self.header = {
                "device_id": f"{self.type}{self.id}",
                "entity_name": f"urn:ngsi-ld:{self.type}:{self.id}",
                "entity_type": self.type,
                "transport": "MQTT",
            }

            self.mapping = {
                "attributes": [
                    {
                        "object_id": attr,
                        "name": attr,
                        "type": self.attributes[attr]["type"]
                    }
                    for attr in self.attributes.keys()
                ]
            }

            self.static_attributes = {
                "static_attributes": [{
                    "name": "refStore",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:Store:003"}
                ]
            }

            self.device = {
                **self.header,
                **self.attributes,
                **self.mapping,
                **self.static_attributes
            }

            body_params = json.dumps({
                "devices": [
                    self.device
                ]
            })
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_device`")

        return self.api_client.call_api(
            method="POST",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )


class RobotDevice(DeviceBase):
    TYPE = DeviceType.ROBOT

    def __init__(self, id, api_client, ngsi_group):
        super(RobotDevice, self).__init__(id=id,
                                          type=ngsi_group.type,
                                          api_client=api_client)

        self.attributes = {
            "pose": {
                "type": "coordinates",
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "path": {
                "type": "list",
                "points": []
            },
            "target": {
                "type": "point",
                "x": 0.0,
                "y": 0.0
            },
            "targetProduct": {
                "type": "productID",
                "val": "Product-001"
            },
            "velocities": {
                "type": "vector2d",
                "linear": 0.0,
                "angular": 0.0
            },
            "state": {
                "type": "enum",
                "val": "IDLE"
            },
            "power": {
                "type": "float",
                "percentage": 1.0
            },
            "hearbeat": {
                "type": "boolean",
                "val": True,
            },
            "logs": {
                "type": "string",
                "msg": "I am a default log!"
            },
            "image": {
                "type": "string",
                "val": ""
            }
        }

        self._create(
            service=ngsi_group.service,
            service_path=ngsi_group.service_path
        )
