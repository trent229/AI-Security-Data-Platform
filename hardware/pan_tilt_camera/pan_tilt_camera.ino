#include <Servo.h>

Servo panServo;
Servo tiltServo;

const int PAN_PIN = 9;
const int TILT_PIN = 10;

const int PAN_MIN = 30;
const int PAN_MAX = 150;
const int TILT_HOME = 95;

int panPos = 90;
int panStep = 2;

void setup() {
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);

  panServo.write(panPos);
  tiltServo.write(TILT_HOME);

  Serial.begin(9600);
  Serial.println("Autonomous Pan-Tilt Tracking Camera Started");
}

void loop() {
  autonomousScan();
}

void autonomousScan() {
  panServo.write(panPos);
  tiltServo.write(TILT_HOME);

  panPos += panStep;

  if (panPos >= PAN_MAX || panPos <= PAN_MIN) {
    panStep = -panStep;
  }

  Serial.print("Pan: ");
  Serial.print(panPos);
  Serial.print(" | Tilt: ");
  Serial.println(TILT_HOME);

  delay(50);
}
