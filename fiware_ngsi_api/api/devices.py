from fiware_ngsi_api.api_client import NgsiApiClient

import json


class NgsiDevice(object):
    RESOURCE_PATH = ":4041/iot/devices"

    HTTP_INFO = [
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, api_client):
        if api_client is None:
            api_client = NgsiApiClient()
        self.api_client = api_client

    @property
    def api_client(self):
        return self._api_client

    @api_client.setter
    def api_client(self, new_api_client):
        self._api_client = new_api_client

    def create(self, id, type, attrs, service="openiot", service_path="/"):
        resource_path = NgsiDevice.RESOURCE_PATH

        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        try:
            header = {
                "device_id": f"{type}{id}",
                "entity_name": f"urn:ngsi-ld:{type}:{id}",
                "entity_type": type,
                "transport": "MQTT",
            }

            if attrs is not None:
                mapping = {
                    "attributes": [
                        {
                            "object_id": attr,
                            "name": attr,
                            "type": attrs[attr]["type"]
                        }
                        for attr in attrs.keys()
                    ]
                }

            self.device = {
                **header,
                **attrs,
                **mapping
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
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def list(self, id=None, type=None, service="openiot", service_path="/"):
        resource_path = NgsiDevice.RESOURCE_PATH
        if id is not None and type is not None:
            resource_path = f"{NgsiDevice.RESOURCE_PATH}/{type}{id}"

        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path
        }

        return self.api_client.call_api(
            method="GET",
            resource_path=resource_path,
            header_params=header_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def update(self, id, type, new_attrs, service="openiot", service_path="/"):
        resource_path = f"{NgsiDevice.RESOURCE_PATH}/{type}{id}"

        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        try:
            body_params = json.dumps(new_attrs)
        except Exception as e:
            pass

        return self.api_client.call_api(
            method="PUT",
            resource_path=resource_path,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def delete(self, id, type, service="openiot", service_path="/"):
        resource_path = f"{NgsiDevice.RESOURCE_PATH}/{type}{id}"

        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path
        }

        return self.api_client.call_api(
            method="GET",
            resource_path=resource_path,
            header_params=header_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

        # class RobotDevice(NgsiDevice):
        #     def __init__(self, id, api_client, ngsi_group):
        #         super(RobotDevice, self).__init__(id=id,
        #                                           type=ngsi_group.type,
        #                                           api_client=api_client)

        #         self.attributes = {
        #             "pose": {
        #                 "type": "pose",
        #                 "x": 0.0,
        #                 "y": 0.0,
        #                 "z": 0.0
        #             },
        #             "path": {
        #                 "type": "list",
        #                 "points": []
        #             },
        #             "target": {
        #                 "type": "point",
        #                 "x": 0.0,
        #                 "y": 0.0
        #             },
        #             "targetProduct": {
        #                 "type": "productID",
        #                 "val": "Product-001"
        #             },
        #             "velocities": {
        #                 "type": "vector2d",
        #                 "linear": 0.0,
        #                 "angular": 0.0
        #             },
        #             "state": {
        #                 "type": "enum",
        #                 "val": "IDLE"
        #             },
        #             "power": {
        #                 "type": "float",
        #                 "percentage": 1.0
        #             },
        #             "heartbeat": {
        #                 "type": "bool",
        #                 "val": True,
        #             },
        #             "logs": {
        #                 "type": "string",
        #                 "val": "I am a default log!"
        #             },
        #             "image": {
        #                 "type": "string",
        #                 "val": ""
        #             }
        #         }

        #         self._create(
        #             service=ngsi_group.service,
        #             service_path=ngsi_group.service_path
        #         )

        # class RobotKPIDevice(DeviceBase):
        #     TYPE = DeviceType.ROBOT

        #     def __init__(self, id, api_client, ngsi_group):
        #         super(RobotKPIDevice, self).__init__(id=id,
        #                                              type=ngsi_group.type,
        #                                              api_client=api_client)

        #         self.attributes = {
        #             "date": {
        #                 "type": "Date",
        #                 "val": "14/06/2022"
        #             },
        #             "boxesMoved": {
        #                 "type": "number",
        #                 "val": 1
        #             },
        #             "palletesMoved": {
        #                 "type": "number",
        #                 "val": 1
        #             },
        #             "distance": {
        #                 "type": "number",
        #                 "val": 0.0
        #             }
        #         }

        #         self._create(
        #             service=ngsi_group.service,
        #             service_path=ngsi_group.service_path
        #         )
