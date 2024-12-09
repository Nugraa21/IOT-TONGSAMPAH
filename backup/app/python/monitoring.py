import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt

# Konfigurasi MQTT
mqtt_server = "broker.mqttdashboard.com"
topic_tong_sampah_1 = "tong_sampah_1/status"
topic_tong_sampah_2 = "tong_sampah_2/status"

# Fungsi untuk update status pada dashboard
def update_status(status, topic):
    if topic == topic_tong_sampah_1:
        label_tong_sampah_1.config(text=f"Status Tong Sampah 1: {status}")
    elif topic == topic_tong_sampah_2:
        label_tong_sampah_2.config(text=f"Status Tong Sampah 2: {status}")
    
    # Pemberian notifikasi dan perubahan warna
    if status == "Sudah Penuh":
        status_label.config(text=f"ALERT: {topic} is FULL!", fg="red", font=("Arial", 14, "bold"))
        root.config(bg="lightcoral")
    elif status == "Kosong":
        status_label.config(text=f"{topic} is EMPTY. (Empty)", fg="green", font=("Arial", 14, "bold"))
        root.config(bg="lightgreen")
    elif status == "Hampir Penuh":
        status_label.config(text=f"{topic} is NEAR FULL. (Near Full)", fg="yellow", font=("Arial", 14, "bold"))
        root.config(bg="lightyellow")

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
root.title("Dashboard Monitoring Tong Sampah")
root.geometry("600x400")
root.config(bg="#f0f0f0")

# Frame utama
main_frame = tk.Frame(root, bg="#ffffff", bd=10)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title Label
title_label = tk.Label(main_frame, text="Monitoring Tong Sampah", font=("Arial", 18, "bold"), bg="#ffffff")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Label untuk status Tong Sampah 1
label_tong_sampah_1 = tk.Label(main_frame, text="Status Tong Sampah 1: Waiting...", font=("Arial", 14), bg="#ffffff")
label_tong_sampah_1.grid(row=1, column=0, pady=5, padx=10, sticky="w")

# Label untuk status Tong Sampah 2
label_tong_sampah_2 = tk.Label(main_frame, text="Status Tong Sampah 2: Waiting...", font=("Arial", 14), bg="#ffffff")
label_tong_sampah_2.grid(row=2, column=0, pady=5, padx=10, sticky="w")

# Label untuk status alert
status_label = tk.Label(main_frame, text="Status: Monitoring...", font=("Arial", 12), fg="blue", bg="#ffffff")
status_label.grid(row=3, column=0, columnspan=2, pady=10)
s
# Button untuk refresh atau menghubungkan kembali (opsional)
def reconnect():
    try:
        client.reconnect()
        status_label.config(text="Reconnected to Broker", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Connection failed: {e}")

reconnect_button = tk.Button(main_frame, text="Reconnect", command=reconnect, font=("Arial", 12), bg="skyblue", relief="raised")
reconnect_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start MQTT client loop in a separate thread
def start_mqtt_loop():
    client.loop_start()

# Start the MQTT client loop
start_mqtt_loop()

# Start the Tkinter main loop
root.mainloop()


# data 