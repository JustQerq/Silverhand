#include <Servo.h>
#include <string.h>

const int num_servos = 4;
Servo servos[num_servos] = {};

int angles[num_servos];
int angles_new[num_servos];
const int angles_min[num_servos] = {0, 95, 0, 0}; // wrist fixed in place for now
const int angles_max[num_servos] = {180, 170, 180, 180};
const int angles_default[num_servos] = {90, 170, 90, 90};
const int d = 10; // delay between servo steps

void setup() {
  servos[0].attach(3);
  servos[0].write(angles_default[0]);
  servos[1].attach(5);
  servos[1].write(angles_default[1]);
  servos[2].attach(6);
  servos[2].write(angles_default[2]);
  servos[3].attach(9);
  servos[3].write(angles_default[3]);

  for(int i=0; i<num_servos; i++){angles[i] = angles_default[i];}
  for(int i=0; i<num_servos; i++){angles_new[i] = angles_default[i];}
  Serial.begin(115200);
  Serial.setTimeout(20);
  Serial.flush();
}

void loop() {
  if(Serial.available() > 0){
    Serial.print("Angles set to: ");

    angles_new[0] = Serial.parseInt();
    angles_new[0] = constrain(angles_new[0], angles_min[0], angles_max[0]);
    angles[0] = angles_new[0];
    servos[0].write(angles[0]);
    Serial.print(angles[0]);

    angles_new[1] = 180 - Serial.parseInt();
    angles_new[1] = constrain(angles_new[1], angles_min[1], angles_max[1]);
    angles[1] = angles_new[1];
    servos[1].write(angles[1]);
    Serial.print(angles[1]);

    angles_new[2] = Serial.parseInt();
    angles_new[2] = constrain(angles_new[2], angles_min[2], angles_max[2]);
    angles[2] = angles_new[2];
    servos[2].write(angles[2]);
    Serial.print(angles[2]);

    angles_new[3] = 90 - Serial.parseInt();
    angles_new[3] = constrain(angles_new[3], angles_min[3], angles_max[3]);
    angles[3] = angles_new[3];
    servos[3].write(angles[3]);
    Serial.print(angles[3]);

    // for(int i=2; i<num_servos; i++){
    //   angles_new[i] = Serial.parseInt();
    //   angles_new[i] = constrain(angles_new[i], angles_min[i], angles_max[i]);
    //   angles[i] = angles_new[i];
    //   servos[i].write(angles[i]);
    //   Serial.print(angles[i]);
    // }
    Serial.println();
  }
}