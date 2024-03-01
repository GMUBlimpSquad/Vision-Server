#include <eloquent_esp32cam.h>
#include <WiFi.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <ESP32Servo.h>
// #include <cstring>


#define WIFI_SSID "SPARXnet"
#define WIFI_PASSWORD "smolydolio!78DB3"
#define HOSTNAME  "esp32cam"


#define HOST "192.168.1.198"
#define PORT 8000
#define MOTOR 12


WiFiClient client;

Servo myservo;
int x_1, y_1, x_2, y_2;
void setup() {
  // put your setup code here, to run once:
    delay(3000);
    Serial.begin(115200);
    Serial.println("___Camera Streamer___");
    myservo.attach(MOTOR, 1000, 2000);
    myservo.setPeriodHertz(50);
    // camera settings
    // replace with your own model!
    eloq::camera.pinout.aithinker();
    eloq::camera.brownout.disable();
    // Edge Impulse models work on square images
    // face resolution is 240x240
    eloq::camera.resolution.face();
    eloq::camera.quality.high();

    // init camera
    while (!eloq::camera.begin().isOk())
        Serial.println(eloq::camera.exception.toString());

    // connect to WiFi
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    myservo.write(90);
    delay(500);
    myservo.write(0);
    delay(500);
    myservo.write(180);
    delay(500);
    myservo.write(0);
    delay(500);
    myservo.write(90);

  if(!client.connect(HOST, PORT)){
    return;
  }
}

String objDetect(){

    if (!eloq::camera.capture().isOk()) {
        Serial.println(eloq::camera.exception.toString());
        return "";
    }
    client.print(eloq::camera.frame->len);
    client.write((const char *) eloq::camera.frame->buf, eloq::camera.frame->len);
    client.flush();
    x_1 = client.readStringUntil(',').toInt();
    y_1 = client.readStringUntil(',').toInt();
    x_2 = client.readStringUntil(',').toInt();
    y_2 = client.readStringUntil(',').toInt();
    String str = client.readStringUntil('#');
    return str;
}

void loop() {
  // put your main code here, to run repeatedly:

    if(!client.connected()){
      if(!client.connect(HOST, PORT)){
        return;
      }
      delay(500);
    }

  String detection = objDetect();
  if (detection.length() > 0){

    Serial.printf("x1:%d, y1:%d, x2:%d, y2:%d", x_1, y_1, x_2, y_2);

  }

}
