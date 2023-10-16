#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
int buzzerPin = 12;
int ledPin = 12;
int threshold = 999991;
bool triggered = false;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  mpu.initialize();
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  if (abs(ax) > threshold || abs(ay) > threshold || abs(az) > threshold) {
    if (!triggered) {
      digitalWrite(ledPin, HIGH);
      tone(buzzerPin, 1000);
      triggered = true;
    }
  }
  else {
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
    triggered = false;
  }
}