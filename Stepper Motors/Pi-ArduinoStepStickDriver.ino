#define T_ON      500
#define STEP      2           // Pins D2 and D3 for STEP and Dir respectively
#define DIR       3

byte N_b[4];      // Number turns
byte io[1];     // In - 0 / Out - 1
uint32_t N_int;

void setup() {
  // put your setup code here, to run once:
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(STEP, OUTPUT);
    pinMode(DIR, OUTPUT);
    Serial.begin(9600);
    //Serial1.begin(115200);
    
}

void loop() {
  
  N_int = 0;
  N_b[0] = 0;
  N_b[1] = 0;
  N_b[2] = 0;
  N_b[3] = 0;
  
  if(Serial.available()) {
    //digitalWrite(STEP, HIGH);
    Serial.readBytes(N_b, 4);
    Serial.readBytes(io, 1);

    // convert N_b to N_int: Thank you Jacob Priddy for helping with this
    N_int = (N_b[3] << 24) | (N_b[2] << 16) | (N_b[1] << 8) | N_b[0];
    
    //Serial.println(N_int);
    if(N_int != 0) {
      if(io[0] == 0) {
        digitalWrite(DIR, HIGH);        
      }
      else {
        digitalWrite(DIR, LOW);
      }
      for(int i=0; i < N_int; i++) {
        //digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(STEP, HIGH);
        delayMicroseconds(T_ON);
        //digitalWrite(LED_BUILTIN, LOW);
        digitalWrite(STEP, LOW);
        delayMicroseconds(T_ON);     
      }

      Serial.println("DONE");
    }
    
  }

}
