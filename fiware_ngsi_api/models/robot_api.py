from fiware_ngsi_api.api.entities import NgsiEntities
from fiware_ngsi_api.api.services import NgsiService
from fiware_ngsi_api.api.devices import NgsiDevice

import json
import yaml
import os


class NgsiRobotAPIError(Exception):
    def __init__(self, id, message="Error initializing robot entity"):
        self.id = id
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f'{self.id} -> {self.message}'


class NgsiRobotAPI(NgsiEntities):
    ENTITY_TYPE = 'Robot'

    def __init__(self, api_client, robot_id, file_path, service="openiot", service_path="/"):
        self.api_client = api_client
        self.service = service
        self.service_path = service_path
        self.file_path = file_path
        self.robot_id = robot_id

        self._robot = None

        self.type = NgsiRobotAPI.ENTITY_TYPE

        super(NgsiRobotAPI, self).__init__(api_client)

        if isinstance(file_path, str):
            self._load_settings()
        else:
            self._robot = file_path
            self.file_path = None

        self._service_api = NgsiService(api_client)
        self._device_api = NgsiDevice(api_client)

        if not self._service_exists():
            raise NgsiRobotAPIError(
                id=self.robot_id,
                message="Error: Robot type service is not found!")

        if not self._device_exists():
            try:
                response = self._device_api.create(
                    id=robot_id,
                    type=NgsiRobotAPI.ENTITY_TYPE,
                    attrs=self._robot['attributes'],
                    s_attrs=self._robot['static_attributes']
                )

                if response.status != 201:
                    raise Exception(
                        f"Error creating robot entity {robot_id}: {response.data}")

                # response = self.replace_all_entity_attributes(
                #     entity_id=f"urn:ngsi-ld:{self.type}:{self.robot_id}",
                #     body=self._robot['attributes']
                # )

                # if response.status != 204:
                #     raise Exception(
                #         f"Error initializing robot entity {robot_id}: {response.data}")
            except Exception as e:
                raise NgsiRobotAPIError(
                    id=self.robot_id,
                    message=e)

    @property
    def robot_id(self):
        return self._robot_id

    @robot_id.setter
    def robot_id(self, new_robot_id):
        self._robot_id = new_robot_id

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, new_apikey):
        self._apikey = new_apikey

    @property
    def api_client(self):
        return self._api_client

    @api_client.setter
    def api_client(self, new_api_client):
        self._api_client = new_api_client

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
    def robotClass(self):
        return self._get_robot_attr("robotClass")

    @robotClass.setter
    def robotClass(self, new_robot_class):
        response = self._set_robot_attr({
            "robotClass": {
                "type": "string",
                "value": new_robot_class
            }
        })

        if response:
            self._robot["attributes"]["robotClass"]["value"] = new_robot_class

    @property
    def pose(self):
        return self._get_robot_attr("pose")

    @pose.setter
    def pose(self, new_pose):
        response = self._set_robot_attr({
            "pose": {
                "type": "pose",
                "value": new_pose
            }
        })

        if response:
            self._robot["attributes"]["pose"]["value"] = new_pose

    @property
    def origin(self):
        return self._get_robot_attr("origin")

    @origin.setter
    def origin(self, new_origin):
        response = self._set_robot_attr({
            "origin": {
                "type": "origin",
                "value": new_origin
            }
        })

        if response:
            self._robot["attributes"]["origin"]["value"] = new_origin

    @property
    def target(self):
        return self._get_robot_attr("target")

    @target.setter
    def target(self, new_target):
        response = self._set_robot_attr({
            "target": {
                "type": "point",
                "value": new_target
            }
        })

        if response:
            self._robot["attributes"]["target"]["value"] = new_target

    @property
    def target_product(self):
        return self._get_robot_attr("targetProduct")

    @target_product.setter
    def target_product(self, new_target_product):
        response = self._set_robot_attr({
            "targetProduct": {
                "type": "productID",
                "value": new_target_product
            }
        })

        if response:
            self._robot["attributes"]["targetProduct"]["value"] = new_target_product

    @property
    def velocities(self):
        return self._get_robot_attr("velocities")

    @velocities.setter
    def velocities(self, new_velocities):
        response = self._set_robot_attr({
            "velocities": {
                "type": "vector2d",
                "value": new_velocities
            }
        })

        if response:
            self._robot["attributes"]["targetProduct"]["value"] = new_velocities

    @property
    def path(self):
        return self._get_robot_attr("path")

    @path.setter
    def path(self, new_path):
        response = self._set_robot_attr({
            "path": {
                "type": "list",
                "value": new_path
            }
        })

        if response:
            self._robot["attributes"]["path"]["value"] = new_path

    @property
    def state(self):
        return self._get_robot_attr("state")

    @state.setter
    def state(self, new_state):
        response = self._set_robot_attr({
            "state": {
                "type": "enum",
                "value": new_state
            }
        })

        if response:
            self._robot["attributes"]["state"]["value"] = new_state

    @property
    def power(self):
        return self._get_robot_attr("power")

    @power.setter
    def power(self, new_power):
        response = self._set_robot_attr({
            "power": {
                "type": "float",
                "value": new_power
            }
        })

        if response:
            self._robot["attributes"]["power"]["value"] = new_power

    @property
    def heartbeat(self):
        return self._get_robot_attr("heartbeat")

    @heartbeat.setter
    def heartbeat(self, new_heartbeat):
        response = self._set_robot_attr({
            "heartbeat": {
                "type": "boolean",
                "value": new_heartbeat
            }
        })

        if response:
            self._robot["attributes"]["heartbeat"]["value"] = new_heartbeat

    @property
    def logs(self):
        return self._get_robot_attr("logs")

    @logs.setter
    def logs(self, new_logs):
        response = self._set_robot_attr({
            "logs": {
                "type": "string",
                "value": new_logs
            }
        })

        if response:
            self._robot["attributes"]["logs"]["value"] = new_logs

    @property
    def image(self):
        return self._get_robot_attr("image")

    @image.setter
    def image(self, new_image):
        response = self._set_robot_attr({
            "image": {
                "type": "string",
                "value": new_image
            }
        })

        if response:
            self._robot["attributes"]["image"]["value"] = new_image

    def _get_robot_attr(self, attr):
        try:
            response = self.retrieve_entity_attributes(
                entity_id=f"urn:ngsi-ld:{self.type}:{self.robot_id}",
                type=self.type,
                attrs=attr,
                options="keyValues"
            )

            if response.status == 200:
                return json.loads(response.data)
        except Exception as e:
            print(f"Error occured when trying to get attr: {attr}")

        return {}

    def _set_robot_attr(self, value):
        try:
            response = self.update_existing_entity_attributes(
                entity_id=f"urn:ngsi-ld:{self.type}:{self.robot_id}",
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
                    self._robot = yaml.safe_load(stream)['Robot']
                    print(self._robot)
                except yaml.YAMLError as e:
                    NgsiRobotAPIError(
                        id=self.robot_id,
                        error="Caught error when parsing yaml file!")
                except KeyError as e:
                    NgsiRobotAPIError(
                        id=self.robot_id,
                        error="Caught Key value error!")
        else:
            raise IOError("Invalid settings path!")

    def _service_exists(self):
        try:
            response = self._service_api.list(
                service=self._service,
                service_path=self._service_path
            )

            if response.status != 200:
                return False

            response = json.loads(response.data)

            for service in response['services']:
                if service['entity_type'] == self.type:
                    self.apikey = service['apikey']
                    return True
        except Exception as e:
            print(f"Error occured when searching {self.type} service: {e}.")
            return False

    def _device_exists(self):
        try:
            response = self._device_api.list(
                id=self.robot_id,
                type=self.type,
                service=self._service,
                service_path=self._service_path
            )

            if response.status != 200:
                return False

            return True
        except Exception as e:
            print(f"Error occured when searching {self.type} device: {e}.")
            return False

    def __del__(self):
        robot_to_save = {
            "Robot": self._robot
        }

        if self.file_path is not None:
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "w") as outstream:
                        yaml.dump(robot_to_save, outstream,
                                  default_flow_style=False)
                except yaml.YAMLError as e:
                    NgsiRobotAPIError(
                        id=self.robot_id,
                        error="Caught error when parsing yaml file!")
                except KeyError as e:
                    NgsiRobotAPIError(
                        id=self.robot_id,
                        error="Caught Key value error!")
            else:
                raise IOError("Invalid settings path!")

    # to add logger
    # to add setting group of attributes
