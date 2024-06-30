#include <Servo.h>
#include <string.h>

const int num_servos = 4;
Servo servos[num_servos] = {};

const int potentio_pin = A0;
int angle_potentio = 0;

int angles[num_servos];
int angles_new[num_servos];
const int angles_min[num_servos] = {0, 95, 0, 0};
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
  angle_potentio = analogRead(potentio_pin);
  //angle_potentio = int(float(angle_potentio) / 1023 * 270);
  //angle_potentio = constrain(angle_potentio, angles_min[1], angles_max[1]);
  
  //servos[1].write(angle_potentio);
  Serial.println(angle_potentio);
  delay(300);
}