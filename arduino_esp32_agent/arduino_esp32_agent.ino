#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>

#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#include <HTTPClient.h>

float temp, humi, temperatureC, temperatureF;
String aray[100]={},aray2[100]={};

const char* assid ="esp32";
const char* asecret ="esp32@2020";
/*Put your SSID & Password*/
const char* ssid = "Depeka";  // Enter SSID here
const char* password = "SudKriDep242612";  //Enter Password here
const char* emails = "depekakrishnan12@gmail.com";

#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define ONBOARD_LED  2
#define DHTTYPE    DHT11     // DHT 11

DHT dht(DHTPIN, DHTTYPE);

#define REPORTING_PERIOD_MS     1000

AsyncWebServer server(80);

void notFound(AsyncWebServerRequest *request) {
    request->send(404, "text/plain", "Not found");
}

// GPIO where the DS18B20 is connected to
const int oneWireBus = 5;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

String readDHTTemperature() 
{
  float t = dht.readTemperature();
  if (isnan(t)) 
  {    
    Serial.println("Failed to read from DHT sensor!");
    return "--";
  }
  else 
  {
    Serial.print("Temperature : ");
    Serial.println(t);
    return String(t);
  }
}

String readDHTHumidity() 
{
  float h = dht.readHumidity();
  if (isnan(h)) 
  {
    Serial.println("Failed to read from DHT sensor!");
    return "--";
  }
  else 
  {
    Serial.print("Humidity : ");
    Serial.println(h);
    return String(h);
  }
}

void onBeatDetected()
{
  Serial.println("Beat!");
}

void types(String a,String b) { Serial.println(b+" it's a String"); }
void types(int a,String b) { Serial.println(b+" it's an int"); }
void types(char *a,String b) { Serial.println(b+" it's a char*"); }
void types(float a,String b) { Serial.println(b+" it's a float"); }
void types(bool a,String b) { Serial.println(b+" it's a bool"); }

String jsoner(float temp, float humi, float bodyC, float bodyF, String aray[100], String aray2[100], String emails)
{
String json_d="{";
json_d+="'BodyTempC':";
json_d+=(int)bodyC;
json_d+=",'BodyTempF':";
json_d+=(int)bodyF;
json_d+=",'Humidity':";
json_d+=(int)humi;
json_d+=",'Temperature':";
json_d+=(int)temp;
json_d+=",'Email':'";
json_d+=(String)emails;
json_d+="','wifi_names':['";
for(int i=0; i<=99;i++)
{
  json_d+=(aray[i]);
  json_d+="','";
}
json_d+="'],'wifi_ids':['";
for(int i=0; i<=99;i++)
{
  json_d+=(aray2[i]);
  json_d+="','";
}
json_d+="']}";

return json_d;
}


void setup()
{
  Serial.begin(115200);
  dht.begin();
  WiFi.mode(WIFI_AP_STA);
   pinMode(ONBOARD_LED,OUTPUT);
  // Start the DS18B20 sensor
  sensors.begin();

  sensors.requestTemperatures(); 
  temperatureC = sensors.getTempCByIndex(0);
  temperatureF = sensors.getTempFByIndex(0);
  Serial.print(temperatureC);
  Serial.println("ºC");
  Serial.print(temperatureF);
  Serial.println("ºF");
  
  
  temp = readDHTTemperature().toFloat();
  humi = readDHTHumidity().toFloat();
  Serial.println("Post Function Call : ");
  Serial.println(temp);
  Serial.println(humi);

  Serial.println("Post Function Call 2 : ");
  
  types(temp,"temp");
  types(humi,"humi");
  
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  int n = WiFi.scanNetworks();
    Serial.println("scan done");
    if (n == 0) {
        Serial.println("no networks found");
    } else {
        Serial.print(n);
        Serial.println(" networks found");
        for (int i = 0; i < n; ++i) {
            // Print SSID and RSSI for each network found
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(WiFi.SSID(i));
            Serial.print(" (");
            Serial.print(WiFi.RSSI(i));
            Serial.print(")");
            Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
            
            delay(10);
            aray[i]=(WiFi.SSID(i));
            aray2[i]=(WiFi.RSSI(i));
            if((WiFi.RSSI(i))<(-90)){
              digitalWrite(ONBOARD_LED,HIGH);}
              else{
           digitalWrite(ONBOARD_LED,LOW);  }
        }
    }
  
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", jsoner(temp, humi, temperatureC, temperatureF, aray, aray2, emails).c_str());
  });
  server.onNotFound(notFound);
  server.begin();
  HTTPClient http;
  http.begin("http://192.168.10:5001/begin_loop?device=esp32");
  int httpCode = http.GET();                                        //Make the request
 
    if (httpCode > 0) { //Check for the returning code
 
        //String payload = http.getString();
        Serial.println(httpCode);
        Serial.println("Triggered");
      }
 
    else {
      Serial.println("Error on HTTP request");
    }
 
    http.end();
}

void test()
{
  sensors.requestTemperatures(); 
  temperatureC = sensors.getTempCByIndex(0);
  temperatureF = sensors.getTempFByIndex(0);

  temp = readDHTTemperature().toFloat();
  humi = readDHTHumidity().toFloat();

  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0) 
  {
    Serial.println("no networks found");
  } 
  else 
  {
     Serial.print(n);
     Serial.println(" networks found");
     for (int i = 0; i < n; ++i) 
     {
       // Print SSID and RSSI for each network found
       delay(10);
       aray[i]=(WiFi.SSID(i));
       aray2[i]=(WiFi.RSSI(i));
            
      }
   }
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    //request->send_P(200, "text/html", pager(temp, humi, temperatureC, temperatureF, aray, aray2).c_str());
    request->send_P(200, "text/html", jsoner(temp, humi, temperatureC, temperatureF, aray, aray2, emails).c_str());
  });
  server.onNotFound(notFound);
}

void loop()
{
  test();
  delay(50000);
}