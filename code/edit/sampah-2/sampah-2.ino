#include <WiFi.h>
#include <WiFiManager.h>
#include <PubSubClient.h>

// Konfigurasi MQTT
const char* mqtt_server = "broker.mqttdashboard.com";
const char* topic = "tong_sampah_2/status";
WiFiClient espClient;
PubSubClient client(espClient);

// Definisikan pin untuk sensor ultrasonik dan buzzer
const int trigPin = 16;  // Pin Trigger
const int echoPin = 4;   // Pin Echo
const int buzzerPin = 5; // Pin buzzer

void setup() {
  Serial.begin(115200);

  // Inisialisasi WiFi Manager
  WiFiManager wm;
  wm.setAPCallback(configModeCallback);  // Callback saat ESP masuk mode konfigurasi

  // ESP32 membuat hotspot untuk konfigurasi WiFi
  if (!wm.autoConnect("Tongsampah-2", "12345678")) {
    Serial.println("Gagal menghubungkan ke WiFi. Restarting...");
    ESP.restart();
  }
  Serial.println("WiFi connected");

  // Inisialisasi MQTT
  client.setServer(mqtt_server, 1883);

  // Inisialisasi Pin
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long distance = measureDistance();

  // Tentukan status berdasarkan jarak
  String status;
  if (distance > 10) {
    status = "Kosong";
    digitalWrite(buzzerPin, LOW);
  } else if (distance > 5 && distance <= 20) {
    status = "Hampir Penuh";
    digitalWrite(buzzerPin, LOW);
  } else if (distance <= 5) {
    status = "Sudah Penuh";
    digitalWrite(buzzerPin, HIGH);
  }

  // Kirim status ke MQTT
  client.publish(topic, status.c_str());
  Serial.println("Status: " + status);

  delay(2000); // Delay untuk pembacaan berikutnya
}

// Fungsi untuk mengukur jarak
long measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;
  return distance;
}

// Fungsi untuk reconnect MQTT
void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32_TongSampah_1")) {
      client.subscribe(topic);
    } else {
      delay(5000);
    }
  }
}

// Callback saat ESP32 masuk mode konfigurasi
void configModeCallback(WiFiManager *myWiFiManager) {
  Serial.println("Masuk mode konfigurasi!");
  Serial.println("Buka WiFi dan hubungkan ke: ESP32_TongSampah");
  Serial.println("Akses alamat ini di browser: http://192.168.4.1");
}
