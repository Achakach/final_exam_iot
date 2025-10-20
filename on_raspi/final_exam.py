# final_exam_receiver.py
from RPLCD.i2c import CharLCD
import json
import time
import paho.mqtt.client as mqtt

MQTT_BROKER = "mqtt-dashboard.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = "66070244/final"

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A02', auto_linebreaks=True)

def show_text(line1, line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2[:16])

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected rc={rc}")
    client.subscribe(MQTT_TOPIC)
    show_text("MQTT connected", "subscribed")

def on_message(client, userdata, message):
    s = message.payload.decode('utf-8', errors='ignore').strip()
    print(f"[MQTT] {message.topic} -> {s}")

    # ถ้าเป็น JSON {"temp":..,"humid":..} ก็แสดงสวย ๆ
    try:
        d = json.loads(s)
        t, h = d.get("temp"), d.get("humid")
        if isinstance(t, (int, float)) and isinstance(h, (int, float)):
            show_text(f"Temp:{t:.1f}C", f"Hum:{h:.1f}%")
            return
    except json.JSONDecodeError:
        pass

    # ไม่ใช่ JSON ก็แสดงตรง ๆ
    show_text(s[:16], s[16:32])

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected rc={rc}")
    show_text("MQTT lost", "reconn...")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    lcd.close(clear=True)
    client.disconnect()
