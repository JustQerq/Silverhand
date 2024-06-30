#include <Arduino.h>
#include <string>

#define ISR_SERVO_DEBUG             0
#define TIMER_INTERRUPT_DEBUG       0
#include <ESP8266_ISR_Servo.h>

// Published values for SG90 servos; adjust if needed
// DS3225MG: 500-2500
#define MIN_MICROS      500  //544
#define MAX_MICROS      2450

#define NUM_SERVOS    5

int angles_min[NUM_SERVOS] = {0, 0, 0, 0, 0};
int angles_max[NUM_SERVOS] = {120, 120, 120, 120, 90};
int angles[NUM_SERVOS] = {};
int angles_new[NUM_SERVOS] = {};

typedef struct
{
  int     servoIndex;
  uint8_t servoPin;
} ISR_servo_t;

ISR_servo_t ISR_servo[NUM_SERVOS] =
{
  { -1, D1 }, {-1, D2}, {-1, D3}, {-1, D4}, {-1, D5}
};

void setup()
{
  Serial.begin(115200);
  //Serial.println("\nStarting");

  for (int index = 0; index < NUM_SERVOS; index++)
  {
    ISR_servo[index].servoIndex = ISR_Servo.setupServo(ISR_servo[index].servoPin, MIN_MICROS, MAX_MICROS);
    angles[index] = angles_min[index];
    ISR_Servo.setPosition(ISR_servo[index].servoIndex, angles[index]);

    // if (ISR_servo[index].servoIndex != -1)
    //   Serial.println("Setup OK Servo index = " + String(ISR_servo[index].servoIndex));
    // else
    //   Serial.println("Setup Failed Servo index = " + String(ISR_servo[index].servoIndex));
  }
}

void loop()
{
  if(Serial.available() > 0)
  {
    for(int i=0; i<5; i++){
      angles_new[i] = Serial.parseInt();
      angles_new[i] = constrain((angles_new[i] + angles_min[i]), angles_min[i], angles_max[i]);
    }
    //Serial.print("Angles set to: ");
    for (int index = 0; index < NUM_SERVOS; index++)
    {
      angles[index] = angles_new[index];
      ISR_Servo.setPosition(ISR_servo[index].servoIndex, angles[index]);
      //Serial.print(angles[index]);
      //Serial.print(" ");
    }
    //Serial.println();
  }
}