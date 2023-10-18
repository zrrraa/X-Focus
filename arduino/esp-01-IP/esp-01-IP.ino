
/*
    WiFi Connect - connecting Arduino Nano 33 BLE to WiFi using an ESP-01 and
    WiFiEspAT library. WiFi settings stored in seperate configuration file. 
*/
#include <WiFiEspAT.h>    // Include the Wi-Fi library
#include "config.h"


void setup() {

    // Start the Serial communication to send messages to the computer
    Serial.begin(115200);
    while(!Serial);
    delay(10);
    Serial.println("Arduino Nano 33 BLE WiFi Connection Demo");

    // Start serial communication to wifi module
    Serial1.begin(115200);
    WiFi.init(Serial1);

    // check for the WiFi module:
    if (WiFi.status() == WL_NO_MODULE) {
        Serial.println();
        Serial.println("Communication with WiFi module failed!");
        // don't continue
        while (true);
    }

    WiFi.endAP(true); // to disable default automatic start of persistent AP at startup

    WiFi.setPersistent(); // set the following WiFi connection as persistent


    // Create and assign a hostname to the device
    // Hostname is generated as a prefix combined with the chip id code as a hexidecimal string
    String s_hostname = "Nano33BLE-" + String(NRF_FICR->DEVICEID[1], HEX);
    int n = s_hostname.length();
    char hostname[n+1];
    s_hostname.toCharArray(hostname, n+1);
    Serial.println();
    Serial.print("Setting hostname to: ");
    Serial.println(hostname);
    // WiFi.hostname(hostname);
    WiFi.setHostname(hostname);


    // Connect to the WiFi network
    WiFi.begin(ssid, password);
    Serial.print("Connecting to SSID: ");
    Serial.print(ssid); Serial.println(" ...");

    while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
        delay(1000);
        Serial.print('.');
    }

    Serial.println("");
    Serial.println("Connection established!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());         // Get the assigned IP address

    // print the received signal strength:
    Serial.print("signal strength (RSSI):");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");

}

void loop() {
    // empty
}
