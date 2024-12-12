// Lokasi tong sampah
const lokasiTongSampah = [
  { id: 1, lokasi: [-7.82062992849643, 110.42654669574745], nama: 'Tong Sampah 1' },
  { id: 2, lokasi: [-7.820135382837104, 110.42666630956253], nama: 'Tong Sampah 2' },
  { id: 3, lokasi: [-7.821398025909336, 110.42598761336608], nama: 'Tong Sampah 3' }
];

// Inisialisasi peta
const map = L.map('map').setView([-7.8204, 110.4266], 20); // Pusat peta

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fungsi untuk membuat marker dan pop-up
function createMarker(tongSampah) {
  const marker = L.marker(tongSampah.lokasi, {
      icon: L.divIcon({ className: 'marker-empty', html: '🟢' })
  }).addTo(map)
      .bindPopup(`
          <div style="font-family: Arial, sans-serif; padding: 10px;">
              <h3 style="margin: 0; font-size: 18px;">${tongSampah.nama}</h3>
              <p style="margin: 5px 0;">Alamat: Sekarsuli, Sendangtirto, Kec. Berbah, Kabupaten Sleman, Daerah Istimewa</p>
              <p id="statusTongSampah${tongSampah.id}" class="status-empty-js" style="margin: 5px 0; font-weight: bold; color: green;">Status: Kosong</p>
          </div>
      `);

  // Mengembalikan marker untuk referensi di masa depan
  return marker;
}

// Membuat marker untuk semua tong sampah
const markers = lokasiTongSampah.map(tongSampah => {
  return createMarker(tongSampah);
});

// Inisialisasi MQTT
const client = mqtt.connect('ws://broker.mqttdashboard.com:8000/mqtt');

client.on('connect', function () {
  console.log('MQTT Connected');
  // Subscribe untuk mendapatkan data dari broker
  client.subscribe('tong_sampah_1/status');
  client.subscribe('tong_sampah_2/status');
  client.subscribe('tong_sampah_3/status');
});

client.on('message', function (topic, message) {
  const status = message.toString();
  const tongId = parseInt(topic.split('_')[2]); // Mengambil id tong sampah dari topic

  // Menangani status perubahan setiap tong sampah
  const statusElement = document.getElementById(`statusTongSampah${tongId}`);
  const marker = markers[tongId - 1]; // Mendapatkan marker yang sesuai berdasarkan ID

  statusElement.textContent = 'Status: ' + status;

  if (status === 'Sudah Penuh') {
      statusElement.classList.add('status-full');
      statusElement.classList.remove('status-empty');
      marker.bindPopup(`
          <div style="font-family: Arial, sans-serif; padding: 10px;">
              <h3 style="margin: 0; font-size: 18px; color: red;">${marker.getPopup().getContent().match(/<h3.*?>(.*?)<\/h3>/)[1]} Penuh</h3>
              <p style="margin: 5px 0;">Alamat: Sekarsuli, Sendangtirto, Kec. Berbah, Kabupaten Sleman, Daerah Istimewa</p>
              <p style="margin: 5px 0;">Status: <span style="color: red; font-weight: bold;">Penuh</span></p>
              <p style="margin: 5px 0;">Mohon segera kosongkan tong sampah ini.</p>
          </div>
      `).openPopup();
      marker.setIcon(L.divIcon({ className: 'marker-full', html: '🔴' }));
      playAlertSound();
  } else {
      statusElement.classList.add('status-empty');
      statusElement.classList.remove('status-full');
      marker.bindPopup(`
          <div style="font-family: Arial, sans-serif; padding: 10px;">
              <h3 style="margin: 0; font-size: 18px; color: green;">${marker.getPopup().getContent().match(/<h3.*?>(.*?)<\/h3>/)[1]} Kosong</h3>
              <p style="margin: 5px 0;">Alamat: Sekarsuli, Sendangtirto, Kec. Berbah, Kabupaten Sleman, Daerah Istimewa</p>
              <p style="margin: 5px 0;">Status: <span style="color: green; font-weight: bold;">Kosong</span></p>
          </div>
      `);
      marker.setIcon(L.divIcon({ className: 'marker-empty', html: '🟢' }));
  }
});

// Fungsi untuk memutar suara peringatan
function playAlertSound() {
  const audio = new Audio('pilager.mp3'); // Ganti dengan path suara yang diinginkan
  audio.play();
}
