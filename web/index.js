
// Lokasi tong sampah
const lokasiTongSampah1 = [-7.82062992849643, 110.42654669574745];
const lokasiTongSampah2 = [-7.820135382837104, 110.42666630956253];
const lokasiTongSampah3 = [-7.821398025909336, 110.42598761336608];

// Inisialisasi peta
const map = L.map('map').setView([-7.8204, 110.4266], 20); // Pusat peta

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Menambahkan marker untuk tong sampah dengan tampilan pop-up yang diperbarui
// ======== Tong sampah 1 ======== //
const markerTongSampah1 = L.marker(lokasiTongSampah1, {
icon: L.divIcon({ className: 'marker-empty', html: '🟢' })
}).addTo(map)
.bindPopup(`
<div style="font-family: Arial, sans-serif; padding: 10px;">
<h3 style="margin: 0; font-size: 18px;">Tong Sampah 1</h3>
<p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 1</p>
<p id="statusTongSampah1" class="status-empty-js" style="margin: 5px 0; font-weight: bold; color: green;">Status: Kosong</p>
</div>
`)
.openPopup();
// ======== Tong sampah 2 ======== //
const markerTongSampah2 = L.marker(lokasiTongSampah2, {
icon: L.divIcon({ className: 'marker-empty', html: '🟢' })
}).addTo(map)
.bindPopup(`
<div style="font-family: Arial, sans-serif; padding: 10px;">
<h3 style="margin: 0; font-size: 18px;">Tong Sampah 2</h3>
<p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 2</p>
<p id="statusTongSampah2" class="status-empty-js" style="margin: 5px 0; font-weight: bold; color: green;">Status: Kosong</p>
</div>
`);
// ======== Tong sampah 3 ======== //
const markerTongSampah3 = L.marker(lokasiTongSampah3, {
icon: L.divIcon({ className: 'marker-empty', html: '🟢' })
}).addTo(map)
.bindPopup(`
<div style="font-family: Arial, sans-serif; padding: 10px;">
<h3 style="margin: 0; font-size: 18px;">Tong Sampah 3</h3>
<p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 3</p>
<p id="statusTongSampah3" class="status-empty-js" style="margin: 5px 0; font-weight: bold; color: green;">Status: Kosong</p>
</div>
`);

// Inisialisasi MQTT
const client = mqtt.connect('ws://broker.mqttdashboard.com:8000/mqtt');

client.on('connect', function () {
console.log('MQTT Connected');
//  Clayen subacribe untuk mendapatkan data dari broker
client.subscribe('tong_sampah_1/status');
client.subscribe('tong_sampah_2/status');
client.subscribe('tong_sampah_3/status');
});

client.on('message', function (topic, message) {
const status = message.toString();

// ======== Tong sampah 1 ======== //
if (topic === 'tong_sampah_1/status') {
const statusElement = document.getElementById('statusTongSampah1');
statusElement.textContent = 'Status: ' + status;
if (status === 'Sudah Penuh') {
statusElement.classList.add('status-full');
statusElement.classList.remove('status-empty');
markerTongSampah1.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: red;">Tong Sampah 1 Penuh</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 1</p>
    <p style="margin: 5px 0;">Status: <span style="color: red; font-weight: bold;">Penuh</span></p>
    <p style="margin: 5px 0;">Mohon segera kosongkan tong sampah ini.</p>
  </div>
`).openPopup();
markerTongSampah1.setIcon(L.divIcon({ className: 'marker-full', html: '🔴' }));
playAlertSound();
} else {
statusElement.classList.add('status-empty');
statusElement.classList.remove('status-full');
markerTongSampah1.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: green;">Tong Sampah 1 Kosong</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 1</p>
    <p style="margin: 5px 0;">Status: <span style="color: green; font-weight: bold;">Kosong</span></p>
  </div>
`);
markerTongSampah1.setIcon(L.divIcon({ className: 'marker-empty', html: '🟢' }));
}
}

// ======== Tong sampah 2 ======== //
if (topic === 'tong_sampah_2/status') {
const statusElement = document.getElementById('statusTongSampah2');
statusElement.textContent = 'Status: ' + status;
if (status === 'Sudah Penuh') {
statusElement.classList.add('status-full');
statusElement.classList.remove('status-empty');
markerTongSampah2.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: red;">Tong Sampah 2 Penuh</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 2</p>
    <p style="margin: 5px 0;">Status: <span style="color: red; font-weight: bold;">Penuh</span></p>
    <p style="margin: 5px 0;">Mohon segera kosongkan tong sampah ini.</p>
  </div>
`).openPopup();
markerTongSampah2.setIcon(L.divIcon({ className: 'marker-full', html: '🔴' }));
playAlertSound();
} else {
statusElement.classList.add('status-empty');
statusElement.classList.remove('status-full');
markerTongSampah2.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: green;">Tong Sampah 2 Kosong</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 2</p>
    <p style="margin: 5px 0;">Status: <span style="color: green; font-weight: bold;">Kosong</span></p>
  </div>
`);
markerTongSampah2.setIcon(L.divIcon({ className: 'marker-empty', html: '🟢' }));
}
}

// ======== Tong sampah 3 ======== //
if (topic === 'tong_sampah_3/status') {
const statusElement = document.getElementById('statusTongSampah3');
statusElement.textContent = 'Status: ' + status;
if (status === 'Sudah Penuh') {
statusElement.classList.add('status-full');
statusElement.classList.remove('status-empty');
markerTongSampah3.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: red;">Tong Sampah 3 Penuh</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 3</p>
    <p style="margin: 5px 0;">Status: <span style="color: red; font-weight: bold;">Penuh</span></p>
    <p style="margin: 5px 0;">Mohon segera kosongkan tong sampah ini.</p>
  </div>
`).openPopup();
markerTongSampah3.setIcon(L.divIcon({ className: 'marker-full', html: '🔴' }));
playAlertSound();
} else {
statusElement.classList.add('status-empty');
statusElement.classList.remove('status-full');
markerTongSampah3.bindPopup(`
  <div style="font-family: Arial, sans-serif; padding: 10px;">
    <h3 style="margin: 0; font-size: 18px; color: green;">Tong Sampah 3 Kosong</h3>
    <p style="margin: 5px 0;">Alamat: Jl. Contoh Lokasi 3</p>
    <p style="margin: 5px 0;">Status: <span style="color: green; font-weight: bold;">Kosong</span></p>
  </div>
`);
markerTongSampah3.setIcon(L.divIcon({ className: 'marker-empty', html: '🟢' }));
}
}

//  End Tong sampah
});


// Fungsi untuk memutar suara alert
function playAlertSound() {
const audio = new Audio('pilager.mp3');
audio.play();
}

// Mengambil elemen link ( Saat di klick akan menuju ke tong ssampah )
document.getElementById("showLocationButton1").addEventListener("click", function() {
map.setView(lokasiTongSampah1, 20); // Koordinat untuk Tong Sampah 1
markerTongSampah1.openPopup(); // Menampilkan popup untuk Tong Sampah 1
});

document.getElementById("showLocationButton2").addEventListener("click", function() {
map.setView(lokasiTongSampah2, 20); // Koordinat untuk Tong Sampah 2
markerTongSampah2.openPopup(); // Menampilkan popup untuk Tong Sampah 2
});

document.getElementById("showLocationButton3").addEventListener("click", function() {
map.setView(lokasiTongSampah3, 20); // Koordinat untuk Tong Sampah 3
markerTongSampah3.openPopup(); // Menampilkan popup untuk Tong Sampah 3
});

