const int DATA_IN_0       = 19; // D-SUB Pin 2
const int DATA_IN_1       = 18; // D-SUB Pin 3
const int DATA_IN_2       = 2;  // D-SUB Pin 4
const int DATA_IN_3       = 3;  // D-SUB Pin 5
const int DATA_IN_4       = 4;  // D-SUB Pin 6
const int DATA_IN_5       = 5;  // D-SUB Pin 7
const int DATA_IN_6       = 6;  // D-SUB Pin 8
const int DATA_IN_7       = 7;  // D-SUB Pin 9
const int SELECT_IN_N     = 14; // D-SUB Pin 17
const int RESET_IN        = 15; // D-SUB Pin 16
const int LINEFEED_IN_N   = 16; // D-SUB Pin 14
const int STROBE_IN_N     = 17; // D-SUB Pin 1

const int ACK_OUT_N       = 8;  // D-SUB Pin 10
const int BUSY_OUT        = 9;  // D-SUB Pin 11
const int PAPER_OUT       = 10; // D-SUB Pin 12
const int SELECT_OUT      = 11; // D-SUB Pin 13
const int ERROR_OUT_N     = 12; // D-SUB Pin 15

volatile bool strobe_flag = false;

void setup() {
  pinMode(DATA_IN_0,      INPUT_PULLUP);
  pinMode(DATA_IN_1,      INPUT_PULLUP);
  pinMode(DATA_IN_2,      INPUT_PULLUP);
  pinMode(DATA_IN_3,      INPUT_PULLUP);
  pinMode(DATA_IN_4,      INPUT_PULLUP);
  pinMode(DATA_IN_5,      INPUT_PULLUP);
  pinMode(DATA_IN_6,      INPUT_PULLUP);
  pinMode(DATA_IN_7,      INPUT_PULLUP);
  pinMode(SELECT_IN_N,    INPUT_PULLUP);  // This mf stays HIGH forever on the HP 8596E …
  pinMode(RESET_IN,       INPUT_PULLUP);  // Don't care
  pinMode(LINEFEED_IN_N,  INPUT_PULLUP);  // Don't care
  pinMode(STROBE_IN_N,    INPUT_PULLUP);

  pinMode(ACK_OUT_N,      OUTPUT);  digitalWrite(ACK_OUT_N,   HIGH);
  pinMode(BUSY_OUT,       OUTPUT);  digitalWrite(BUSY_OUT,    LOW);
  pinMode(PAPER_OUT,      OUTPUT);  digitalWrite(PAPER_OUT,   LOW);
  pinMode(SELECT_OUT,     OUTPUT);  digitalWrite(SELECT_OUT,  HIGH);
  pinMode(ERROR_OUT_N,    OUTPUT);  digitalWrite(ERROR_OUT_N, HIGH);
  
  cli();
  PCICR |= 0b00000010;
  PCMSK1 |= 0b00001000;
  sei();

  delay(1000);
  Serial.begin(115200);
}

ISR(PCINT1_vect) {
  strobe_flag = true;
  digitalWrite(BUSY_OUT, HIGH);
}

void loop() {
  if (strobe_flag) {
    delayMicroseconds(20);
    
    strobe_flag = false;

    while (digitalRead(STROBE_IN_N) == LOW);

    delayMicroseconds(20);

    uint8_t data =
      digitalRead(DATA_IN_0) << 0 |
      digitalRead(DATA_IN_1) << 1 |
      digitalRead(DATA_IN_2) << 2 |
      digitalRead(DATA_IN_3) << 3 |
      digitalRead(DATA_IN_4) << 4 |
      digitalRead(DATA_IN_5) << 5 |
      digitalRead(DATA_IN_6) << 6 |
      digitalRead(DATA_IN_7) << 7;

    Serial.write(data);

    digitalWrite(ACK_OUT_N, LOW);
    delayMicroseconds(20);
    digitalWrite(ACK_OUT_N, HIGH);    
    delayMicroseconds(20);
    digitalWrite(BUSY_OUT, LOW);

    delayMicroseconds(20);
  }
}
