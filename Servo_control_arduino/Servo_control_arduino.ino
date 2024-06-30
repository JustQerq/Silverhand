#include <Servo.h>
#include <string.h>

const int num_servos = 5;
Servo servos[num_servos] = {};

int angles[num_servos];
int angles_new[num_servos];
const int angle_min = 0;
const int angle_max[num_servos] = {130, 130, 130, 130, 90};
const int d = 10; // delay between servo steps

void setup() {
  servos[0].attach(3);
  servos[0].write(angle_min);
  servos[1].attach(5);
  servos[1].write(angle_min);
  servos[2].attach(6);
  servos[2].write(angle_min);
  servos[3].attach(9);
  servos[3].write(angle_min);
  servos[4].attach(10);
  servos[4].write(angle_min);

  for(int i=0; i<5; i++){angles[i] = angle_min;}
  for(int i=0; i<5; i++){angles_new[i] = angle_min;}
  Serial.begin(115200);
  Serial.setTimeout(20);
  Serial.flush();
}

void loop() {
  if(Serial.available() > 0){
    Serial.print("Angles set to: ");
    for(int i=0; i<num_servos; i++){
      angles_new[i] = Serial.parseInt();
      angles_new[i] = constrain((angles_new[i] + angle_min), angle_min, angle_max[i]);
      angles[i] = angles_new[i];
      servos[i].write(angles[i]);
      Serial.print(angles[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
  // if(angle > angle_new){
  //   //myservo.write(--angle);
  //   delay(d);
  // }
  // else if(angle < angle_new){
  //   //myservo.write(++angle);
  //   delay(d);
  // }
}