//A4988 step motor direction PIN
const int MOTOR_1_DIR = 41;
//A4988 step motor step PIN
const int MOTOR_1_STEP = 42;
//relay PIN
const int LED_1 = 17;
const int LED_2 = 18;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Initialization...");

  pinMode(MOTOR_1_DIR, OUTPUT);
  pinMode(MOTOR_1_STEP, OUTPUT);
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);

  Serial.println("Finished initialization...");
}

void open(int motorDirectionAdr, int motorStepAdr){
  rotate(true, motorDirectionAdr, motorStepAdr);
}

void close(int motorDirectionAdr, int motorStepAdr){
  rotate(false, motorDirectionAdr, motorStepAdr);
}

void rotate(boolean direction, int motorDirectionAdr, int motorStepAdr){
  digitalWrite(motorDirectionAdr, direction);
  for (int i = 0; i < 200; i++) {
        digitalWrite(motorStepAdr, HIGH);
        delay(200);
        digitalWrite(motorStepAdr, LOW);
  }
}

void loop() {
    Serial.println("Start loop");
    digitalWrite(LED_1, LOW);
    digitalWrite(LED_2, HIGH);
    delay(2000);

    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_2, LOW);
    delay(1000);
    Serial.println("Finished loop");
}
