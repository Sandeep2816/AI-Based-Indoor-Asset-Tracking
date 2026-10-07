/*
  ESP32 BLE Anchor
  Configure Wi-Fi and MQTT values locally before flashing.
  Never commit real credentials.
*/
#include <WiFi.h>
#include <PubSubClient.h>
#include <BLEDevice.h>
#include <BLEScan.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* MQTT_HOST = "192.168.1.100";
const char* ANCHOR_ID = "A1";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
BLEScan* scanner;

void connectWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void connectMqtt() {
  mqtt.setServer(MQTT_HOST, 1883);
  while (!mqtt.connected()) {
    mqtt.connect(ANCHOR_ID);
    delay(500);
  }
}

void setup() {
  Serial.begin(115200);
  connectWifi();
  connectMqtt();
  BLEDevice::init("");
  scanner = BLEDevice::getScan();
  scanner->setActiveScan(true);
}

void loop() {
  if (!mqtt.connected()) connectMqtt();
  mqtt.loop();

  BLEScanResults* results = scanner->start(3, false);

  for (int i = 0; i < results->getCount(); i++) {
    BLEAdvertisedDevice device = results->getDevice(i);
    String name = device.getName().c_str();

    if (name.startsWith("TAG-")) {
      String topic = String("anchor/") + ANCHOR_ID + "/rssi";
      String payload = String("{\"anchor_id\":\"") + ANCHOR_ID +
        String("\",\"tag_id\":\"") + name +
        String("\",\"rssi\":") + device.getRSSI() + String("}");
      mqtt.publish(topic.c_str(), payload.c_str());
    }
  }
  scanner->clearResults();
}
