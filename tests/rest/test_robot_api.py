from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient

from fiware_ngsi_api.models.robot_api import NgsiRobotAPI

if __name__ == "__main__":
    API_KEY = "1234abcd"
    SENSOR_TYPE = "Robot"
    ROBOT_ID = 1

    if __name__ == "__main__":
        config = NgsiConfiguration("../../conf/settings.conf")
        client = NgsiApiClient(configuration=config)

        robot = NgsiRobotAPI(client, ROBOT_ID, "../../data-models/robot.yaml")

        # ============ Pose ============
        robot.pose = {
            "x": 0,
            "y": 0,
            "th": 0
        }

        print(robot.pose)

        # ============ Path ============
        robot.path = {
            "points": []
        }

        print(robot.path)

        # ============ Target ============
        robot.target = {
            "x": 0,
            "y": 0
        }

        print(robot.target)

        # ============ TargetProduct ============
        robot.target_product = {
            "val": "Product-123"
        }

        print(robot.target_product)

        # ============ velocities ============
        robot.velocities = {
            "linear": 0,
            "angular": 0
        }

        print(robot.velocities)

        # ============ State ============
        robot.state = {
            "val": "IDLE"
        }

        print(robot.state)

        # ============ Heartbeat ============
        robot.heartbeat = {
            "val": False
        }

        print(robot.heartbeat)

        # ============ power ============
        robot.power = {
            "percentage": 0.0
        }

        print(robot.power)

        # ============ Logs ============
        robot.logs = {
            "val": ""
        }

        print(robot.logs)

        # ============ Image ============
        robot.image = {
            "val": ""
        }

        print(robot.image)
