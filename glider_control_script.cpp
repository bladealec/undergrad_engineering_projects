
#include <Servo.h>  // For servo control

// Pin configuration
const int dropPin = 2; // Pin to detect drop (assuming a digital input)
const int servoPin = 9; // Servo control pin for ailerons

// Variables for drop detection
bool isDropped = false;
Servo aileronServo; // Create servo object for controlling aileron

// Flight parameters
const int neutralPosition = 90; // Neutral position for servo (example)
const int fullTurnPosition = 180; // Servo position for turn (180 degrees)

void setup() {
  // Initialize pin modes
  pinMode(dropPin, INPUT);  // Pin to detect drop

  // Initialize servo
  aileronServo.attach(servoPin); // Attach servo to pin

  // Set servo to neutral position initially
  aileronServo.write(neutralPosition);  
}

void loop() {
  // Check if the drop pin is disconnected (or changed state)
  if (digitalRead(dropPin) == LOW) {  // Assuming LOW indicates drop (adjust based on your wiring)
    if (!isDropped) {
      isDropped = true;  // Mark as dropped
      performTurn();  // Start performing a 360-degree turn
    }
  }

  // Other flight control logic (e.g., keep the glider flying straight before drop)
  if (!isDropped) {
    // Ascend to required altitude or maintain glide path here
    // This would generally be handled by the flight controller's flight modes (e.g., using stabilization or altitude control)
  }
}

// Function to perform a 360-degree turn
void performTurn() {
  // Turn the glider by moving the aileron servo
  aileronServo.write(fullTurnPosition); // Turn to 180 degrees (adjust for your glider's turn rate)
  delay(5000); // Adjust duration for a complete 360-degree turn (depending on your glider and turn rate)

  // After 360-degree turn, return the servo to neutral
  aileronServo.write(neutralPosition); // Return to neutral after turn
  delay(2000); // Wait for a moment before completing the loop
}
