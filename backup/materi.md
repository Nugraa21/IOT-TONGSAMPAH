

```
broker.mqttdashboard.com
```

## Tong sampah 1
```c
#include <WiFi.h>
#include <PubSubClient.h>

// Konfigurasi WiFi
const char* ssid = "nugra";  // Ganti dengan nama SSID WiFi
const char* password = "081328400060";  // Ganti dengan password WiFi

// Konfigurasi MQTT
const char* mqtt_server = "broker.mqttdashboard.com";
const char* topic = "tong_sampah_1/status";
WiFiClient espClient;
PubSubClient client(espClient);

// Definisikan pin untuk sensor ultrasonik dan buzzer
const int trigPin = 16;  // Pin Trigger
const int echoPin = 4;  // Pin Echo
const int buzzerPin = 5; // Pin buzzer

void setup() {
  Serial.begin(115200);

  // Inisialisasi WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

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

```
##  Tong sampah 2 
```c
#include <WiFi.h>
#include <PubSubClient.h>

// Konfigurasi WiFi
const char* ssid = "nugra";  // Ganti dengan nama SSID WiFi
const char* password = "081328400060";  // Ganti dengan password WiFi

// Konfigurasi MQTT
const char* mqtt_server = "broker.mqttdashboard.com";
const char* topic = "tong_sampah_2/status";
WiFiClient espClient;
PubSubClient client(espClient);

// Definisikan pin untuk sensor ultrasonik dan buzzer
const int trigPin = 16;  // Pin Trigger
const int echoPin = 4;  // Pin Echo
const int buzzerPin = 5; // Pin buzzer

void setup() {
  Serial.begin(115200);

  // Inisialisasi WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

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
  if (distance > 20) {
    status = "Kosong";
    digitalWrite(buzzerPin, LOW);
  } else if (distance > 10 && distance <= 20) {
    status = "Hampir Penuh";
    digitalWrite(buzzerPin, LOW);
  } else if (distance <= 10) {
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
    if (client.connect("ESP32_TongSampah_2")) { // Client ID untuk Tong Sampah 2
      client.subscribe(topic);
    } else {
      delay(5000);
    }
  }
}

```