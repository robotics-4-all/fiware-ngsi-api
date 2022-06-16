from curses.panel import top_panel
from commlib.transports.mqtt import ConnectionParameters, MQTTProtocolType, Credentials
from commlib.node import Node, TransportType
import time

MOSQUITTO_HOST = "155.207.33.189"
MOSQUITTO_PORT = 1893
MOSQUITTO_USERNAME = "porolog"
MOSQUITTO_PASSWORD = "fiware"

API_KEY = "1234"
ENTITY_TYPE = "Robot"
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

    # ===================== Publishers =====================
    pose_pub = node.create_publisher(topic=BASE_TOPIC + "/pose")
    path_pub = node.create_publisher(topic=BASE_TOPIC + "/path")
    target_pub = node.create_publisher(topic=BASE_TOPIC + "/target")
    target_product_pub = node.create_publisher(
        topic=BASE_TOPIC + "/targetProduct")
    velocities_pub = node.create_publisher(
        topic=BASE_TOPIC + "/velocities")
    state_pub = node.create_publisher(topic=BASE_TOPIC + "/state")
    power_pub = node.create_publisher(topic=BASE_TOPIC + "/power")
    heartbeat_pub = node.create_publisher(topic=BASE_TOPIC + "/heartbeat")
    logs_pub = node.create_publisher(topic=BASE_TOPIC + "/logs")
    image_pub = node.create_publisher(topic=BASE_TOPIC + "/image")

    teleop_pub = node.create_publisher(topic=BASE_TOPIC + "/teleop/commands")

    # ================== Callback functions =================
    def target_cb(msg):
        print(f"Received new Robot TARGET: {msg}")

    def state_cb(msg):
        print(f"Received new Robot STATE: {msg}")

    def teleop_comm_cb(msg):
        print(f"Received new Robot TELEOP: {msg}")

    # ===================== Subscribers =====================
    target_sub = node.create_subscriber(
        topic=BASE_TOPIC + "/target",
        on_message=target_cb
    )
    target_sub.run()

    state_sub = node.create_subscriber(
        topic=BASE_TOPIC + "/state",
        on_message=state_cb
    )
    state_sub.run()

    teleop_comm_sub = node.create_subscriber(
        topic=BASE_TOPIC + "/teleop/commands",
        on_message=teleop_comm_cb
    )
    teleop_comm_sub.run()

    # ====================  Publish to Pose ====================
    pose_pub.publish({
        "x": 1.0,
        "y": 2.0,
        "th": 90
    })

    # ====================  Publish to Path ====================
    path_pub.publish({
        "points": [[x, x] for x in range(10)]
    })

    # ====================  Publish to Target ====================
    target_pub.publish({
        "x": 10.0,
        "y": 10.0
    })

    # ====================  Publish to TargetProduct ====================
    target_product_pub.publish({
        "val": "Product-X"
    })

    # ====================  Publish to Velocities ====================
    velocities_pub.publish({
        "linear": 5.35,
        "angular": 0.0
    })

    # ====================  Publish to State ====================
    state_pub.publish({
        "val": "Moving"
    })

    # ====================  Publish to Power ====================
    power_pub.publish({
        "percentage": 0.89
    })

    # ====================  Publish to Heartbeat ====================
    heartbeat_pub.publish({
        "val": True
    })

    # ====================  Publish to Logs ====================
    logs_pub.publish({
        "val": "Everything works perfectly!"
    })

    # ====================  Publish to Image ====================
    image_pub.publish({
        "val": "This is an image base64 - encoded string!"
    })

    time.sleep(1)

    teleop_commands = ["Stop", "Lift", "Release",
                       "Forward", "Backwards", "Left", "Right"]
    try:
        for command in teleop_commands:
            print(f"Publishing teleop command: {command}")

            teleop_pub.publish({
                "command": command
            })

            time.sleep(0.2)
    except KeyboardInterrupt as e:
        print("Bey!")
