void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial1.begin(115200);
  delay(3000);
  Serial.println("wifi STA TCP test begin!");
  Serial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8040");
  Serial.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8040,WAITING...");
  delay(5000);

  Serial1.println("AT+CIPMODE=1");
  Serial.println("AT+CIPMODE=1,WAITING...");
  delay(2000);

  Serial1.println("AT+CIPSEND");
  Serial.println("AT+CIPSEND,WAITING...");
  delay(2000);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial1.println("transmit test");
  Serial.println("transmit test");
  delay(2000);
}
