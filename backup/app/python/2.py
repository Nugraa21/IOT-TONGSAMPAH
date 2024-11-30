import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
import folium
from folium.plugins import MarkerCluster
import webbrowser


# Konfigurasi MQTT
mqtt_server = "broker.mqttdashboard.com"
topic_tong_sampah_1 = "tong_sampah_1/status"
topic_tong_sampah_2 = "tong_sampah_2/status"

# Lokasi tong sampah
location_tong_sampah_1 = [-7.820640656827386, 110.4265487821296]
location_tong_sampah_2 = [-7.820160663142095, 110.42662803314063]

# Fungsi untuk update label status
def update_status(status, topic):
    if topic == topic_tong_sampah_1:
        label_tong_sampah_1.config(text=f"Status Tong Sampah 1: {status}")
    elif topic == topic_tong_sampah_2:
        label_tong_sampah_2.config(text=f"Status Tong Sampah 2: {status}")
    
    # Pemberian notifikasi
    if status == "Sudah Penuh":
        status_label.config(text=f"ALERT: {topic} is FULL!", fg="red")
        update_map_marker(status, topic)
    elif status == "Kosong":
        status_label.config(text=f"{topic} is EMPTY. (Empty)", fg="green")
        update_map_marker(status, topic)
    elif status == "Hampir Penuh":
        status_label.config(text=f"{topic} is NEAR FULL. (Near Full)", fg="yellow")
        update_map_marker(status, topic)

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

# Frame untuk Navbar
navbar_frame = tk.Frame(root)
navbar_frame.pack(side="top", fill="x", pady=5)

# Button untuk navigasi
def show_monitoring():
    monitoring_frame.pack(side="top", fill="both", expand=True)
    map_frame.pack_forget()

def show_map():
    map_frame.pack(side="top", fill="both", expand=True)
    monitoring_frame.pack_forget()

navbar_monitoring_button = tk.Button(navbar_frame, text="Monitoring", command=show_monitoring)
navbar_monitoring_button.pack(side="left", padx=10)

navbar_map_button = tk.Button(navbar_frame, text="Peta", command=show_map)
navbar_map_button.pack(side="left", padx=10)

# Frame untuk Monitoring
monitoring_frame = tk.Frame(root)
monitoring_frame.pack(side="top", fill="both", expand=True)

# Cart untuk monitoring status tong sampah
cart_frame = tk.LabelFrame(monitoring_frame, text="Status Tong Sampah", font=("Arial", 14), padx=10, pady=10)
cart_frame.pack(pady=20, padx=20, fill="both", expand=True)

label_tong_sampah_1 = tk.Label(cart_frame, text="Status Tong Sampah 1: Waiting...", font=("Arial", 14))
label_tong_sampah_1.grid(row=0, column=0, pady=10)

label_tong_sampah_2 = tk.Label(cart_frame, text="Status Tong Sampah 2: Waiting...", font=("Arial", 14))
label_tong_sampah_2.grid(row=1, column=0, pady=10)

# Label untuk notifikasi
status_label = tk.Label(cart_frame, text="Status: Monitoring...", font=("Arial", 12), fg="blue")
status_label.grid(row=2, column=0, pady=20)

# Frame untuk Peta
map_frame = tk.Frame(root)

# Inisialisasi peta dengan lokasi tong sampah
m = folium.Map(location=[-7.8204, 110.4266], zoom_start=15)

# Membuat marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Menambahkan marker untuk tong sampah 1
marker_tong_sampah_1 = folium.Marker(location_tong_sampah_1, popup="Tong Sampah 1", icon=folium.Icon(color='blue'))
marker_tong_sampah_1.add_to(marker_cluster)

# Menambahkan marker untuk tong sampah 2
marker_tong_sampah_2 = folium.Marker(location_tong_sampah_2, popup="Tong Sampah 2", icon=folium.Icon(color='blue'))
marker_tong_sampah_2.add_to(marker_cluster)

# Fungsi untuk update marker berdasarkan status
def update_map_marker(status, topic):
    if topic == topic_tong_sampah_1:
        if status == "Sudah Penuh":
            marker_tong_sampah_1.popup = "Tong Sampah 1: PENUH!"
            marker_tong_sampah_1.icon = folium.Icon(color='red')
        elif status == "Kosong":
            marker_tong_sampah_1.popup = "Tong Sampah 1: KOSONG"
            marker_tong_sampah_1.icon = folium.Icon(color='green')
        elif status == "Hampir Penuh":
            marker_tong_sampah_1.popup = "Tong Sampah 1: HAMPIR PENUH"
            marker_tong_sampah_1.icon = folium.Icon(color='yellow')
    elif topic == topic_tong_sampah_2:
        if status == "Sudah Penuh":
            marker_tong_sampah_2.popup = "Tong Sampah 2: PENUH!"
            marker_tong_sampah_2.icon = folium.Icon(color='red')
        elif status == "Kosong":
            marker_tong_sampah_2.popup = "Tong Sampah 2: KOSONG"
            marker_tong_sampah_2.icon = folium.Icon(color='green')
        elif status == "Hampir Penuh":
            marker_tong_sampah_2.popup = "Tong Sampah 2: HAMPIR PENUH"
            marker_tong_sampah_2.icon = folium.Icon(color='yellow')

    # Simpan peta untuk diperbarui di GUI
    m.save("map.html")
    webbrowser.open("map.html")  # Membuka peta di browser setelah diupdate
    messagebox.showinfo("Peta Diperbarui", "Peta telah diperbarui dengan status terbaru!")

# Start MQTT client loop in a separate thread
def start_mqtt_loop():
    client.loop_start()

# Start the MQTT client loop
start_mqtt_loop()

# Start the Tkinter main loop
root.mainloop()
