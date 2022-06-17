from fiware_ngsi_api.api_client import NgsiApiClient

import json


class NgsiService:
    RESOURCE_PATH = ":4041/iot/services"

    HTTP_INFO = [
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, api_client):
        if api_client is None:
            api_client = NgsiApiClient()
        self._api_client = api_client

    def create(self, api_key, type, service="openiot", service_path="/"):
        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
            "Cache-Control": "no-cache",
            "Content-Type": "application/json"
        }

        try:
            body_params = json.dumps({
                "services": [
                    {
                        "apikey": api_key,
                        "type": type,
                        "resource": "/iot/json",
                    }
                ]
            })
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_group`")

        resource_path = self.RESOURCE_PATH

        return self._api_client.call_api(
            method="POST",
            resource_path=resource_path,
            header_params=header_params,
            body=body_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def list(self, service="openiot", service_path="/"):

        header_params = {
            "Content-Type": "text/plain",
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
        }

        resource_path = self.RESOURCE_PATH

        return self._api_client.call_api(
            method="GET",
            resource_path=resource_path,
            header_params=header_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )

    def update(self, api_key, body, service="openiot", service_path="/"):
        header_params = {
            "Content-Type": "application/json",
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
        }

        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_group`")

        resource_path = self.RESOURCE_PATH

        query_params = {
            "resource": "/iot/json",
            "apikey": api_key
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

    def delete(self, api_key, service="openiot", service_path="/"):
        header_params = {
            "Fiware-Service": service,
            "Fiware-ServicePath": service_path,
        }

        resource_path = self.RESOURCE_PATH

        query_params = {
            "resource": "/iot/json",
            "apikey": api_key
        }

        return self._api_client.call_api(
            method="DELETE",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            async_req=None,
            _return_http_data_only=None,
            _preload_content=None,
            _request_timeout=None
        )
