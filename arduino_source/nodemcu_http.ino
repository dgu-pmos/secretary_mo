#include <time.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char*  ssid = "U+NetDDC3";
const char* password = "4000017462";

const char* host = "gudah1478.pythonanywhere.com";
const int httpsPort = 443;

// Root certificate used by api.github.com.
// Defined in "CACert" tab.
extern const unsigned char caCert[] PROGMEM;
extern const unsigned int caCertLen;

WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Synchronize time useing SNTP. This is necessary to verify that
  // the TLS certificates offered by the server are currently valid.
  Serial.print("Setting time using SNTP");
  configTime(8 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));

  // Load root certificate in DER format into WiFiClientSecure object
  bool res = client.setCACert_P(caCert, caCertLen);
  if (!res) {
    Serial.println("Failed to load root CA certificate!");
    while (true) {
      yield();
    }
  }
}

void loop() {
  String content = "";
  StaticJsonDocument<200> jsonBuffer;
  JsonObject root = jsonBuffer.to<JsonObject>();
  //root["temp"] = DHT11.temperature;
  //root["humi"] = DHT11.humidity;
  root["temp"] = 30;
  root["humi"] = 60;
  serializeJson(root, content);
  // Connect to remote server
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }

  // Verify validity of server's certificate
  if (client.verifyCertChain(host)) {
    Serial.println("Server certificate verified");
  } else {
    Serial.println("ERROR: certificate verification failed!");
 //   return;
  }

  String url = "/pmos/room_add/";
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: BuildFailureDetectorESP8266\r\n" +
               "Connection: close\r\n" +
               "Content-Type: application/json;\r\n" +
               "Content-Length: " + content.length() + "\r\n\r\n" +
               content + "r\n"
               );
  /*
  Serial.println("request sent");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  if (line.startsWith("{\"state\":\"success\"")) {
    Serial.println("esp8266/Arduino CI successfull!");
  } else {
    Serial.println("esp8266/Arduino CI has failed");
  }
  Serial.println("reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println();

  static int repeat = 0;
  if (++repeat == 3) {
    Serial.println("Done");
    while (true) {
      delay(1000);
    }
  }
  */
  delay(10000);
}
