UART softSerial1(analogPinToPinName(6), analogPinToPinName(7), NC, NC);
UART softSerial2(digitalPinToPinName(2), digitalPinToPinName(0), NC, NC);
void setup() {
  softSerial1.begin(115200);
  softSerial2.begin(115200);
  Serial.begin(115200);
  // softSerial1.listen();
  delay(3000);
  softSerial2.println("Serial1 OK");
  Serial.println("Serial OK");
  softSerial1.println("wifi STA TCP test begin!");
  softSerial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8020");
  softSerial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8020,WAITING...");
  delay(5000);
  softSerial2.println("Serial1 OK");
  Serial.println("Serial OK");

  softSerial1.println("AT+CIPMODE=1");
  softSerial1.println("AT+CIPMODE=1,WAITING...");
  delay(2000);
  softSerial2.println("Serial1 OK");
  Serial.println("Serial OK");

  softSerial1.println("AT+CIPSEND");
  softSerial1.println("AT+CIPSEND,WAITING...");
  delay(2000);
  softSerial2.println("Serial1 OK");
  Serial.println("Serial OK");
}

void loop() {
  // put your main code here, to run repeatedly:

}
