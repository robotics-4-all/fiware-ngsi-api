from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api.entities import NgsiEntities

import json


if __name__ == "__main__":
    config = NgsiConfiguration("../conf/settings.conf")
    client = NgsiApiClient(configuration=config)

    nsgi_entities = NgsiEntities(api_client=client)

    body = {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "address": {
            "type": "PostalAddress",
                "value": {
                    "streetAddress": "Bornholmer Straße 65",
                    "addressRegion": "Berlin",
                    "addressLocality": "Prenzlauer Berg",
                    "postalCode": "10439"
                },
            "metadata": {
                    "verified": {
                        "value": True,
                        "type": "Boolean"
                    }
                }
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [13.3986, 52.5547]
            }
        },
        "name": {
            "type": "Text",
            "value": "Bösebrücke Einkauf"
        }
    }

    # Create Entity
    response = nsgi_entities.create_entity(body)
    print("Creating an entity! \n", response.data.decode('utf-8'), response.status)

    # List all entities
    response = nsgi_entities.list_entities(
        options="keyValues", type="Store", q="address.addressLocality==Prenzlauer Berg")

    result = json.loads(response.data)
    print("Listing all current entities! \n", result)

    # Replace all entities attributes
    new_attr = {
        "address": {
            "type": "PostalAddress",
            "value": {
                    "streetAddress": "Nikou Akritidi 13",
                    "addressRegion": "Thessaloniki",
                    "addressLocality": "Kentro",
                    "postalCode": "54635"
            },
            "metadata": {
                "verified": {
                    "value": True,
                    "type": "Boolean"
                }
            }
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [15, 16]
            }
        },
        "name": {
            "type": "Text",
            "value": "Giorgos"
        }
    }

    response = nsgi_entities.replace_all_entity_attributes(
        entity_id="urn:ngsi-ld:Store:001", body=new_attr
    )

    print("Replace entities attributes! \n", response.data, response.status)

    # List entity
    response = nsgi_entities.retrieve_entity(
        entity_id="urn:ngsi-ld:Store:001", options="keyValues")

    result = json.loads(response.data)
    print("List specific entity! \n", result)

    # Add attribute to entity
    extra_attribute = {
        "temperature": {
            "type": "Number",
            "value": 27.5
        }
    }

    response = nsgi_entities.update_or_append_entity_attributs(
        entity_id="urn:ngsi-ld:Store:001", body=extra_attribute, options="append"
    )

    print("Append an attribute to an entity\n", response.data, response.status)

    # Update existing entity attribute
    updated_attribute = {
        "temperature": {
            "type": "Number",
            "value": 30.0
        }
    }

    response = nsgi_entities.update_existing_entity_attributes(
        entity_id="urn:ngsi-ld:Store:001", body=updated_attribute
    )

    print("Update an existing attribute of that entity!\n",
          response.data, response.status)

    # List entity's attribute
    response = nsgi_entities.retrieve_entity_attributes(
        entity_id="urn:ngsi-ld:Store:001")

    result = json.loads(response.data)
    print("List attributes of the specified enitity\n", result)

    # Remove Entity
    response = nsgi_entities.remove_entity(entity_id="urn:ngsi-ld:Store:001")
    print("Removing an existing entity!\n",
          response.data.decode('utf-8'), response.status)
