from commlib.transports.mqtt import ConnectionParameters, MQTTProtocolType, Credentials
from commlib.node import Node, TransportType
from datetime import datetime
import time

MOSQUITTO_HOST = "155.207.33.189"
MOSQUITTO_PORT = 1893
MOSQUITTO_USERNAME = "porolog"
MOSQUITTO_PASSWORD = "fiware"

API_KEY = "1234"
ENTITY_TYPE = "RobotKPI"
ENTITY_ID = "001"


if __name__ == "__main__":
    creds = Credentials(
        username=MOSQUITTO_USERNAME,
        password=MOSQUITTO_PASSWORD
    )

    params = ConnectionParameters(
        host=MOSQUITTO_HOST,
        port=MOSQUITTO_PORT,
        creds=creds
    )

    node = Node(
        transport_type=TransportType.MQTT,
        connection_params=params,
        debug=True
    )

    BASE_TOPIC = f"/{API_KEY}/{ENTITY_TYPE}{ENTITY_ID}/attrs"

    # Publishers
    date_pub = node.create_publisher(topic=BASE_TOPIC + "/date")
    boxes_moved_pub = node.create_publisher(topic=BASE_TOPIC + "/boxesMoved")
    palletes_moved_pub = node.create_publisher(
        topic=BASE_TOPIC + "/palletesMoved")
    distance_pub = node.create_publisher(
        topic=BASE_TOPIC + "/distance")

    # ====================  Publish to Pose ====================
    date_pub.publish({
        "val": datetime.now().strftime("%d/%m/%y")
    })

    # ====================  Publish to Path ====================
    boxes_moved_pub.publish({
        "val": 856
    })

    # ====================  Publish to Target ====================
    palletes_moved_pub.publish({
        "val": 36
    })

    # ====================  Publish to TargetProduct ====================
    distance_pub.publish({
        "val": 3
    })

    time.sleep(1)
