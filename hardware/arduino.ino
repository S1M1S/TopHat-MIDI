int lightOut = 13;
int buttonState1 = 0;
int buttonState2 = 0;
int oldButtonState1 = 0;
int oldButtonState2 = 0;

void setup() {
  pinMode(1, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  buttonState1 = digitalRead(1);
  buttonState2 = digitalRead(2);
  
  if(buttonState2 == LOW) {
    Serial.println("LOW");
    digitalWrite(13, LOW);
  }
  else {
    digitalWrite(13, HIGH);
  }
  oldButtonState1 = buttonState1;
  oldButtonState2 = buttonState2;
}

