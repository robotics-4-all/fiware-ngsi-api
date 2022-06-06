import json
import six

from fiware_ngsi_api.api_client import NgsiApiClient

# from six.moves.urllib.parse import urlencode


class NgsiEntities:
    RESOUCE_PATH = ":1026/v2/entities"

    ALL_PARAMS = {
        "List": [
            'id',
            'type',
            'id_pattern',
            'type_pattern',
            'q',
            'mq',
            'georel',
            'geometry',
            'coords',
            'limit',
            'offset',
            'attrs',
            'metadata',
            'order_by',
            'options'
        ],
        "Create": [
            'body',
            'content_type',
            'options'
        ],
        "Remove": [
            'entity_id',
            'type'
        ],
        "Retrive": [
            'entity_id',
            'type',
            'attrs',
            'metadata',
            'options'
        ],
        "Replace": [
            'body',
            'content_type',
            'entity_id',
            'type',
            'options'
        ]
    }

    HTTP_INFO = [
        'fiware_service',
        'fiware_service_path',
        'async_req',
        '_return_http_data_only',
        '_preload_content',
        'request_timeout'
    ]

    def __init__(self, api_client):
        if api_client is None:
            api_client = NgsiApiClient()
        self._api_client = api_client

        for key in NgsiEntities.ALL_PARAMS:
            NgsiEntities.ALL_PARAMS[key].extend(NgsiEntities.HTTP_INFO)

    def create_entity(self, body, **kwargs):
        params = locals()
        input_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Create']:
                input_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method create_entitiy"
                )

        del params['kwargs']

        # parse path param
        resource_path = self.RESOUCE_PATH

        # parse query params
        query_params = {}
        if 'options' in input_params:
            query_params['options'] = input_params['options']

        # parse header params
        header_params = {}
        if 'content_type' not in input_params or input_params['content_type'] is None:
            header_params['Content-Type'] = "application/json"
        else:
            header_params['Content-Type'] = input_params['content_type']

        if 'fiware_service' in input_params:
            header_params['Fiware-Service'] = input_params['fiware_service']

        if 'fiware_service_path' in input_params:
            header_params['Fiware-ServicePath'] = input_params['fiware_service_path']

        # parse body param
        body_params = None
        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `create_entity`")

        return self._api_client.call_api(
            method="POST",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def list_entities(self, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['List']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method list_entities"
                )

        del params['kwargs']

        # parse path param
        resource_path = self.RESOUCE_PATH

        # parse header param
        header_params = {}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="GET",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def retrieve_entity(self, entity_id, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Retrive']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method list_entities"
                )

        del params['kwargs']

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `retrieve_entity`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}"

        # parse header param
        header_params = {}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="GET",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def remove_entity(self, entity_id, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Remove']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method remove_entitiy"
                )

        del params['kwargs']

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `remove_entity`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}"

        # parse header param
        header_params = {}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="DELETE",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def retrieve_entity_attributes(self, entity_id, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Retrieve']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method retrieve_entity_attributes"
                )

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `retrieve_entity_attributes`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}/attrs"

        # parse header param
        header_params = {}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="GET",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def replace_all_entity_attributes(self, entity_id, body, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Replace']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method replace_all_entity_attributes"
                )

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `replace_all_entity_attributes`")

        # parse body param
        body_params = None
        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `replace_all_entity_attributes`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}/attrs"

        # parse header param
        header_params = {"Content-Type": "application/json"}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="PUT",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def update_existing_entity_attributes(self, entity_id, body, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Replace']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method replace_all_entity_attributes"
                )

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `replace_all_entity_attributes`")

        # parse body param
        body_params = None
        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `replace_all_entity_attributes`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}/attrs"

        # parse header param
        header_params = {"Content-Type": "application/json"}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="PATCH",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )

    def update_or_append_entity_attributs(self, entity_id, body, **kwargs):
        params = locals()
        query_params = {}

        for key, val in six.iteritems(params['kwargs']):
            if key in NgsiEntities.ALL_PARAMS['Replace']:
                query_params[key] = val
            else:
                raise TypeError(
                    f"Got an unexpected keyword argument {key} to method replace_all_entity_attributes"
                )

        if entity_id is None:
            raise ValueError(
                "Missing the required parameter `entity_id` when calling `replace_all_entity_attributes`")

        # parse body param
        body_params = None
        try:
            body_params = json.dumps(body)
        except Exception as e:
            raise ValueError(
                "Parameter `body` is not a valid json when calling `replace_all_entity_attributes`")

        # parse path param
        resource_path = f"{self.RESOUCE_PATH}/{entity_id}/attrs"

        # parse header param
        header_params = {"Content-Type": "application/json"}

        if 'fiware_service' in query_params:
            header_params['Fiware-Service'] = query_params['fiware_service']

        if 'fiware_service_path' in query_params:
            header_params['Fiware-ServicePath'] = query_params['fiware_service_path']

        return self._api_client.call_api(
            method="POST",
            resource_path=resource_path,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content'),
            _request_timeout=params.get('_request_timeout')
        )
