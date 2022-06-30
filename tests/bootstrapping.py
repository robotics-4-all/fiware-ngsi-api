from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api.services import NgsiService
from fiware_ngsi_api.api.entities import NgsiEntities
from fiware_ngsi_api.models.robot_api import NgsiRobotAPI
from fiware_ngsi_api.api.devices import NgsiDevice

import os
import json
import time
import yaml

API_KEY = "1234abcd"

def cleanup_type(ngsi_type, ngsi, device_api, service_api):
    print("<<<-------------------------------->>>")
    print("Preparing " + ngsi_type + " type")
    res = ngsi.list_entities(type = ngsi_type)
    resp = json.loads(res.data)
    print("Number of entities: " + str(len(resp)))
    for i in resp:
        print("Deleting " + i['id'])
        ngsi.remove_entity(i['id'])
    time.sleep(2)

    response = device_api.list(type=ngsi_type)
    response_msg = json.loads(response.data)
    print("Devices found: " + str(len(response_msg['devices'])))
    for i in response_msg['devices']:
        device_api.delete(id = i['device_id'], type = ngsi_type)
        # TODO: DOES NOT DELETE THE DEVICES!!

    service_api.create(api_key=API_KEY, type=ngsi_type)


if __name__ == "__main__":
    config = NgsiConfiguration(file_path="../conf/settings.conf")
    api_client = NgsiApiClient(configuration=config)

    device_api = NgsiDevice(api_client=api_client)
    service_api = NgsiService(api_client=api_client)
    service_api.delete(api_key=API_KEY)
    ngsi = NgsiEntities(api_client)

    #---------------------- Warehouse handling --------------------------#
    cleanup_type("Warehouse", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Warehouse",
        "name": "Bleujour",
        "georeference": {
            "type": "vector",
            "value": {
                "longitude": 43.5746458,
                "lattitude": 1.4514467
            },
            "metadata": {
                "address": {
                    "type": "postalAddress",
                    "value": {
                        "streetAddress": "37 Av. Jules Julien",
                        "addressRegion": "Toulouse, France",
                        "addressLocality": "-",
                        "postalCode": "31400" 
                    }
                }
            }
        },
        'attributes': {
            "blueprint": {
                "type": "string",
                "value": ""
            },
            "dimensions": {
                "type": "vector",
                "value": {
                    "width": 120,
                    "height": 80,
                    "resolution": 0.2
                }
            },
            "annotations": {
                "type": "list",
                "value": [] 
            }
        }
    }

    print("Creating Warehouse...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- WarehouseKPI handling --------------------------#
    cleanup_type("WarehouseKPI", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "WarehouseKPI",
        'attributes': {
            "date": {
                "type": "Date",
                "val": "14/06/2022"
            },
            "palleteStorageDensity":{
                "type": "number",
                "val": 1
            },
            "distanceXmassMovedByRobots":{
                "type": "number",
                "val": 1
            },
            "distanceXmassMovedByOperators":{
                "type": "number",
                "val": 1
            },
            "palletsMoved":{
                "type": "number",
                "val": 1
            },
            "parcelsMoved":{
                "type": "number",
                "val": 1
            },
            "savedTimeshareForOperator":{
                "type": "number",
                "val": 1
            }
        },
        "refWarehouse": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Warehouse:1"
        }
    }

    print("Creating WarehouseKPI...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Robots handling --------------------------#
    cleanup_type("Robot", ngsi, device_api, service_api)
    time.sleep(1)

    # Load robot yaml
    robot_yaml = {}
    if os.path.exists("../data-models/bootstrapping/robot1.yaml"):
        with open("../data-models/bootstrapping/robot1.yaml", "r") as stream:
            try:
                robot_yaml = yaml.safe_load(stream)['Robot']
            except Exception as e:
                print(e)
    else:
        raise IOError("Invalid robot yaml path!")

    print("Creating Robot1...")
    robot_yaml['id'] = 1
    robot_yaml['name'] = "Robot" + str(robot_yaml['id'])
    robot_yaml['refWarehouse'] = {
        "type": "Relationship",
        "value": "urn:ngsi-ld:Warehouse:1"
    }
    robot1 = NgsiRobotAPI(api_client, robot_yaml)
    time.sleep(0.5)

    print("Creating Robot2...")
    robot_yaml['id'] = 2
    robot_yaml['name'] = "Robot" + str(robot_yaml['id'])
    robot_yaml['refWarehouse'] = {
        "type": "Relationship",
        "value": "urn:ngsi-ld:Warehouse:1"
    }
    robot1 = NgsiRobotAPI(api_client, robot_yaml)
    time.sleep(0.5)

    #---------------------- Robots KPIs handling --------------------------#
    cleanup_type("RobotKPI", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "RobotKPI",
        'attributes': {
            'date': {
                'type': 'Date',
                'val': ''
            },
            'boxedMoved': {
                'type': 'number',
                'val': 0
            },
            'palletesMoved': {
                'type': 'number',
                'val': 0
            },
            'distance': {
                'type': 'number',
                'val': 0
            }
        },
        "refRobot": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Robot:1"
        }
    }

    print("Creating RobotKPI1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    time.sleep(3)
 
    #---------------------- Room  handling --------------------------#
    cleanup_type("Room", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Room",
        'attributes': {
            "floor": {
                "type": "number",
                "value": 0
            },
            "blueprint": {
                "type": "string",
                "value": ""
            },
            "dimensions": {
                "type": "vector",
                "value": {
                    "width": 10, 
                    "height": 15.2, 
                    "z": 4.5, 
                    "resolution": 0.2 
                }
            },
            "annotations": {
                "type": "list",
                "value": [] 
            },
            "groundType": {
                "type": "string",
                "value": ""
            },
            "origin": {
                "type": "vector",
                "value": {
                    "x": 230, 
                    "y": 140 
                }
            }
        },
        "refWarehouse": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Warehouse:1"
        }
    }

    print("Creating Room1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Rack  handling --------------------------#
    cleanup_type("Rack", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Rack",
        'attributes': {
            "maxPayload": {
                "type": "number",
                "value": 300
            },
            "dimensions": {
                "type": "vector",
                "value": {
                    "length": 3, 
                    "width": 1.5, 
                    "height": 0.8, 
                    "orientation": 0
                }
            },
            "origin": {
                "type": "vector",
                "value": {
                    "x": 1.2, 
                    "y": 0.6 
                }
            }
        },
        "refRoom": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Room:1"
        }
    }

    print("Creating Rack1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Shelf  handling --------------------------#
    cleanup_type("Shelf", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Shelf",
        'attributes': {
            "altitude": {
                "type": "number",
                "value": 2.5
            },
            "surfaceNature": {
                "type": "string",
                "value": ""
            }
        },
        "refRack": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Rack:1"
        }
    }

    print("Creating Shelf1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Slot  handling --------------------------#
    cleanup_type("Slot", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Slot",
        'attributes': {
            "width": {
                "type": "number",
                "value": 2.5
            },
            "originx": {
                "type": "number",
                "value": 0.5
            }
        },
        "refShelf": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Shelf:1"
        }
    }

    print("Creating Slot1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Pallet  handling --------------------------#
    cleanup_type("Pallet", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Pallet",
        'attributes': {
            "dimensions": {
                "type": "vector",
                "value": {
                    "length": 0,
                    "width": 0,
                    "height": 0
                }
            },
            "barcode": {
                "type": "string",
                "value": {
                    "val": "xxx"
                }
            },
            "material": {
                "type": "string",
                "value": ""
            },
            "fragile": {
                "type": "bool",
                "value": false
            }
        },
        "refSlot": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Slot:1"
        }
    }

    print("Creating Pallet1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    #---------------------- Pallet  handling --------------------------#
    cleanup_type("Parcel", ngsi, device_api, service_api)
    time.sleep(1)

    entity_yaml = {
        "id": "-",
        "type": "Parcel",
        'attributes': {
            "dimensions": {
                "type": "vector",
                "value": {
                    "length": 0,
                    "width": 0,
                    "height": 0
                }
            },
            "sku": {
                "type": "string",
                "value": "xxx"
            },
            "manufacturer": {
                "type": "string",
                "value": ""
            },
            "manufDate": {
                "type": "Date",
                "value": ""
            },
            "content": {
                "type": "string",
                "value": ""
            },
            "mass": {
                "type": "number",
                "value": 0
            },
            "price": {
                "type": "number",
                "value": 0
            },
            "fragile": {
                "type": "bool",
                "value": false
            },
            "itemQuantity": {
                "type": "number",
                "value": 10
            }
        },
        "refPallet": {
            "type": "Relationship",
            "value": "urn:ngsi-ld:Pallet:1"
        }
    }

    print("Creating Parcel1...")
    entity_yaml["id"] = 1
    ngsi.create_entity(entity_yaml)
    time.sleep(0.5)

    # to end...
    time.sleep(5)


    