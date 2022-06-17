from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient

from fiware_ngsi_api.models.robot_api import NgsiRobotAPI

if __name__ == "__main__":
    API_KEY = "1234"
    SENSOR_TYPE = "Robot"
    ROBOT_ID = "001"

    if __name__ == "__main__":
        config = NgsiConfiguration("../../conf/settings.conf")
        client = NgsiApiClient(configuration=config)

        robot = NgsiRobotAPI(client, "../../data-models/robot.yaml")

        # ============ Pose ============
        robot.pose = {
            "x": 1,
            "y": 2,
            "th": 98
        }

        print(robot.pose)

        # ============ Path ============
        robot.path = {
            "points": [[i, i] for i in range(10)]
        }

        print(robot.path)

        # ============ Target ============
        robot.target = {
            "x": 1,
            "y": 2
        }

        print(robot.target)

        # ============ TargetProduct ============
        robot.target_product = {
            "val": "Product-123"
        }

        print(robot.target_product)

        # ============ velocities ============
        robot.velocities = {
            "linear": 100,
            "angular": -100
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
            "percentage": 0.8
        }

        print(robot.power)

        # ============ Logs ============
        robot.logs = {
            "val": "I am a new log!"
        }

        print(robot.logs)

        # ============ Image ============
        robot.image = {
            "val": "I am a new base64 image!"
        }

        print(robot.image)
