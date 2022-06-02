from fiware_ngsi_api.configuration import NgsiConfiguration

import datetime
import urllib3
import six

from six.moves.urllib.parse import urlencode


class NgsiApiClient:
    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types

    def __init__(self, configuration=None):
        if configuration is None:
            configuration = NgsiConfiguration()
        self._configuration = configuration

        self._http = urllib3.PoolManager()

    def _prepare_for_serialization(self, obj):
        if obj is None:
            return None
        elif isinstance(obj, NgsiApiClient.PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj, list):
            return list(self.sanitize_for_serialization(sub_obj)
                        for sub_obj in obj)
        elif isinstance(obj, tuple):
            return tuple(self.sanitize_for_serialization(sub_obj)
                         for sub_obj in obj)
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            obj_dict = dict
        else:
            obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                        for attr, _ in six.iteritems(obj.swagger_types)
                        if getattr(obj, attr) is not None}

        return {key: self.sanitize_for_serialization(val)
                for key, val in six.iteritems(obj_dict)}

    # Construct topic & attributes
    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, post_params=None,
                 body=None, async_req=None, _return_http_data_only=None, _preload_content=True, _request_timeout=None):

        # if header_params:
        #     header_params = self._prepare_for_serialization(header_params)

        # if path_params:
        #     path_params = self._prepare_for_serialization(path_params)

        # if query_params:
        #     query_params = self._prepare_for_serialization(query_params)

        # if body:
        #     body = self._prepare_for_serialization(body)

        url = self._configuration.host + resource_path

        respose_data = self.request(method,
                                    url,
                                    query_params,
                                    header_params,
                                    post_params,
                                    body,
                                    _preload_content,
                                    _request_timeout)

        return respose_data

    def request(self, method, url, query_params=None, header_params=None,
                post_params=None, body=None, _preload_content=True, _request_timeout=None):

        if method == "GET":
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        elif method == 'POST':
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        elif method == 'DELETE':
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        elif method == 'PUT':
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        elif method == 'PATCH':
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        elif method == 'POST':
            if query_params:
                url += "?" + urlencode(query_params)

            return self._http.request(method=method, url=url,
                                      headers=header_params,
                                      body=body)
        else:
            raise ValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )
