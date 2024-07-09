int PUL = 7;
int DIR = 6;
int ENA = 5;
long int steps = 0;

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()) {
    char val = Serial.read();
    if(val == '0') {
      Serial.println('0');
    }
    else if(val == '1') {
      long int move = steps;
      for(long int i=0; i<move; i++) {
          digitalWrite(DIR, LOW);
          digitalWrite(ENA, HIGH);
          digitalWrite(PUL, HIGH);
          delayMicroseconds(50);
          digitalWrite(PUL, LOW);
          delayMicroseconds(50);
          steps--;
          Serial.println(steps);
        }
      for(long int i=0; i<100000; i++) {
        char val2 = Serial.read();
        if(val2 == '2') {
          Serial.println('0');
          break;
        }
        digitalWrite(DIR, HIGH);
        digitalWrite(ENA, HIGH);
        digitalWrite(PUL, HIGH);
        delayMicroseconds(50);
        digitalWrite(PUL, LOW);
        delayMicroseconds(50);
        steps++;
        Serial.println(steps);
      }
      Serial.println(steps);
    }
  } 
}
