from ast import Global
from importlib.resources import path
from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient
from fiware_ngsi_api.models.robot_api import NgsiRobotAPI

from time import sleep
from commlib.transports.mqtt import ConnectionParameters, Credentials
from commlib.node import Node, TransportType


API_KEY = "1234abcd"
ENTITY_TYPE = "Robot"
ENTITY_ID = "100"

new_target = False
target = None
pose = None
robot_path = None


def get_target(msg):
    global pose, robot_path, new_target, target

    new_target = True
    target = msg

    print("New Target: ", msg)

    # calculate path
    robot_path = []

    a = 0
    if msg['x'] != pose['x']:
        a = (msg['y'] - pose['y']) / (msg['x'] - pose['x'])

    b = pose['y'] - a * pose['x']

    for i in range(11):
        x = pose['x'] + i * (msg['x'] - pose['x']) / 10
        robot_path.append([int(x), int(a * x + b)])

    print(robot_path)


def check_if_cancelled(msg):
    global new_target, target
    new_target = False
    target = None

    print("Goal Cancelled!")


if __name__ == "__main__":
    config = NgsiConfiguration("../../conf/settings.conf")
    client = NgsiApiClient(configuration=config)
    robot = NgsiRobotAPI(client, "../../data-models/robot.yaml")

    # Initialize robot pose
    robot.pose = {
        "x": 0,
        "y": 0,
        "th": 90
    }

    pose = robot.pose['pose']
    print(pose)

    # connect to broker
    cred = Credentials(
        username="porolog",
        password="fiware"
    )

    conn_params = ConnectionParameters(
        host="snf-889260.vm.okeanos.grnet.gr",
        port=1893,
        creds=cred
    )

    node = Node(node_name="eurakos",
                transport_type=TransportType.MQTT,
                connection_params=conn_params,
                debug=True)

    # Target Sub
    TARGET_TOPIC = f"/{API_KEY}/{ENTITY_TYPE}{ENTITY_ID}/attrs/target"
    sub_target = node.create_subscriber(topic=TARGET_TOPIC,
                                        on_message=get_target)

    sub_target.run()

    # Cancel Sub
    CANCEL_TOPIC = f"/{API_KEY}/{ENTITY_TYPE}{ENTITY_ID}/attrs"
    sub_cancel = node.create_subscriber(topic=CANCEL_TOPIC,
                                        on_message=check_if_cancelled)

    sub_cancel.run()

    # Path pub
    PATH_TOPIC = f"/{API_KEY}/{ENTITY_TYPE}{ENTITY_ID}/attrs/path"
    pub_path = node.create_publisher(topic=PATH_TOPIC)

    try:
        while True:
            if new_target:
                print("Publish new path!")
                pub_path.publish({
                    "points": robot_path
                })

                new_target = False

            sleep(1)
    except KeyboardInterrupt:
        pass
