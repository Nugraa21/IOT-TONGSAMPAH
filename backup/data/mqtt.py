from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT Configuration
BROKER = "broker.mqttdashboard.com"
PORT = 8000
TOPICS = ["tong_sampah_1/status", "tong_sampah_2/status", "tong_sampah_3/status"]

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker: {rc}")
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} -> {msg.payload.decode()}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MQTT Tong Sampah</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }
            h1 {
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .form-container {
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .form-container h2 {
                color: #007bff;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-bottom: 10px;
                font-size: 14px;
            }
            .button-group {
                display: flex;
                gap: 10px;
            }
            button {
                padding: 10px 20px;
                font-size: 14px;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                opacity: 0.9;
            }
            .btn-primary {
                background-color: #007bff;
            }
            .btn-warning {
                background-color: #ffc107;
            }
            .btn-danger {
                background-color: #dc3545;
            }
            .btn-success {
                background-color: #28a745;
            }
            .status-container {
                margin-top: 20px;
            }
            .status-container h3 {
                margin-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            table th, table td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            table th {
                background-color: #007bff;
                color: white;
            }
            .clear-button {
                background-color: #ff4c4c;
            }
            .clear-button:hover {
                background-color: #d10000;
            }
        </style>
        <script>
            function sendData(topic, inputId) {
                const input = document.getElementById(inputId);
                const message = input.value;

                if (message) {
                    fetch("/publish", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ topic, message }),
                    })
                    .then(response => response.json())
                    .then(data => console.log(data.message))
                    .catch(err => console.error(err));
                    input.value = "";
                } else {
                    alert("Input tidak boleh kosong!");
                }
            }

            function sendMessage(topic, message) {
                fetch("/publish", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ topic, message }),
                })
                .then(response => response.json())
                .then(data => console.log(data.message))
                .catch(err => console.error(err));
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- Form Tong Sampah 1 -->
            <div class="form-container">
                <h2>Tong Sampah 1</h2>
                <label for="input-tong-1">Input Data Manual:</label>
                <input type="text" id="input-tong-1" placeholder="Masukkan data untuk tong sampah 1">
                <div class="button-group">
                    <button class="btn-primary" onclick="sendData('tong_sampah_1/status', 'input-tong-1')">Kirim Manual</button>
                    <button class="btn-warning" onclick="sendMessage('tong_sampah_1/status', 'Sudah Penuh')">Sudah Penuh</button>
                    <button class="btn-success" onclick="sendMessage('tong_sampah_1/status', 'Kosong')">Kosong</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    topic = data.get("topic")
    message = data.get("message")
    mqtt_client.publish(topic, message)
    return jsonify({"success": True, "message": f"Published '{message}' to '{topic}'"})

if __name__ == "__main__":
    app.run(debug=True)
