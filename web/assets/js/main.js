    // Lokasi tong sampah
    const lokasiTongSampah1 = [-7.82062992849643, 110.42654669574745];
    const lokasiTongSampah2 = [-7.820135382837104, 110.42666630956253];

    // Inisialisasi peta
    const map = L.map('map').setView([-7.8204, 110.4266], 16); // Pusat peta

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Menambahkan marker untuk tong sampah
    const markerTongSampah1 = L.marker(lokasiTongSampah1).addTo(map)
      .bindPopup('Tong Sampah 1')
      .openPopup();

    const markerTongSampah2 = L.marker(lokasiTongSampah2).addTo(map)
      .bindPopup('Tong Sampah 2');

    // Inisialisasi MQTT
    const client = mqtt.connect('ws://broker.mqttdashboard.com:8000/mqtt');

    client.on('connect', function () {
      console.log('MQTT Connected');
      client.subscribe('tong_sampah_1/status');
      client.subscribe('tong_sampah_2/status');
    });

    client.on('message', function (topic, message) {
      const status = message.toString();
      
      if (topic === 'tong_sampah_1/status') {
        const statusElement = document.getElementById('statusTongSampah1');
        statusElement.textContent = 'Status: ' + status;
        if (status === 'Sudah Penuh') {
          statusElement.classList.add('status-full');
          statusElement.classList.remove('status-empty');
          markerTongSampah1.bindPopup('Tong Sampah 1 Penuh').openPopup();
        } else {
          statusElement.classList.add('status-empty');
          statusElement.classList.remove('status-full');
        }
      }

      if (topic === 'tong_sampah_2/status') {
        const statusElement = document.getElementById('statusTongSampah2');
        statusElement.textContent = 'Status: ' + status;
        if (status === 'Sudah Penuh') {
          statusElement.classList.add('status-full');
          statusElement.classList.remove('status-empty');
          markerTongSampah2.bindPopup('Tong Sampah 2 Penuh').openPopup();
        } else {
          statusElement.classList.add('status-empty');
          statusElement.classList.remove('status-full');
        }
      }
    });