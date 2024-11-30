import tkinter as tk
import tkintermapview

# Fungsi untuk memperbarui marker berdasarkan status
def update_marker(status, marker):
    # Update ikon marker berdasarkan status
    if status == "Sudah Penuh":
        marker.set_icon("full_marker_icon.png")  # Ganti dengan ikon untuk penuh
    else:
        marker.set_icon("empty_marker_icon.png")  # Ganti dengan ikon untuk kosong
    print(f"Status: {status}")

# Setup window Tkinter
root = tk.Tk()
root.title("Peta Lokasi Tong Sampah")
root.geometry("800x600")

# Membuat frame untuk peta
map_frame = tk.Frame(root)
map_frame.pack(fill="both", expand=True)

# Membuat peta menggunakan tkintermapview
map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0)
map_widget.set_position(-7.795580, 110.369490)  # Koordinat lat/lng Yogyakarta (ganti sesuai lokasi yang diinginkan)
map_widget.set_zoom(15)  # Set zoom level
map_widget.pack(fill="both", expand=True)

# Menambahkan marker untuk Tong Sampah 1 dan 2
marker1 = map_widget.set_marker(-7.795580, 110.369490, text="Tong Sampah 1")
marker2 = map_widget.set_marker(-7.796000, 110.370000, text="Tong Sampah 2")

# Status awal marker (kosong)
status_tong_1 = "Kosong"
status_tong_2 = "Kosong"

# Fungsi untuk memperbarui status secara manual (simulasi)
def update_status():
    global status_tong_1, status_tong_2

    # Simulasi perubahan status
    if status_tong_1 == "Kosong":
        status_tong_1 = "Sudah Penuh"
    else:
        status_tong_1 = "Kosong"

    if status_tong_2 == "Kosong":
        status_tong_2 = "Sudah Penuh"
    else:
        status_tong_2 = "Kosong"

    # Update marker berdasarkan status
    update_marker(status_tong_1, marker1)
    update_marker(status_tong_2, marker2)

    # Tampilkan status di console
    print(f"Status Tong Sampah 1: {status_tong_1}")
    print(f"Status Tong Sampah 2: {status_tong_2}")

# Tombol untuk memperbarui status (simulasi perubahan)
update_button = tk.Button(root, text="Update Status", command=update_status)
update_button.pack(pady=20)

# Menjalankan aplikasi Tkinter
root.mainloop()
