#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

const char* TAG_NAME = "TAG-01";

void setup() {
  Serial.begin(115200);
  BLEDevice::init(TAG_NAME);
  BLEServer* server = BLEDevice::createServer();
  BLEAdvertising* advertising = BLEDevice::getAdvertising();
  advertising->addServiceUUID(BLEUUID((uint16_t)0x180F));
  advertising->setScanResponse(true);
  advertising->start();
  Serial.println("BLE asset tag advertising...");
}

void loop() {
  delay(1000);
}
