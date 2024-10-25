// HalloweenCoffin.ino
// This code controls the Halloween coffin.
// It listens for a trigger from a controller and bangs/opens the coffin door when triggered.
// The coffin door then closes after a delay.
// This is meant to run on an Arduino Uno.


const int triggerPin = 3;     // the number of the blue pushbutton pin
const int doorPin =  7;      // the number of the coffin door relay in pin

void setup() {
  // initialize the door pin as an output
  pinMode(doorPin, OUTPUT);
  // initialize the door pin as an input
  pinMode(triggerPin, INPUT);
  
  Serial.begin(9600);               // starts the serial monitor
  delay(3000);
}

void loop() {
  // Only run when triggerPin is HIGH
  if (digitalRead(triggerPin) == HIGH) {
    Serial.println("BOO");

    digitalWrite(doorPin, HIGH);
    delay(300);
    digitalWrite(doorPin, LOW);
    delay(500);

    digitalWrite(doorPin, HIGH);
    delay(300);
    digitalWrite(doorPin, LOW);
    delay(500);

    digitalWrite(doorPin, HIGH);
    delay(300);
    digitalWrite(doorPin, LOW);
    delay(500);

    digitalWrite(doorPin, HIGH);
    delay(300);
    digitalWrite(doorPin, LOW);
    delay(500);

    digitalWrite(doorPin, HIGH);
    delay(300);
    digitalWrite(doorPin, LOW);
    delay(500);

    digitalWrite(doorPin, HIGH);
    delay(7000);
    digitalWrite(doorPin, LOW);
    
    // Wait until trigger is released to prevent multiple triggers
    while(digitalRead(triggerPin) == HIGH) {
      delay(10);
    }
  }
}