from fiware_ngsi_api.api_client import NgsiApiClient

import json


class NgsiGroups:
    RESOURCE_PATH = ":4041/iot/services"

    HTTP_INFO = [
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, api_client, type, api_key, service="openiot", service_path="/"):
        if api_client is None:
            api_client = NgsiApiClient()
        self._api_client = api_client

        self.type = type
        self.api_key = api_key
        self.service = service
        self.service_path = service_path

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, new_api_key):
        self._api_key = new_api_key

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, new_service):
        self._service = new_service

    @service.setter
    def service(self, new_service):
        self._service = new_service

    @property
    def service_path(self):
        return self._service_path

    @service_path.setter
    def service_path(self, new_service_path):
        self._service_path = new_service_path

    def create(self):
        header_params = {
            "Fiware-Service": self.service,
            "Fiware-ServicePath": self.service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        try:
            body_params = json.dumps({
                "services": [
                    {
                        "apikey": self.api_key,
                        "type": self.type,
                        "resource": "/iot/json",
                    }
                ]
            })
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_group`")

        resource_path = self.RESOURCE_PATH

        query_params = {}

        return self._api_client.call_api(
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

    def list(self, service=None, service_path=None):
        if service is None:
            service = self.service

        if service_path is None:
            service_path = self.service_path

        header_params = {
            "Content-Type": "text/plain",
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
        }

        body_params = ""

        resource_path = self.RESOURCE_PATH

        query_params = {}

        return self._api_client.call_api(
            method="GET",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def update(self, body):
        header_params = {
            "Content-Type": "application/json",
            "Fiware-Service": self.service,
            "Fiware-ServicePath": self.service_path,
        }

        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_group`")

        resource_path = self.RESOURCE_PATH

        query_params = {
            "resource": "/iot/json",
            "apikey": self.api_key
        }

        return self._api_client.call_api(
            method="PUT",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def delete(self):
        header_params = {
            "Fiware-Service": self.service,
            "Fiware-ServicePath": self.service_path,
        }

        body_params = None

        resource_path = self.RESOURCE_PATH

        query_params = {
            "resource": "/iot/json",
            "apikey": self.api_key
        }

        return self._api_client.call_api(
            method="DELETE",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )
