#include "WiFiEsp.h"
#ifndef HAVE_HWSERIAL1
#endif
#include "SoftwareSerial.h"
#include <dht11.h>
#include <ArduinoJson.h>
#define DHT11PIN 7

/*
dht11 DHT11;
int PIR = 8;

SoftwareSerial Serial1(2, 3); // RX, TX

char ssid[] = "U+NetDDC3";            // your network SSID (name)
char pass[] = "4000017462";        // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status
//char server[] = "arduino.cc";
char server[] = "192.168.219.115";

WiFiEspClient client;
*/

void setup()
{
  while(true)
  {
   WiFiEspClient client;
   dht11 DHT11;
   int PIR = 8;
   SoftwareSerial Serial1(2, 3);
   char ssid[] = "U+NetDDC3";
   char pass[] = "4000017462";
   int status = WL_IDLE_STATUS;
   char server[] = "gudah1478.pythonanywhere.com";
  // initialize serial for debugging
  Serial.begin(9600);
  // initialize serial for ESP module
  Serial1.begin(9600);
  // initialize ESP module
  WiFi.init(&Serial1);
  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }
  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }
  // you're connected now, so print out the data
  Serial.println("You're connected to the network");
  printWifiStatus();
  Serial.println();
  Serial.println("Starting connection to server...");
  if (client.connect(server, 443)) {
    int chk = DHT11.read(DHT11PIN);
    String content = "";
    StaticJsonDocument<200> jsonBuffer;
    JsonObject root = jsonBuffer.to<JsonObject>();
    root["temp"] = DHT11.temperature;
    root["humi"] = DHT11.humidity;
    serializeJson(root, content);
    Serial.println("start send");
    client.println("POST /pmos/room_add/ HTTP/1.1");
    client.println("Host: gudah1478.pythonanywhere.com");
    client.println("Connection: close");
    client.println("Content-Type: application/json;");
    client.print("Content-Length: ");
    client.println(content.length());
    client.println();
    client.println(content);
    Serial.println("done");
    //delay(600000);
    delay(10000);
  }
  }
}

void loop()
{
  /*
  // if there are incoming bytes available
  // from the server, read them and print them
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }
  // if the server's disconnected, stop the client
  if (!client.connected()) {
    Serial.println();
    Serial.println("Disconnecting from server...");
    client.stop();
    // do nothing forevermore
    while (true);
  }
    int chk = DHT11.read(DHT11PIN);
    String content = "";
    StaticJsonDocument<200> jsonBuffer;
    JsonObject root = jsonBuffer.to<JsonObject>();
    root["temp"] = DHT11.temperature;
    root["humi"] = DHT11.humidity;
    serializeJson(root, content);
    /*
    client.print(F("POST /pmos/room_add/"));
    client.print(F(" HTTP/1.1\r\n"));
    client.print(F("Cache-Control: no-cache\r\n"));
    client.print(F("Host: 192.168.219.115:8000\r\n"));
    client.print(F("Content-Type: application/json\r\n"));
    client.print(F("Content-Length: "));
    client.println(content.length());
    client.println();
    client.println(content);
    client.print(F("\r\n\r\n"));
    client.println("Connection: close");
    client.println();
    Serial.println("start send");
    client.println("POST /pmos/room_add/ HTTP/1.1");
    client.println("Host: 192.168.219.115:8000");
    //client.println("Connection: close");
    client.println("Content-Type: application/json;");
    client.print("Content-Length: ");
    client.println(content.length());
    client.println();
    client.println(content);
    Serial.println("done");
    
    delay(1000);
    */
}

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  // print the received signal strength
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
