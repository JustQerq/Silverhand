#include <Servo.h>
#include <string.h>

Servo s;
int angle = 90;

void setup() {
  s.attach(9);
  s.write(angle);
  
  Serial.begin(115200);
  Serial.setTimeout(20);
  Serial.flush();
}

void loop() {
  if(Serial.available()){
    angle = Serial.parseInt();
    s.write(angle);
    Serial.print("Angle set to ");
    Serial.print(angle);
    Serial.println();
  }
}
