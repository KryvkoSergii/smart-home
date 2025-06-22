#include <WiFi.h>
#include <PubSubClient.h>

// --- Налаштування WiFi ---
const char* ssid = "----";
const char* password = "------";

// --- Налаштування MQTT ---
const char* mqtt_server = "-----"; // IP Mosquitto broker
const int mqtt_port = 1883;
const char* mqtt_user = "";  // if no auth — leave empty
const char* mqtt_pass = "";

const char* mqtt_sub_topic = "toDevice/topic";
const char* mqtt_pub_topic = "fromDevice/topic";

WiFiClient espClient;
PubSubClient client(espClient);

// --- Callback on receive MQTT event ---
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Received event from topic: ");
  Serial.println(topic);
  Serial.print("Content: ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connect to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP addr: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connection to MQTT...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("connected");
      client.subscribe(mqtt_sub_topic);
    } else {
      Serial.print("error, rc=");
      Serial.print(client.state());
      Serial.println(" attempt 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // sending event every 5 sec
  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    String msg = "From ESP32!";
    client.publish(mqtt_pub_topic, msg.c_str());
    Serial.println("Message sent: " + msg);
  }
}
