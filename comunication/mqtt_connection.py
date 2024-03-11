import paho.mqtt.client as mqtt_user
import time


def on_connect(cclient, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code= ", reason_code)


def on_disconnect(client, userdata, flags, reason_code, properties):
    print("disconnecting reason= ", reason_code)


mqtt_broker = "127.0.0.1"
mqtt_client = mqtt_user.Client(mqtt_user.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect

print("Connecting to broker", mqtt_broker)
mqtt_client.connect(mqtt_broker)
mqtt_client.loop_start()
mqtt_client.subscribe("topic/DEVICE")
mqtt_client.publish("topic/DEVICE", "message")
# mqtt_user.MQTTMessageInfo.wait_for_publish(mqtt_client.publish("topic/test", "Hello World message"))
time.sleep(5)
mqtt_client.loop_stop()
mqtt_client.disconnect()
