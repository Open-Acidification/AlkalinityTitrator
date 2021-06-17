#define T_ON      500
#define STEP      6           // Pins D6 and D5 for STEP and Dir respectively
#define DIR       5           
#define LIM_1     4           // Pins D4 and D3 for LIM_F and LIM_E respectively
#define LIM_0     3           

byte N_b[4];      // Number turns
byte io[1];     // In - 0 / Out - 1
uint32_t N_int;

void setup() {
  // put your setup code here, to run once:
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(STEP, OUTPUT);
    pinMode(DIR, OUTPUT);
    Serial.begin(9600);
    //Seria1.begin(115200);
    
}

void loop() {
  
  N_int = 0;
  N_b[0] = 0;
  N_b[1] = 0;
  N_b[2] = 0;
  N_b[3] = 0;
  int i = 0;
  if(Serial.available()) {
    //digitalWrite(STEP, HIGH);
    Serial.readBytes(N_b, 4);
    Serial.readBytes(io, 1);

    // convert N_b to N_int: Thank you Jacob Priddy for helping with this
    N_int = (uint32_t(N_b[3]) << 24) | (uint32_t(N_b[2]) << 16) | (uint32_t(N_b[1]) << 8) | N_b[0];
    
    //Serial.println(N_int);
    if(N_int != 0) {
      if(io[0] == 0) {
        digitalWrite(DIR, HIGH);        
      }
      else {
        digitalWrite(DIR, LOW);
      }
      for(i = 0; i < N_int; i++) {
        if(digitalRead(LIM_1) == HIGH || digitalRead(LIM_0) == HIGH) {
          break;
        }
        else {
          //digitalWrite(LED_BUILTIN, HIGH);
          digitalWrite(STEP, HIGH);
          delayMicroseconds(T_ON);
          //digitalWrite(LED_BUILTIN, LOW);
          digitalWrite(STEP, LOW);
          delayMicroseconds(T_ON);     
        }
      }
      if(digitalRead(LIM_1) == HIGH || digitalRead(LIM_0) == HIGH){
        Serial.println(N_int - i);
      }
      else {
        Serial.println("DONE");
      }
    }    
  }
}
