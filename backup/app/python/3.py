import tkinter as tk
import paho.mqtt.client as mqtt

# Konfigurasi MQTT
mqtt_server = "broker.mqttdashboard.com"
topic_tong_sampah_1 = "tong_sampah_1/status"
topic_tong_sampah_2 = "tong_sampah_2/status"

# Fungsi untuk update label status
def update_status(status, topic):
    if topic == topic_tong_sampah_1:
        label_tong_sampah_1.config(text=f"Status Tong Sampah 1: {status}")
    elif topic == topic_tong_sampah_2:
        label_tong_sampah_2.config(text=f"Status Tong Sampah 2: {status}")
    
    # Pemberian notifikasi
    if status == "Sudah Penuh":
        status_label.config(text=f"ALERT: {topic} is FULL!", fg="red")
    elif status == "Kosong":
        status_label.config(text=f"{topic} is EMPTY. (Empty)", fg="green")
    elif status == "Hampir Penuh":
        status_label.config(text=f"{topic} is NEAR FULL. (Near Full)", fg="yellow")

# Callback ketika terhubung ke broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic_tong_sampah_1)
    client.subscribe(topic_tong_sampah_2)

# Callback ketika menerima pesan
def on_message(client, userdata, msg):
    status = msg.payload.decode()
    update_status(status, msg.topic)

# Setup client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect ke broker MQTT
client.connect(mqtt_server, 1883, 60)

# Setup GUI
root = tk.Tk()
root.title("Monitoring Tong Sampah")

# Label untuk status
label_tong_sampah_1 = tk.Label(root, text="Status Tong Sampah 1: Waiting...", font=("Arial", 14))
label_tong_sampah_1.pack(pady=10)

label_tong_sampah_2 = tk.Label(root, text="Status Tong Sampah 2: Waiting...", font=("Arial", 14))
label_tong_sampah_2.pack(pady=10)

# Label untuk notifikasi
status_label = tk.Label(root, text="Status: Monitoring...", font=("Arial", 12), fg="blue")
status_label.pack(pady=20)

# Start MQTT client loop in a separate thread
def start_mqtt_loop():
    client.loop_start()

# Start the MQTT client loop
start_mqtt_loop()

# Start the Tkinter main loop
root.mainloop()
