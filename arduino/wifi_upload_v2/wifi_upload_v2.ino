/*
  Active Learning Labs
  Harvard University 
  tinyMLx - OV7675 Camera Test

*/

#include <TinyMLShield.h>

//a6 TX     a7 RX
UART softSerial1(analogPinToPinName(6), analogPinToPinName(7), NC, NC);


bool commandRecv = false; // flag used for indicating receipt of commands from serial port
bool liveFlag = false; // flag as true to live stream raw camera bytes, set as false to take single images on command
bool captureFlag = false;

// Image buffer;
byte image[320 * 240 * 2]; // QCIF: 176x144 x 2 bytes per pixel (RGB565)
long long bytesPerFrame;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  softSerial1.begin(115200);
  while(!softSerial1);
  

  //softSerial1.println("softSerial test");
  initializeShield();

  // Initialize the OV7675 camera
  if (!Camera.begin(QVGA, RGB565, 1, OV7675)) {
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();

  //Serial.println("Welcome to the OV7675 test\n");
  //Serial.println("Available commands:\n");
  //Serial.println("single - take a single image and print out the hexadecimal for each pixel (default)");
  //Serial.println("live - the raw bytes of images will be streamed live over the serial port");
  //Serial.println("capture - when in single mode, initiates an image capture");


  //wifi init
  //Serial.begin(115200);
  // Serial1.begin(115200);
  // delay(3000);
  // Serial.println("wifi STA TCP test begin!");
  // Serial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8080");
  // Serial.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8080,WAITING...");
  // delay(5000);

  // Serial1.println("AT+CIPMODE=1");
  // Serial.println("AT+CIPMODE=1,WAITING...");
  // delay(2000);

  // Serial1.println("AT+CIPSEND");
  // Serial.println("AT+CIPSEND,WAITING...");
  // delay(2000);


  
  // softSerial1.listen();
  delay(3000);
  softSerial1.println("wifi STA TCP test begin!");
  softSerial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8090");
  softSerial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8090,WAITING...");
  delay(5000);

  softSerial1.println("AT+CIPMODE=1");
  softSerial1.println("AT+CIPMODE=1,WAITING...");
  delay(2000);

  softSerial1.println("AT+CIPSEND");
  softSerial1.println("AT+CIPSEND,WAITING...");
  delay(2000);
}

void loop() {
  int i = 0;
  String command;

  bool clicked = readShieldButton();
  if (clicked) {
    if (!liveFlag) {
      if (!captureFlag) {
        captureFlag = true;
      }
    }
  }

  // Read incoming commands from serial monitor
  while (Serial.available()) {
    char c = Serial.read();
    if ((c != '\n') && (c != '\r')) {
      command.concat(c);
    } 
    else if (c == '\r') {
      commandRecv = true;
      command.toLowerCase();
    }
  }

  // Command interpretation
  if (commandRecv) {
    commandRecv = false;
    if (command == "live") {
      //Serial.println("\nRaw image data will begin streaming in 5 seconds...");
      liveFlag = true;
      delay(5000);
    }
    else if (command == "single") {
      //Serial.println("\nCamera in single mode, type \"capture\" to initiate an image capture");
      liveFlag = false;
      delay(200);
    }
    else if (command == "capture") {
      if (!liveFlag) {
        if (!captureFlag) {
          captureFlag = true;
        }
        delay(200);
      }
      else {
        //Serial.println("\nCamera is not in single mode, type \"single\" first");
        delay(1000);
      }
    }
  }
  
  if (liveFlag) {
    Camera.readFrame(image);
    Serial.write(image, bytesPerFrame);
  }
  else {
    if (captureFlag) {
      captureFlag = false;
      Camera.readFrame(image);
      //Serial.println("\nImage data will be printed out in 3 seconds...");
      delay(3000);
      for (int i = 0; i < bytesPerFrame - 1; i += 2) {
        Serial.print("0x");
        Serial.print(image[i+1], HEX);
        Serial.print(image[i], HEX);
        if (i != bytesPerFrame - 2) {
          Serial.print(", ");
        }
      }
      Serial.println();

      //wifi upload
      for (int i = 0; i < bytesPerFrame - 1; i += 2) {
        softSerial1.print("0x");
        softSerial1.print(image[i+1], HEX);
        softSerial1.print(image[i], HEX);
        if (i != bytesPerFrame - 2) {
          softSerial1.print(", ");
        }
      }
      softSerial1.println();
    }
  }
}
