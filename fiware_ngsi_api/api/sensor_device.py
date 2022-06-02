from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient
from enum import Enum

import json
import time


class DeviceType(str, Enum):
    BATTERY = 'Battery'


class DeviceCommand(object):
    def __init__(self, name):
        self.name = name
        self.type = "command"

    def to_json(self):
        return self.__dict__


class DeviceBase(object):
    RESOURCE_PATH_CREATE = ":4041/iot/devices"
    RESOURCE_PATH_COMMAND = ":4041/v2/op/update"

    HTTP_INFO = [
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, id, type, api_client):
        self.id = id
        self.type = type

        self.commands = []
        self.references = []

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

    def add_command(self, command):
        self.commands.append(command.to_json())

    def _create(self, service="openiot", service_path="/"):
        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        resource_path = DeviceBase.RESOURCE_PATH_CREATE

        query_params = {}

        # print(f"{self.type}{self.id}")
        # print(f"urn:ngsi-ld:{self.type}:{self.id}")
        # print(self.type)

        try:
            body_params = json.dumps({
                "devices": [
                    {
                        "device_id": f"{self.type}{self.id}",
                        "entity_name": f"urn:ngsi-ld:{self.type}:{self.id}",
                        "entity_type": self.type,
                        "transport": "MQTT",
                        "commands": self.commands,
                        "static_attributes": self.references
                    }
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

    def _command(self, command, data, service="openiot", service_path="/"):
        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

        resource_path = DeviceBase.RESOURCE_PATH_COMMAND

        query_params = {}

        try:
            body_params = json.dumps({
                "actionType": "update",
                "entities": [
                    {
                        "type": self.type,
                        "id": f"urn:ngsi-ld:{self.type}:{self.id}",
                        command: {
                            "type": "command",
                            "value": data
                        }
                    }
                ]
            })
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_device`")

        print(body_params)

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


class BatteryDevice(DeviceBase):
    TYPE = DeviceType.BATTERY

    def __init__(self, id, api_client):
        super(BatteryDevice, self).__init__(id=id,
                                            type=BatteryDevice.TYPE,
                                            api_client=api_client)

        self.add_command(DeviceCommand("UpdateVoltage"))

        r = self._create()
        print(r.data)

    def updateVoltage(self, voltage):
        r = self._command("UpdateVoltage", voltage)
        print(r.data)


if __name__ == "__main__":
    config = NgsiConfiguration("settings.conf")
    client = NgsiApiClient(configuration=config)

    bat_device = BatteryDevice("001", client)

    while True:
        bat_device.updateVoltage(voltage=5)
        time.sleep(0.2)
