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