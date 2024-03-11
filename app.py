import threading
from flask import Flask, render_template
from data.db import DBManager
import paho.mqtt.client as mqtt_client

app = Flask(__name__)

mqtt_user = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
mqtt_user.loop_start()
mqtt_user.connect("localhost", 1883, 60)


@mqtt_user.connect_callback()
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.subscribe("topic/test")


@mqtt_user.message_callback()
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


"""def main():
    db = DBManager()
    print("1")
    # mqtt_thread = threading.Thread(target=mqtt_oper.on_connect, args=("localhost", 1883, 60))
    print("2")
    db.insert_values("air_quality", pollution_level=432545)
    temp_data = db.get_values("air_quality", "id", "ambient_temp")
    tmp = [print(item['ambient_temp']) for item in temp_data]
    # TODO: remove the print statement -> tmp = [print(item['pollution_level']) for item in temp_data]
    db.update_values("air_quality", "pollution_level = 432545", id=10, ambient_temp=30.5)
    db.delete_values("air_quality", "pollution_level = 128")"""


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

app_thread = threading.Thread(target=app.run)
mqtt_thread = threading.Thread(target=mqtt_user.connect, args=("localhost", 1883, 60))
app_thread.start()
mqtt_thread.start()
