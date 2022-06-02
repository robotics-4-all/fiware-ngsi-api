from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api.device_groups import NgsiGroups


if __name__ == "__main__":
    config = NgsiConfiguration("../conf/settings.conf")
    client = NgsiApiClient(configuration=config)

    nsgi_devices = NgsiGroups(api_client=client)

    api_key = "1234"
    sensor_type = "Battery"
    service = "openiot"
    service_path = "/"

    r = nsgi_devices.create(api_key=api_key,
                            sensor_type=sensor_type,
                            service=service,
                            service_path=service_path)

    print(r.data)

    body = {
        "entity_type": "new sensor",
        "static_attributes": {
            "mpampis": 1,
            "giorgos": 4
        }
    }

    r = nsgi_devices.update(api_key="1234",
                            body=body,
                            service=service,
                            service_path=service_path)

    print(r.data)

    r = nsgi_devices.list(service=service,
                          service_path=service_path)

    print(r.data)

    r = nsgi_devices.delete(api_key="1234",
                            service=service,
                            service_path=service_path)

    print(r.data)

    r = nsgi_devices.list(service=service,
                          service_path=service_path)

    print(r.data)
