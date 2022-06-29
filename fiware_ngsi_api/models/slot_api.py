from urllib import response
from fiware_ngsi_api.api.entities import NgsiEntities

import json
import yaml
import os


class NgsiSlotAPIError(Exception):
    def __init__(self, id, message="Error initializing slot entity"):
        self.id = id
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f'{self.id} -> {self.message}'


class NgsiSlotAPI(NgsiEntities):
    ENTITY_TYPE = 'Slot'

    def __init__(self, api_client, file_path, service="openiot", service_path="/"):
        self.api_client = api_client
        self.service = service
        self.service_path = service_path
        self.file_path = file_path

        self.type = NgsiSlotAPI.ENTITY_TYPE

        super(NgsiSlotAPI, self).__init__(api_client)

        self._load_settings()

        if not self._entity_exists():
            try:
                response = self.create_entity(
                    body=self._slot,
                    fiware_service=self._service,
                    fiware_service_path=self._service_path
                )

                if response.status != 201:
                    raise Exception(
                        f"Error creating slot entity {self._slot['id']}: {response.data}")
            except Exception as e:
                raise NgsiSlotAPIError(
                    id=self.slot_id,
                    message=e)

    @property
    def slot_id(self):
        return self._slot_id

    @slot_id.setter
    def slot_id(self, new_slot_id):
        self._slot_id = new_slot_id
        self._slot["id"] = f"urn:ngsi-ld:{self.type}:{self._slot_id}"

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, new_service):
        self._service = new_service

    @property
    def service_path(self):
        return self._service_path

    @service_path.setter
    def service_path(self, new_service_path):
        self._service_path = new_service_path

    @property
    def width(self):
        return self._get_slot_attr("width")

    @width.setter
    def width(self, new_width):
        response = self._set_slot_attr({
            "width": {
                "type": "boolean",
                "value": new_width
            }
        })

        if response:
            self._slot["width"]["value"] = new_width

    @property
    def originx(self):
        return self._get_slot_attr("originx")

    @originx.setter
    def originx(self, new_originx):
        response = self._set_slot_attr({
            "originx": {
                "type": "boolean",
                "value": new_originx
            }
        })

        if response:
            self._slot["originx"]["value"] = new_originx

    def _get_slot_attr(self, attr):
        try:
            response = self.retrieve_entity_attributes(
                entity_id=f"urn:ngsi-ld:{self.type}:{self.slot_id}",
                type=self.type,
                attrs=attr,
                options="keyValues"
            )

            if response.status == 200:
                return json.loads(response.data)
        except Exception as e:
            print(f"Error occured when trying to get attr: {attr}")

        return {}

    def _set_slot_attr(self, value):
        try:
            response = self.update_existing_entity_attributes(
                entity_id=f"urn:ngsi-ld:{self.type}:{self.slot_id}",
                type=self.type,
                body=value
            )

            if response.status == 204:
                print("Succesfull!")
                return True
        except Exception as e:
            print(f"Error occured when trying to get attr: {value.keys()}")
            return False

    def _load_settings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as stream:
                try:
                    self._slot = yaml.safe_load(stream)['Slot']
                    self._slot_id = self._slot["id"]
                    self._slot["id"] = f"urn:ngsi-ld:{self.type}:{self._slot_id}"
                    self._slot["type"] = self.type
                except yaml.YAMLError as e:
                    NgsiSlotAPIError(
                        id=self.slot_id,
                        error="Caught error when parsing yaml file!")
                except KeyError as e:
                    NgsiSlotAPIError(
                        id=self.slot_id,
                        error="Caught Key value error!")
        else:
            raise IOError("Invalid settings path!")

    def _entity_exists(self):
        try:
            response = self.retrieve_entity(
                entity_id=f"urn:ngsi-ld:{self.type}:{self.slot_id}",
                fiware_service=self._service,
                fiware_service_path=self._service_path
            )

            if response.status != 200:
                return False

            return True
        except Exception as e:
            print(f"Error occured when searching {self.type} entity: {e}.")
            return False

    def list_all(self):
        try:
            response = self.list_entities(
                type=self.type,
                fiware_service=self._service,
                fiware_service_path=self._service_path
            )

            if response.status != 200:
                return {"error": response.status}

            return json.loads(response.data)
        except Exception as e:
            print(f"Error occured when searching {self.type} entity: {e}.")
            return {"error": e}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("called")
        slot_to_save = {
            "Slot": self._slot
        }

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w") as outstream:
                    yaml.dump(slot_to_save, outstream,
                              default_flow_style=False)
            except yaml.YAMLError as e:
                NgsiSlotAPIError(
                    id=self.slot_id,
                    error="Caught error when parsing yaml file!")
            except KeyError as e:
                NgsiSlotAPIError(
                    id=self.slot_id,
                    error="Caught Key value error!")
        else:
            raise IOError("Invalid settings path!")
